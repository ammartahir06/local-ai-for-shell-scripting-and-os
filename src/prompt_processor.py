"""Prompt processing and validation for the Offline Coding AI Assistant.

Validates user input, builds conversational context from session history,
and classifies prompts as coding-related or not.
"""

from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of prompt validation."""

    is_valid: bool
    error_message: str | None = None


class PromptProcessor:
    """Validates, interprets, and contextualizes user prompts."""

    MAX_PROMPT_LENGTH: int = 2000

    # Keywords that suggest a coding request
    _CODING_KEYWORDS: set[str] = {
        "code", "function", "class", "write", "implement", "create",
        "program", "script", "debug", "fix", "error", "bug",
        "python", "loop", "list", "dict", "dictionary", "string",
        "file", "read", "parse", "sort", "search", "algorithm",
        "import", "module", "package", "variable", "print",
        "return", "def", "for", "while", "if", "try", "except",
        "api", "http", "json", "csv", "database", "sql",
        "array", "stack", "queue", "tree", "graph", "recursion",
        "explain", "example", "how to", "generate", "build",
        "convert", "calculate", "compute", "fibonacci", "factorial",
        # Shell scripting / Bash / Ubuntu
        "bash", "shell", "terminal", "command", "ubuntu", "linux",
        "chmod", "chown", "grep", "awk", "sed", "pipe", "redirect",
        "cron", "crontab", "systemctl", "service", "apt", "dpkg",
        "ssh", "scp", "rsync", "tar", "zip", "unzip", "curl", "wget",
        "find", "xargs", "tee", "cut", "tr", "wc", "head", "tail",
        "mkdir", "rmdir", "cp", "mv", "rm", "ls", "cat", "echo",
        "export", "source", "alias", "shebang", "#!/bin/bash",
        "case", "select", "getopts", "trap", "signal",
        # C programming / OS concepts
        "fork", "exec", "wait", "pipe", "dup", "dup2",
        "thread", "pthread", "mutex", "semaphore", "deadlock",
        "process", "pid", "getpid", "getppid", "zombie", "orphan",
        "signal", "sighandler", "sigaction", "kill", "raise",
        "shared memory", "shm", "mmap", "ipc", "message queue",
        "socket", "bind", "listen", "accept", "connect",
        "malloc", "calloc", "realloc", "free", "memory",
        "pointer", "struct", "typedef", "header", "include",
        "makefile", "gcc", "compile", "linker", "object file",
        "stdin", "stdout", "stderr", "file descriptor",
        "open", "close", "read", "write", "lseek", "stat",
        "directory", "opendir", "readdir", "closedir",
        "scheduling", "context switch", "race condition",
        "critical section", "producer consumer", "reader writer",
        "dining philosophers", "barrier", "condition variable",
    }

    def validate(self, prompt: str) -> ValidationResult:
        """Validate that a prompt is non-empty and within the character limit.

        Returns a ValidationResult indicating acceptance or rejection with
        an appropriate error message.
        """
        if not prompt or not prompt.strip():
            return ValidationResult(False, "Please enter a valid prompt.")

        length = len(prompt)
        if length > self.MAX_PROMPT_LENGTH:
            return ValidationResult(
                False,
                f"Prompt exceeds the {self.MAX_PROMPT_LENGTH} character limit. "
                f"Your prompt is {length} characters.",
            )

        return ValidationResult(True)

    def build_context(self, prompt: str, session_history: list[dict]) -> str:
        """Combine current prompt with session history into a contextualized string.

        Each history entry is expected to have 'prompt' and 'response' keys.
        """
        parts: list[str] = []
        for exchange in session_history:
            parts.append(f"User: {exchange['prompt']}")
            parts.append(f"Assistant: {exchange['response']}")
        parts.append(f"User: {prompt}")
        return "\n".join(parts)

    def is_coding_request(self, prompt: str) -> bool:
        """Determine if the prompt is interpretable as a coding request.

        Uses a basic keyword heuristic — returns True if any coding-related
        keyword appears in the lowercased prompt.
        """
        lower = prompt.lower()
        return any(kw in lower for kw in self._CODING_KEYWORDS)
