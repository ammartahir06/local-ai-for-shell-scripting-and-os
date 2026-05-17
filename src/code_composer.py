"""Prompt-driven code composition engine.

Analyzes natural language prompts to extract structural intent and
composes Python code from recognized patterns. Handles a wide range
of common programming tasks including grouping, filtering, mapping,
transforming, and aggregating data.
"""

import re


# ---------------------------------------------------------------------------
# Function name and parameter extraction
# ---------------------------------------------------------------------------

def _extract_function_name(prompt: str) -> str:
    """Derive a snake_case function name from the prompt."""
    lower = prompt.lower()

    # Try explicit: "function called X" or "function named X"
    m = re.search(r"(?:function|def)\s+(?:called|named)\s+([a-z_]\w*)", lower)
    if m:
        return m.group(1)

    # Try explicit: "function X(" or "def X("
    m = re.search(r"(?:function|def)\s+([a-z_]\w*)\s*\(", lower)
    if m:
        return m.group(1)

    # Derive from action words in the prompt
    action_patterns = [
        (r"\b(?:group|grouping)\s+\w+\s+by\b", "group_by"),
        (r"\bcompress\b", "compress_string"),
        (r"\bdecompress\b", "decompress_string"),
        (r"\bprime\b", "is_prime"),
        (r"\bpalindrome\b", "is_palindrome"),
        (r"\banagram\b", "is_anagram"),
        (r"\bcount\s+\w+", "count_items"),
        (r"\bsort\s+\w+", "sort_items"),
        (r"\bfilter\s+\w+", "filter_items"),
        (r"\breverse\s+\w+", "reverse_items"),
        (r"\bflatten\s+\w+", "flatten_list"),
        (r"\bmerge\s+\w+", "merge_items"),
        (r"\bfind\s+\w+", "find_item"),
        (r"\bcheck\s+\w+", "check_item"),
        (r"\bvalidate\s+\w+", "validate_input"),
        (r"\bconvert\s+\w+", "convert_data"),
        (r"\bcalculate\s+\w+", "calculate_result"),
        (r"\bcompute\s+\w+", "compute_result"),
        (r"\bgenerate\s+\w+", "generate_output"),
        (r"\bremove\s+\w+", "remove_items"),
        (r"\btransform\s+\w+", "transform_data"),
        (r"\bmap\s+\w+", "map_items"),
        (r"\btranspose\b", "transpose_matrix"),
        (r"\brotate\b", "rotate_matrix"),
    ]
    for pattern, name in action_patterns:
        if re.search(pattern, lower):
            return name

    return "solution"


def _detect_input_type(prompt: str) -> str:
    """Detect the expected input type from the prompt."""
    lower = prompt.lower()
    if re.search(r"\blist\s+of\s+strings?\b", lower):
        return "list[str]"
    if re.search(r"\blist\s+of\s+(?:int|number|integer)s?\b", lower):
        return "list[int]"
    if re.search(r"\blist\s+of\s+dict(?:ionar(?:y|ies))?\b", lower):
        return "list[dict]"
    if re.search(r"\blist\b", lower):
        return "list"
    if re.search(r"\bstring\b", lower):
        return "str"
    if re.search(r"\bdict(?:ionary)?\b", lower):
        return "dict"
    if re.search(r"\b(?:number|integer|int)\b", lower):
        return "int"
    return "list"


def _detect_output_type(prompt: str) -> str:
    """Detect the expected output type from the prompt."""
    lower = prompt.lower()
    if re.search(r"\breturn\w*\s+(?:a\s+)?dict(?:ionary)?\b", lower):
        return "dict"
    if re.search(r"\bgrouping\b", lower):
        return "dict"
    if re.search(r"\breturn\w*\s+(?:a\s+)?list\b", lower):
        return "list"
    if re.search(r"\breturn\w*\s+(?:a\s+)?(?:bool|true|false)\b", lower):
        return "bool"
    if re.search(r"\breturn\w*\s+(?:a\s+)?(?:string|str)\b", lower):
        return "str"
    if re.search(r"\breturn\w*\s+(?:a\s+)?(?:number|int|count)\b", lower):
        return "int"
    return "auto"


# ---------------------------------------------------------------------------
# Intent detection — what does the user want the code to DO?
# ---------------------------------------------------------------------------

_INTENT_PATTERNS = [
    # Group by some attribute
    ("group_by", r"\bgroup(?:ing)?\s+(?:\w+\s+)*by\s+(?:their\s+)?(\w+)"),
    # Count occurrences
    ("count", r"\bcount\s+(?:the\s+)?(?:number\s+of\s+)?(\w+)"),
    # Filter items
    ("filter", r"\bfilter\s+(?:\w+\s+)?(?:where|that|by|with)\b"),
    ("filter_gt", r"\b(?:greater|more|larger|bigger|above|over)\s+than\s+(\d+)"),
    ("filter_lt", r"\b(?:less|smaller|fewer|below|under)\s+than\s+(\d+)"),
    ("filter_even", r"\beven\s+(?:numbers?|integers?)\b|\bfilter\s+even\b"),
    ("filter_odd", r"\bodd\s+(?:numbers?|integers?)\b|\bfilter\s+odd\b"),
    # Sort
    ("sort_desc", r"\bsort\w*\s+.*\b(?:desc|reverse|descending|largest|highest)\b"),
    ("sort_asc", r"\bsort\w*\b|\border\b|\bascending\b|\balphabetical\b"),
    # Transform / map
    ("uppercase", r"\bupper\s*case\b|\b\.upper\b|\bto\s+upper\b"),
    ("lowercase", r"\blower\s*case\b|\b\.lower\b|\bto\s+lower\b"),
    ("square", r"\bsquare[sd]?\b(?!\s+root)"),
    ("double", r"\bdouble[sd]?\b"),
    ("reverse_str", r"\breverse\s+(?:a\s+)?(?:each\s+)?string"),
    ("reverse_list", r"\breverse\s+(?:a\s+)?(?:the\s+)?list"),
    # Aggregate
    ("sum", r"\bsum\b|\btotal\b"),
    ("average", r"\baverage\b|\bmean\b"),
    ("max", r"\bmax(?:imum)?\b|\blargest\b|\bhighest\b"),
    ("min", r"\bmin(?:imum)?\b|\bsmallest\b|\blowest\b"),
    # Check / validate
    ("palindrome", r"\bpalindrome\b"),
    ("anagram", r"\banagram\b"),
    ("prime", r"\bprime\b"),
    # Flatten
    ("flatten", r"\bflatten\b"),
    # Remove duplicates
    ("unique", r"\bunique\b|\bremove\s+duplicate\b|\bdeduplicate\b|\bdistinct\b"),
    # Intersection / union
    ("intersection", r"\bintersection\b|\bcommon\b"),
    ("union", r"\bunion\b|\bcombine\b"),
    # Zip / pair
    ("zip", r"\bzip\b|\bpair\b|\bcombine\s+two\b"),
    # Frequency / histogram
    ("frequency", r"\bfrequenc(?:y|ies)\b|\bhistogram\b|\boccurrences?\b"),
    # String operations
    ("strip_punct", r"\b(?:strip|remove)\s+(?:\w+\s+)?punctuation\b"),
    ("word_count", r"\bword\s+count\b|\bcount\s+words?\b"),
    ("char_count", r"\bchar(?:acter)?\s+count\b|\bcount\s+char"),
    # String compression / encoding
    ("compress", r"\bcompress\b|\brun[- ]?length\b|\bconsecutive\s+(?:identical\s+)?(?:char|letter|character)"),
    ("decompress", r"\bdecompress\b|\bdecode\b.*\brun[- ]?length\b"),
    # Matrix / 2D operations
    ("transpose", r"\btranspose\b"),
    ("rotate_matrix", r"\brotate\s+(?:a\s+)?matrix\b"),
    # Number operations
    ("digits", r"\bdigits?\b.*\b(?:sum|product|reverse|count)\b|\b(?:sum|reverse)\b.*\bdigits?\b"),
    ("gcd", r"\bgcd\b|\bgreatest\s+common\s+divisor\b"),
    ("lcm", r"\blcm\b|\bleast\s+common\s+multiple\b"),
    ("power", r"\bpower\b|\braise\b.*\bexponent\b"),
    # Conversion
    ("to_binary", r"\b(?:to\s+)?binary\b|\bbase\s*2\b"),
    ("to_roman", r"\broman\s+numeral\b"),
    ("celsius_fahrenheit", r"\bcelsius\b|\bfahrenheit\b|\btemperature\s+convert"),
]


def _detect_intents(prompt: str) -> list[tuple[str, str | None]]:
    """Detect all intents from the prompt. Returns list of (intent, captured_group)."""
    lower = prompt.lower()
    intents = []
    for intent_name, pattern in _INTENT_PATTERNS:
        m = re.search(pattern, lower)
        if m:
            captured = m.group(1) if m.lastindex else None
            intents.append((intent_name, captured))
    return intents


# ---------------------------------------------------------------------------
# Code composition
# ---------------------------------------------------------------------------

def compose_code(prompt: str) -> str | None:
    """Compose Python code from natural language prompt analysis.

    Returns a complete, working Python function, or None if the prompt
    can't be meaningfully decomposed or is asking for shell/C code.
    """
    # Don't compose if the prompt is asking for a known algorithm or data structure
    # — let the retrieval engine handle those
    if _is_algorithm_request(prompt):
        return None

    # Don't compose if the prompt is asking for shell/bash/C code
    # — let the retrieval engine handle those with pre-built snippets
    if _is_non_python_request(prompt):
        return None

    intents = _detect_intents(prompt)
    if not intents:
        return None

    func_name = _extract_function_name(prompt)
    input_type = _detect_input_type(prompt)
    output_type = _detect_output_type(prompt)

    # Determine parameter name based on input type
    param_name = _param_name_for_type(input_type)
    lines: list[str] = []
    indent = "    "

    # Build function signature
    lines.append(f"def {func_name}({param_name}):")

    # Build docstring from prompt
    clean_prompt = prompt.strip().rstrip(".")
    lines.append(f'{indent}"""{clean_prompt}."""')

    # Generate body based on primary intent
    primary_intent = intents[0][0]
    captured = intents[0][1]

    body = _generate_body(primary_intent, captured, intents, param_name,
                          input_type, output_type, indent, prompt)
    lines.extend(body)

    # Add usage example
    lines.append("")
    lines.append("")
    example = _generate_example(func_name, param_name, input_type, prompt)
    lines.extend(example)

    return "\n".join(lines)


# Known algorithm / data structure keywords — if the prompt mentions these,
# defer to snippet retrieval instead of trying to compose from scratch.
_ALGORITHM_KEYWORDS = {
    "merge sort", "quick sort", "heap sort", "insertion sort", "selection sort",
    "counting sort", "bubble sort", "radix sort", "bucket sort",
    "binary search tree", "bst", "linked list", "doubly linked",
    "trie", "prefix tree", "heap", "min heap", "max heap", "priority queue",
    "graph", "bfs", "dfs", "breadth first", "depth first",
    "dijkstra", "topological sort", "shortest path",
    "dynamic programming", "knapsack", "lcs", "longest common subsequence",
    "longest increasing subsequence", "coin change", "edit distance",
    "matrix chain", "backtracking", "n queens", "n-queens",
    "permutation", "combination", "subset", "power set",
    "sliding window", "two pointer",
    "hash map", "hash table",
    # Shell scripting / Bash / Ubuntu topics
    "bash script", "shell script", "for loop bash", "while loop bash",
    "if statement bash", "case statement", "bash function",
    "grep", "awk", "sed", "find command", "xargs",
    "cron job", "crontab", "systemctl", "systemd",
    "apt install", "dpkg", "package manager",
    "ssh", "scp", "rsync", "tar", "curl", "wget",
    "chmod", "chown", "file permission", "umask",
    "pipe", "redirect", "stdin", "stdout", "stderr",
    "process management", "background process", "daemon",
    "disk usage", "disk space", "du", "df",
    "user management", "useradd", "usermod", "passwd",
    "network configuration", "ip address", "ifconfig",
    "firewall", "ufw", "iptables",
    "log rotation", "journalctl", "syslog",
    # C / OS concepts
    "fork", "exec", "wait", "waitpid", "execvp",
    "pthread", "thread", "mutex", "semaphore",
    "producer consumer", "reader writer", "dining philosophers",
    "deadlock", "race condition", "critical section",
    "shared memory", "message queue", "ipc",
    "signal handling", "sigaction", "signal handler",
    "socket programming", "tcp server", "udp server",
    "pipe in c", "named pipe", "fifo",
    "zombie process", "orphan process",
    "memory allocation", "malloc", "calloc",
    "file descriptor", "open close read write",
    "makefile", "gcc compilation",
    "context switch", "process scheduling",
    "condition variable", "barrier", "spinlock",
}


def _is_algorithm_request(prompt: str) -> bool:
    """Check if the prompt is asking for a known algorithm or data structure."""
    lower = prompt.lower()
    return any(kw in lower for kw in _ALGORITHM_KEYWORDS)


# Shell/Bash/C indicators — if the prompt mentions these, defer to retrieval.
_NON_PYTHON_INDICATORS = {
    "bash", "shell", "script", "ubuntu", "linux", "terminal",
    "chmod", "chown", "grep", "awk", "sed", "apt", "systemctl",
    "cron", "crontab", "ssh", "scp", "rsync", "tar", "curl", "wget",
    "find command", "xargs", "pipe", "redirect", "daemon", "nohup",
    "ufw", "iptables", "getopts", "shebang", "#!/bin/bash",
    "fork", "exec", "pthread", "mutex", "semaphore", "malloc",
    "calloc", "free", "struct", "typedef", "#include", "gcc",
    "makefile", "socket", "bind", "listen", "accept", "connect",
    "sigaction", "signal handler", "mmap", "shared memory",
    "fifo", "dup2", "waitpid", "zombie", "orphan", "deadlock",
    "spinlock", "barrier", "condition variable", "thread",
    "wc", "cut", "mv", "mkdir", "echo", "test",
    "subdirectory", "subdirectories", ".txt files",
    "word count", "file processing", "batch",
    # Shell function/math patterns
    "shell script", "bash script", "bash function",
    "sum_of_digits", "sum of digits", "multiplication_table",
    "multiplication table", "read -p", "read input",
    "prompts the user", "enter a number",
    "digits", "modulo", "arithmetic",
    "factorial", "fibonacci", "prime",
    "even odd", "reverse digits", "palindrome number",
    "calculator", "menu", "case statement",
}


def _is_non_python_request(prompt: str) -> bool:
    """Check if the prompt is asking for shell/bash/C code."""
    lower = prompt.lower()
    return any(kw in lower for kw in _NON_PYTHON_INDICATORS)


def _param_name_for_type(input_type: str) -> str:
    """Choose a descriptive parameter name based on input type."""
    type_map = {
        "list[str]": "strings",
        "list[int]": "numbers",
        "list[dict]": "items",
        "list": "items",
        "str": "text",
        "dict": "data",
        "int": "n",
    }
    return type_map.get(input_type, "data")


def _generate_body(intent: str, captured: str | None, all_intents: list,
                    param: str, in_type: str, out_type: str,
                    indent: str, prompt: str) -> list[str]:
    """Generate the function body based on the primary intent."""
    lines: list[str] = []

    if intent == "group_by":
        group_key = captured or "length"
        lines.extend(_body_group_by(param, group_key, in_type, indent, prompt))

    elif intent == "frequency":
        lines.extend(_body_frequency(param, in_type, indent))

    elif intent in ("filter", "filter_gt", "filter_lt", "filter_even", "filter_odd"):
        lines.extend(_body_filter(param, intent, captured, in_type, indent))

    elif intent in ("sort_asc", "sort_desc"):
        desc = intent == "sort_desc"
        lines.extend(_body_sort(param, desc, in_type, indent, prompt))

    elif intent in ("uppercase", "lowercase"):
        case = "upper" if intent == "uppercase" else "lower"
        lines.append(f"{indent}return [{param[:-1]}.{case}() for {param[:-1]} in {param}]")

    elif intent == "square":
        lines.append(f"{indent}return [x ** 2 for x in {param}]")

    elif intent == "double":
        lines.append(f"{indent}return [x * 2 for x in {param}]")

    elif intent == "reverse_str":
        lines.append(f"{indent}return [s[::-1] for s in {param}]")

    elif intent == "reverse_list":
        lines.append(f"{indent}return {param}[::-1]")

    elif intent == "sum":
        lines.append(f"{indent}return sum({param})")

    elif intent == "average":
        lines.append(f"{indent}if not {param}:")
        lines.append(f"{indent}    return 0")
        lines.append(f"{indent}return sum({param}) / len({param})")

    elif intent == "max":
        lines.append(f"{indent}if not {param}:")
        lines.append(f"{indent}    return None")
        lines.append(f"{indent}return max({param})")

    elif intent == "min":
        lines.append(f"{indent}if not {param}:")
        lines.append(f"{indent}    return None")
        lines.append(f"{indent}return min({param})")

    elif intent == "palindrome":
        lines.append(f"{indent}cleaned = ''.join(c.lower() for c in {param} if c.isalnum())")
        lines.append(f"{indent}return cleaned == cleaned[::-1]")

    elif intent == "anagram":
        lines.append(f"{indent}# Check if two strings are anagrams")
        lines.append(f"{indent}if len({param}) != 2:")
        lines.append(f'{indent}    raise ValueError("Need exactly 2 strings")')
        lines.append(f"{indent}a = sorted({param}[0].lower().replace(' ', ''))")
        lines.append(f"{indent}b = sorted({param}[1].lower().replace(' ', ''))")
        lines.append(f"{indent}return a == b")

    elif intent == "prime":
        lines.append(f"{indent}if {param} < 2:")
        lines.append(f"{indent}    return False")
        lines.append(f"{indent}for i in range(2, int({param} ** 0.5) + 1):")
        lines.append(f"{indent}    if {param} % i == 0:")
        lines.append(f"{indent}        return False")
        lines.append(f"{indent}return True")

    elif intent == "flatten":
        lines.append(f"{indent}result = []")
        lines.append(f"{indent}for item in {param}:")
        lines.append(f"{indent}    if isinstance(item, list):")
        lines.append(f"{indent}        result.extend({_current_func_name()}(item))")
        lines.append(f"{indent}    else:")
        lines.append(f"{indent}        result.append(item)")
        lines.append(f"{indent}return result")

    elif intent == "unique":
        lines.append(f"{indent}seen = set()")
        lines.append(f"{indent}result = []")
        lines.append(f"{indent}for item in {param}:")
        lines.append(f"{indent}    if item not in seen:")
        lines.append(f"{indent}        seen.add(item)")
        lines.append(f"{indent}        result.append(item)")
        lines.append(f"{indent}return result")

    elif intent == "intersection":
        lines.append(f"{indent}if len({param}) < 2:")
        lines.append(f"{indent}    return {param}")
        lines.append(f"{indent}result = set({param}[0])")
        lines.append(f"{indent}for lst in {param}[1:]:")
        lines.append(f"{indent}    result &= set(lst)")
        lines.append(f"{indent}return sorted(result)")

    elif intent == "word_count":
        lines.append(f"{indent}return len({param}.split())")

    elif intent == "char_count":
        lines.append(f"{indent}return len({param})")

    elif intent == "strip_punct":
        lines.append(f"{indent}import string")
        lines.append(f"{indent}return {param}.translate(str.maketrans('', '', string.punctuation))")

    elif intent == "compress":
        lines.extend(_body_compress(param, indent))

    elif intent == "decompress":
        lines.extend(_body_decompress(param, indent))

    elif intent == "transpose":
        lines.append(f"{indent}if not {param}:")
        lines.append(f"{indent}    return []")
        lines.append(f"{indent}return [list(row) for row in zip(*{param})]")

    elif intent == "rotate_matrix":
        lines.append(f"{indent}# Rotate 90 degrees clockwise")
        lines.append(f"{indent}n = len({param})")
        lines.append(f"{indent}return [[{param}[n - 1 - j][i] for j in range(n)] for i in range(n)]")

    elif intent == "digits":
        lines.append(f"{indent}return sum(int(d) for d in str(abs({param})))")

    elif intent == "gcd":
        lines.append(f"{indent}a, b = abs({param}[0]), abs({param}[1])")
        lines.append(f"{indent}while b:")
        lines.append(f"{indent}    a, b = b, a % b")
        lines.append(f"{indent}return a")

    elif intent == "lcm":
        lines.append(f"{indent}def gcd(a, b):")
        lines.append(f"{indent}    while b:")
        lines.append(f"{indent}        a, b = b, a % b")
        lines.append(f"{indent}    return a")
        lines.append(f"{indent}a, b = abs({param}[0]), abs({param}[1])")
        lines.append(f"{indent}return a * b // gcd(a, b)")

    elif intent == "to_binary":
        lines.append(f"{indent}if {param} == 0:")
        lines.append(f'{indent}    return "0"')
        lines.append(f"{indent}result = []")
        lines.append(f"{indent}n = abs({param})")
        lines.append(f"{indent}while n > 0:")
        lines.append(f"{indent}    result.append(str(n % 2))")
        lines.append(f"{indent}    n //= 2")
        lines.append(f'{indent}prefix = "-" if {param} < 0 else ""')
        lines.append(f'{indent}return prefix + "".join(reversed(result))')

    elif intent == "to_roman":
        lines.extend(_body_to_roman(param, indent))

    elif intent == "celsius_fahrenheit":
        lines.append(f"{indent}# Celsius to Fahrenheit")
        lines.append(f"{indent}return ({param} * 9 / 5) + 32")

    else:
        lines.append(f"{indent}pass  # TODO: implement")

    return lines


def _current_func_name() -> str:
    """Helper to reference the current function for recursion."""
    return "flatten_list"


def _body_compress(param: str, indent: str) -> list[str]:
    """Generate body for string compression (run-length encoding)."""
    lines = []
    lines.append(f"{indent}if not {param}:")
    lines.append(f'{indent}    return ""')
    lines.append(f"{indent}result = []")
    lines.append(f"{indent}count = 1")
    lines.append(f"{indent}for i in range(1, len({param})):")
    lines.append(f"{indent}    if {param}[i] == {param}[i - 1]:")
    lines.append(f"{indent}        count += 1")
    lines.append(f"{indent}    else:")
    lines.append(f"{indent}        result.append({param}[i - 1] + str(count))")
    lines.append(f"{indent}        count = 1")
    lines.append(f"{indent}result.append({param}[-1] + str(count))")
    lines.append(f'{indent}return "".join(result)')
    return lines


def _body_decompress(param: str, indent: str) -> list[str]:
    """Generate body for string decompression (run-length decoding)."""
    lines = []
    lines.append(f"{indent}result = []")
    lines.append(f"{indent}i = 0")
    lines.append(f"{indent}while i < len({param}):")
    lines.append(f"{indent}    char = {param}[i]")
    lines.append(f"{indent}    i += 1")
    lines.append(f"{indent}    num = []")
    lines.append(f"{indent}    while i < len({param}) and {param}[i].isdigit():")
    lines.append(f"{indent}        num.append({param}[i])")
    lines.append(f"{indent}        i += 1")
    lines.append(f'{indent}    count = int("".join(num)) if num else 1')
    lines.append(f"{indent}    result.append(char * count)")
    lines.append(f'{indent}return "".join(result)')
    return lines


def _body_to_roman(param: str, indent: str) -> list[str]:
    """Generate body for integer to Roman numeral conversion."""
    lines = []
    lines.append(f"{indent}val_map = [")
    lines.append(f'{indent}    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),')
    lines.append(f'{indent}    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),')
    lines.append(f'{indent}    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),')
    lines.append(f"{indent}]")
    lines.append(f"{indent}result = []")
    lines.append(f"{indent}for value, numeral in val_map:")
    lines.append(f"{indent}    while {param} >= value:")
    lines.append(f"{indent}        result.append(numeral)")
    lines.append(f"{indent}        {param} -= value")
    lines.append(f'{indent}return "".join(result)')
    return lines


def _body_group_by(param: str, key: str, in_type: str, indent: str, prompt: str) -> list[str]:
    """Generate body for group-by operations."""
    lines = []
    lines.append(f"{indent}result = {{}}")

    # Determine what to group by
    lower = prompt.lower()
    if "length" in lower or "len" in lower:
        lines.append(f"{indent}for item in {param}:")
        lines.append(f"{indent}    key = len(item)")
        lines.append(f"{indent}    if key not in result:")
        lines.append(f"{indent}        result[key] = []")
        lines.append(f"{indent}    result[key].append(item)")
    elif "first" in lower and ("letter" in lower or "char" in lower):
        lines.append(f"{indent}for item in {param}:")
        lines.append(f"{indent}    key = item[0] if item else ''")
        lines.append(f"{indent}    if key not in result:")
        lines.append(f"{indent}        result[key] = []")
        lines.append(f"{indent}    result[key].append(item)")
    elif "last" in lower and ("letter" in lower or "char" in lower):
        lines.append(f"{indent}for item in {param}:")
        lines.append(f"{indent}    key = item[-1] if item else ''")
        lines.append(f"{indent}    if key not in result:")
        lines.append(f"{indent}        result[key] = []")
        lines.append(f"{indent}    result[key].append(item)")
    elif "even" in lower or "odd" in lower:
        lines.append(f"{indent}for item in {param}:")
        lines.append(f'{indent}    key = "even" if item % 2 == 0 else "odd"')
        lines.append(f"{indent}    if key not in result:")
        lines.append(f"{indent}        result[key] = []")
        lines.append(f"{indent}    result[key].append(item)")
    elif "type" in lower:
        lines.append(f"{indent}for item in {param}:")
        lines.append(f"{indent}    key = type(item).__name__")
        lines.append(f"{indent}    if key not in result:")
        lines.append(f"{indent}        result[key] = []")
        lines.append(f"{indent}    result[key].append(item)")
    else:
        # Generic group by attribute
        lines.append(f"{indent}for item in {param}:")
        if in_type == "list[dict]":
            lines.append(f'{indent}    key = item.get("{key}", None)')
        else:
            lines.append(f"{indent}    key = len(item)")
        lines.append(f"{indent}    if key not in result:")
        lines.append(f"{indent}        result[key] = []")
        lines.append(f"{indent}    result[key].append(item)")

    lines.append(f"{indent}return result")
    return lines


def _body_frequency(param: str, in_type: str, indent: str) -> list[str]:
    """Generate body for frequency counting."""
    lines = []
    lines.append(f"{indent}freq = {{}}")
    lines.append(f"{indent}for item in {param}:")
    lines.append(f"{indent}    freq[item] = freq.get(item, 0) + 1")
    lines.append(f"{indent}return freq")
    return lines


def _body_filter(param: str, intent: str, captured: str | None,
                 in_type: str, indent: str) -> list[str]:
    """Generate body for filter operations."""
    lines = []
    if intent == "filter_gt" and captured:
        lines.append(f"{indent}return [x for x in {param} if x > {captured}]")
    elif intent == "filter_lt" and captured:
        lines.append(f"{indent}return [x for x in {param} if x < {captured}]")
    elif intent == "filter_even":
        lines.append(f"{indent}return [x for x in {param} if x % 2 == 0]")
    elif intent == "filter_odd":
        lines.append(f"{indent}return [x for x in {param} if x % 2 != 0]")
    else:
        lines.append(f"{indent}# TODO: specify filter condition")
        lines.append(f"{indent}return [x for x in {param} if x]")
    return lines


def _body_sort(param: str, desc: bool, in_type: str, indent: str, prompt: str) -> list[str]:
    """Generate body for sort operations."""
    lines = []
    lower = prompt.lower()

    if "length" in lower or "len" in lower:
        lines.append(f"{indent}return sorted({param}, key=len, reverse={desc})")
    elif "alphabetical" in lower or "alpha" in lower:
        lines.append(f"{indent}return sorted({param}, reverse={desc})")
    else:
        lines.append(f"{indent}return sorted({param}, reverse={desc})")
    return lines


# ---------------------------------------------------------------------------
# Usage example generation
# ---------------------------------------------------------------------------

def _generate_example(func_name: str, param: str, in_type: str, prompt: str) -> list[str]:
    """Generate a usage example for the composed function."""
    lines = ["# Example usage"]

    if in_type == "list[str]":
        lines.append(f'result = {func_name}(["hello", "hi", "world", "hey", "python", "go"])')
    elif in_type == "list[int]":
        lines.append(f"result = {func_name}([3, 1, 4, 1, 5, 9, 2, 6])")
    elif in_type == "str":
        lower = prompt.lower()
        if "compress" in lower or "consecutive" in lower:
            lines.append(f'result = {func_name}("AAABBBCCDDDD")')
        elif "decompress" in lower:
            lines.append(f'result = {func_name}("A3B3C2D4")')
        elif "palindrome" in lower:
            lines.append(f'result = {func_name}("A man, a plan, a canal: Panama")')
        else:
            lines.append(f'result = {func_name}("Hello, World!")')
    elif in_type == "int":
        lines.append(f"result = {func_name}(42)")
    else:
        lines.append(f'result = {func_name}(["apple", "banana", "cherry"])')

    lines.append("print(result)")
    return lines
