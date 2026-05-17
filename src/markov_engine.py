"""Lightweight offline code generation engine.

Uses a template-retrieval approach: stores complete, working Python snippets
indexed by keywords. Given a prompt, it finds the best-matching snippet(s)
and returns them. A simple n-gram model is kept for variable-name
substitution and light augmentation, but the core output is always a
real, tested code snippet — never random token soup.

The trained model is serialized to a small JSON file for instant loading.
No external ML libraries required — pure Python + stdlib.
"""

import json
import os
import re
import random
from dataclasses import dataclass, field

from src.code_composer import compose_code


@dataclass
class MarkovModel:
    """A trained model containing indexed code snippets and n-gram data."""

    n: int = 3
    # Each snippet: {"code": str, "keywords": list[str], "description": str}
    snippets: list[dict] = field(default_factory=list)
    # N-gram transitions (kept for potential augmentation)
    transitions: dict[str, dict[str, int]] = field(default_factory=dict)
    starters: list[list[str]] = field(default_factory=list)

    def save(self, path: str) -> None:
        """Serialize the model to a JSON file."""
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        data = {
            "n": self.n,
            "snippets": self.snippets,
            "transitions": self.transitions,
            "starters": self.starters,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, separators=(",", ":"))

    @classmethod
    def load(cls, path: str) -> "MarkovModel":
        """Load a model from a JSON file."""
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        model = cls(n=data.get("n", 3))
        model.snippets = data.get("snippets", [])
        model.transitions = data.get("transitions", {})
        model.starters = [list(s) for s in data.get("starters", [])]
        return model


# ---------------------------------------------------------------------------
# Keyword extraction helpers
# ---------------------------------------------------------------------------

# Common English stop words to ignore during matching
# NOTE: Language keywords like for, while, if, class, def, fork, thread are
# intentionally kept OUT of this set so they can be used for snippet matching.
_STOP_WORDS = frozenset({
    "a", "an", "the", "is", "it", "to", "in", "of", "and", "or",
    "that", "this", "with", "on", "at", "by", "from", "as", "be", "was",
    "are", "been", "being", "have", "has", "had", "do", "does", "did",
    "will", "would", "could", "should", "may", "might", "can", "shall",
    "me", "my", "i", "you", "your", "we", "our", "they", "them", "he",
    "she", "his", "her", "its", "not", "no", "but", "so", "up",
    "out", "about", "into", "over", "after", "how", "what", "which",
    "who", "when", "where", "why", "all", "each", "every", "both",
    "few", "more", "most", "some", "any", "make", "just", "also",
    "than", "then", "now", "here", "there", "very", "too", "only",
    "please", "want", "need", "using", "use", "create",
    "give", "show", "code", "example",
})

# Words that carry extra weight when matching prompts to snippets.
# These help distinguish e.g. "for loop" from "while loop".
_HIGH_VALUE_WORDS = frozenset({
    "for", "while", "if", "else", "class", "def", "lambda", "try",
    "except", "import", "return", "yield", "async", "await", "with",
    "list", "dict", "set", "tuple", "string", "file", "csv", "json",
    "sort", "search", "binary", "bubble", "stack", "queue", "tree",
    "recursion", "recursive", "fibonacci", "factorial", "inheritance",
    "property", "decorator", "comprehension", "generator", "iterator",
    "read", "write", "parse", "format", "count", "sum", "print",
    "loop", "function", "class", "error", "exception", "handling",
    # DSA-specific terms
    "merge", "quick", "heap", "insertion", "selection", "counting",
    "linked", "doubly", "bst", "trie", "prefix", "graph", "bfs",
    "dfs", "dijkstra", "topological", "shortest", "path", "cycle",
    "dynamic", "programming", "knapsack", "lcs", "subsequence",
    "coin", "change", "edit", "distance", "levenshtein", "matrix",
    "chain", "backtracking", "permutation", "combination", "subset",
    "queens", "sliding", "window", "pointer", "palindrome",
    "hashmap", "hash", "priority", "inorder", "preorder", "postorder",
    "traversal", "adjacency", "weighted", "directed", "undirected",
    # Shell scripting / Bash / Ubuntu terms
    "bash", "shell", "script", "terminal", "command", "ubuntu", "linux",
    "chmod", "chown", "grep", "awk", "sed", "pipe", "redirect",
    "cron", "crontab", "systemctl", "service", "apt", "dpkg",
    "ssh", "scp", "rsync", "tar", "curl", "wget", "find", "xargs",
    "variable", "array", "loop", "case", "select", "getopts",
    "trap", "signal", "function", "alias", "export", "source",
    "regex", "pattern", "substitution", "stream", "filter",
    "daemon", "background", "foreground", "job", "nohup",
    "permission", "owner", "group", "umask", "sticky",
    "symlink", "hardlink", "inode", "mount", "filesystem",
    "process", "pid", "kill", "nice", "renice", "top", "ps",
    "network", "interface", "ip", "route", "firewall", "iptables",
    "ufw", "netstat", "ss", "dns", "hostname", "port",
    # C / OS concepts terms
    "fork", "exec", "execvp", "wait", "waitpid", "pipe", "dup2",
    "thread", "pthread", "mutex", "semaphore", "deadlock",
    "process", "pid", "getpid", "getppid", "zombie", "orphan",
    "signal", "sighandler", "sigaction", "sigint", "sigterm",
    "shared", "memory", "shm", "mmap", "ipc", "msgqueue",
    "socket", "bind", "listen", "accept", "connect", "tcp", "udp",
    "malloc", "calloc", "realloc", "free", "pointer", "struct",
    "header", "include", "makefile", "gcc", "compile", "linker",
    "stdin", "stdout", "stderr", "descriptor", "open", "close",
    "scheduling", "context", "switch", "race", "condition",
    "critical", "section", "producer", "consumer", "reader", "writer",
    "dining", "philosophers", "barrier", "condvar", "spinlock",
})


def _extract_keywords(text: str) -> set[str]:
    """Extract meaningful keywords from a text string."""
    words = set(re.findall(r"[a-z][a-z0-9_]*", text.lower()))
    return words - _STOP_WORDS


# ---------------------------------------------------------------------------
# Trainer
# ---------------------------------------------------------------------------

class MarkovTrainer:
    """Trains a MarkovModel from Python code snippets."""

    def __init__(self, n: int = 3) -> None:
        self.n = n
        self._snippets: list[dict] = []
        self._transitions: dict[str, dict[str, int]] = {}
        self._starters: list[list[str]] = []

    def add_snippet(self, code: str, description: str = "") -> None:
        """Add a complete code snippet with an optional description.

        Keywords are auto-extracted from both the code and description.
        """
        code = code.strip()
        if not code:
            return

        # Extract keywords from description, comments, and identifiers
        comment_text = " ".join(re.findall(r"#\s*(.*)", code))
        all_text = f"{description} {comment_text} {code}"
        keywords = sorted(_extract_keywords(all_text))

        self._snippets.append({
            "code": code,
            "keywords": keywords,
            "description": description.strip() or self._extract_first_comment(code),
        })

    def build(self) -> MarkovModel:
        """Build the final MarkovModel."""
        model = MarkovModel(n=self.n)
        model.snippets = self._snippets
        model.transitions = self._transitions
        model.starters = self._starters
        return model

    @staticmethod
    def _extract_first_comment(code: str) -> str:
        """Extract the first comment line as a description."""
        for line in code.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("# ").strip()
        return ""


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class MarkovGenerator:
    """Generates code by retrieving the best-matching snippet(s).

    This is a retrieval-based generator: it finds the snippet whose keywords
    best match the user's prompt and returns it. Supports Python, Bash/Shell,
    and C code snippets. Multiple snippets may be combined if the prompt
    touches several topics.
    """

    def __init__(self, model: MarkovModel) -> None:
        self._model = model
        self._rng = random.Random()

    def generate(self, prompt: str, max_tokens: int = 200, temperature: float = 0.7) -> str:
        """Generate code based on a prompt by retrieving matching snippets."""
        # If prompt contains session context, extract only the last user message
        if "User:" in prompt:
            lines = prompt.strip().splitlines()
            for line in reversed(lines):
                if line.startswith("User:"):
                    prompt = line[len("User:"):].strip()
                    break

        prompt_keywords = _extract_keywords(prompt)
        if not prompt_keywords:
            prompt_keywords = set(re.findall(r"[a-z][a-z0-9_]*", prompt.lower()))

        scored = self._score_snippets(prompt_keywords)

        # Try composition for prompts that describe a specific function to build.
        # The composer already returns None for known algorithm/DSA requests,
        # so if it produces code, it's the right answer for this prompt.
        composed = compose_code(prompt)
        if composed:
            return composed

        best_score = scored[0][0] if scored else 0

        if not scored or best_score == 0:
            return self._fallback_response(prompt)

        # Return the top match, or combine top 2 if they're both strong matches
        best_score = scored[0][0]
        top_snippets = [s for score, s in scored if score >= best_score * 0.7]

        if len(top_snippets) == 1:
            return self._format_output(prompt, top_snippets[0])

        # Pick the best one, or combine two complementary ones
        primary = top_snippets[0]
        # Check if there's a second snippet that adds different info
        if len(top_snippets) >= 2:
            secondary = top_snippets[1]
            primary_kw = set(primary["keywords"])
            secondary_kw = set(secondary["keywords"])
            # Only combine if they cover different aspects
            if len(secondary_kw - primary_kw) > 2:
                return self._format_combined(prompt, primary, secondary)

        return self._format_output(prompt, primary)

    def generate_stream(self, prompt: str, max_tokens: int = 200) -> list[str]:
        """Generate code and return as a list of line chunks for streaming."""
        code = self.generate(prompt, max_tokens)
        lines = code.split("\n")
        return [line + "\n" for line in lines]

    def _score_snippets(self, prompt_keywords: set[str]) -> list[tuple[float, dict]]:
        """Score all snippets using weighted keyword overlap.

        High-value words (Python keywords, specific terms) get 3x weight.
        Description matches get a strong bonus.
        Language context is used to prefer snippets in the right language.
        Coverage bonus rewards snippets that match MORE of the prompt keywords.
        """
        scored = []

        # Detect language context from prompt keywords
        lang_context = self._detect_language_context(prompt_keywords)
        prompt_size = len(prompt_keywords)

        for snippet in self._model.snippets:
            snippet_kw = set(snippet["keywords"])
            overlap = prompt_keywords & snippet_kw
            if not overlap:
                continue

            # Base score: 1 point per keyword, 3 points for high-value matches
            score = 0.0
            for word in overlap:
                score += 3.0 if word in _HIGH_VALUE_WORDS else 1.0

            # Strong bonus for matching words in the snippet description
            desc_lower = snippet.get("description", "").lower()
            desc_words = set(re.findall(r"[a-z][a-z0-9_]*", desc_lower))
            desc_overlap = prompt_keywords & desc_words
            score += len(desc_overlap) * 3.0

            # Coverage bonus: reward snippets that cover a higher percentage
            # of the prompt keywords. This helps complex prompts find
            # comprehensive snippets rather than partial matches.
            coverage = len(overlap) / max(prompt_size, 1)
            score *= (1.0 + coverage)  # Up to 2x multiplier for full coverage

            # Code content bonus: check if prompt keywords appear in the
            # actual code (not just extracted keywords). This catches things
            # like specific command names, variable patterns, etc.
            code_lower = snippet.get("code", "").lower()
            code_hits = sum(1 for kw in prompt_keywords if kw in code_lower)
            score += code_hits * 1.5

            # Extra bonus: check if multi-word phrases from the prompt appear
            # in the description (e.g. "merge sort", "linked list")
            prompt_text = " ".join(sorted(prompt_keywords))
            for phrase_len in (3, 2):
                prompt_words = list(prompt_keywords)
                for i in range(len(prompt_words)):
                    for j in range(i + 1, min(i + phrase_len + 1, len(prompt_words) + 1)):
                        phrase = " ".join(prompt_words[i:j])
                        if phrase in desc_lower:
                            score += 5.0

            # Language context bonus/penalty
            snippet_lang = self._detect_snippet_language(snippet)
            if lang_context and snippet_lang:
                if snippet_lang == lang_context:
                    score *= 1.5  # 50% bonus for matching language
                elif snippet_lang != "python" or lang_context != "any":
                    score *= 0.4  # 60% penalty for wrong language

            scored.append((score, snippet))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored

    @staticmethod
    def _detect_language_context(prompt_keywords: set) -> str:
        """Detect which language the user is asking about."""
        shell_words = {"bash", "shell", "script", "ubuntu", "linux", "terminal",
                       "chmod", "grep", "awk", "sed", "apt", "systemctl", "cron",
                       "crontab", "ssh", "scp", "rsync", "tar", "curl", "wget",
                       "find", "xargs", "pipe", "redirect", "daemon", "nohup",
                       "ufw", "iptables", "getopts", "shebang"}
        c_words = {"fork", "exec", "pthread", "mutex", "semaphore", "malloc",
                   "calloc", "free", "struct", "typedef", "include", "gcc",
                   "makefile", "socket", "bind", "listen", "accept", "connect",
                   "sigaction", "sighandler", "mmap", "shm", "fifo", "dup2",
                   "waitpid", "getpid", "zombie", "orphan", "deadlock",
                   "spinlock", "barrier", "condvar", "pid"}

        if prompt_keywords & shell_words:
            return "shell"
        if prompt_keywords & c_words:
            return "c"
        return ""

    @staticmethod
    def _detect_snippet_language(snippet: dict) -> str:
        """Detect the language of a snippet from its code content."""
        code = snippet.get("code", "")
        if "#include" in code or "int main(" in code or "void " in code:
            return "c"
        if code.lstrip().startswith("#!/bin/bash") or code.lstrip().startswith("#!/bin/sh"):
            return "shell"
        # Check for strong shell indicators
        shell_patterns = ["echo ", "fi\n", "done\n", "esac", "then\n"]
        if any(p in code for p in shell_patterns):
            return "shell"
        return "python"

    @staticmethod
    def _format_output(prompt: str, snippet: dict) -> str:
        """Format a single snippet as the response."""
        desc = snippet.get("description", "")
        header = f"# {desc}" if desc else f"# Generated for: {prompt}"
        code = snippet["code"]
        # If the code already starts with a comment, don't double up
        if code.lstrip().startswith("#"):
            return code
        return f"{header}\n{code}"

    @staticmethod
    def _format_combined(prompt: str, primary: dict, secondary: dict) -> str:
        """Combine two snippets into a single response."""
        parts = []
        parts.append(primary["code"])
        parts.append("")
        parts.append("# --- Additional related example ---")
        parts.append("")
        parts.append(secondary["code"])
        return "\n".join(parts)

    @staticmethod
    def _fallback_response(prompt: str) -> str:
        """Return a helpful message when no matching snippet is found."""
        return (
            f"# I don't have a specific example for: {prompt}\n"
            "# Here's a starter template you can build on:\n"
            "\n"
            "# Topics I know about:\n"
            "#\n"
            "# Python:\n"
            "# - loops (for, while, list comprehension)\n"
            "# - functions (factorial, fibonacci, recursion)\n"
            "# - file I/O (read, write, CSV, JSON)\n"
            "# - classes (OOP, inheritance, properties)\n"
            "# - sorting (bubble, merge, quick, heap sort)\n"
            "# - data structures (stack, queue, linked list, BST, graph)\n"
            "# - dynamic programming (knapsack, LCS, coin change)\n"
            "# - strings (formatting, manipulation)\n"
            "# - error handling (try/except, custom exceptions)\n"
            "#\n"
            "# Shell Scripting / Ubuntu:\n"
            "# - bash basics (variables, arrays, strings)\n"
            "# - loops (for, while, until, select)\n"
            "# - conditionals (if/elif/else, case, test operators)\n"
            "# - functions, getopts, error handling\n"
            "# - text processing (grep, awk, sed, cut, sort)\n"
            "# - file operations (find, chmod, chown, tar, rsync)\n"
            "# - process management (ps, kill, nice, nohup, jobs)\n"
            "# - system admin (apt, systemctl, cron, user management)\n"
            "# - networking (ssh, scp, ufw, iptables, curl)\n"
            "# - pipes and redirection\n"
            "#\n"
            "# C / OS Concepts:\n"
            "# - process creation (fork, exec, wait, zombie, orphan)\n"
            "# - threading (pthread_create, pthread_join)\n"
            "# - synchronization (mutex, semaphore, condition variable)\n"
            "# - classic problems (producer-consumer, reader-writer, dining philosophers)\n"
            "# - IPC (pipes, named pipes/FIFO, shared memory)\n"
            "# - signals (signal, sigaction, kill)\n"
            "# - socket programming (TCP/UDP server and client)\n"
            "# - memory management (malloc, calloc, realloc, free)\n"
            "# - file I/O (open, read, write, lseek, file descriptors)\n"
            "# - compilation (gcc, Makefile)\n"
        )
