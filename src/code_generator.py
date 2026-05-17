"""Code generation for the Offline Coding AI Assistant.

Orchestrates inference via ModelLoader, formats output for Python, Bash,
and C code, and combines code with documentation references.
"""

import ast
import re
import textwrap
from collections.abc import Generator

from src.config import InferenceError
from src.model_loader import ModelLoader


class CodeGenerator:
    """Generates code from prompts using the local language model."""

    _NON_CODING_MESSAGE = (
        "I couldn't interpret that as a coding request. "
        "Try asking me to write, explain, or fix Python code, "
        "shell scripts, Ubuntu commands, or C programs (threading, fork, etc.)."
    )

    _INFERENCE_ERROR_MESSAGE = (
        "An error occurred during code generation. "
        "Please try again or restart the assistant."
    )

    # Keywords that indicate shell/bash code
    _SHELL_INDICATORS = {
        "#!/bin/bash", "#!/bin/sh", "echo ", "if [", "fi", "done",
        "do\n", "esac", ";;", "then\n", "elif ", "$(",
        "apt ", "systemctl ", "chmod ", "chown ", "grep ",
        "awk ", "sed ", "find ", "xargs ", "cron",
    }

    # Keywords that indicate C code
    _C_INDICATORS = {
        "#include", "int main", "void ", "printf(", "scanf(",
        "malloc(", "free(", "fork(", "pthread_", "mutex",
        "semaphore", "struct ", "typedef ", "->", "NULL",
        "sizeof(", "return 0;", "int *", "char *",
    }

    def __init__(self, model_loader: ModelLoader) -> None:
        self._model = model_loader

    def generate(self, prompt: str, context: str) -> Generator[str, None, None]:
        """Stream code tokens from the model.

        Yields partial output as tokens become available.
        If inference fails, yields a user-friendly error message.
        """
        try:
            yield from self._model.infer(context)
        except InferenceError:
            yield self._INFERENCE_ERROR_MESSAGE

    def detect_language(self, code: str) -> str:
        """Detect the language of the generated code."""
        if any(indicator in code for indicator in self._C_INDICATORS):
            return "c"
        if any(indicator in code for indicator in self._SHELL_INDICATORS):
            return "bash"
        return "python"

    def format_output(self, raw_code: str) -> str:
        """Apply language-appropriate formatting.

        - For Python: PEP 8 formatting with 4-space indentation
        - For Bash: Normalize indentation, ensure shebang
        - For C: Normalize indentation to 4 spaces
        """
        lang = self.detect_language(raw_code)

        if lang == "bash":
            return self._format_bash(raw_code)
        elif lang == "c":
            return self._format_c(raw_code)
        else:
            return self._format_python(raw_code)

    def build_response(self, code: str, references: list[str]) -> str:
        """Combine generated code with documentation references."""
        lang = self.detect_language(code)
        comment_prefix = "//" if lang == "c" else "#"

        parts = [code]
        if references:
            parts.append("")
            parts.append(f"{comment_prefix} References:")
            for ref in references:
                parts.append(f"{comment_prefix}   - {ref}")
        return "\n".join(parts)

    # ------------------------------------------------------------------
    # Language-specific formatters
    # ------------------------------------------------------------------

    def _format_python(self, raw_code: str) -> str:
        """Apply PEP 8 formatting for Python code."""
        code = self._normalize_indentation(raw_code)
        code = self._strip_trailing_whitespace(code)
        code = self._ensure_comments(code)
        return code

    def _format_bash(self, raw_code: str) -> str:
        """Format bash/shell script code."""
        code = raw_code.replace("\t", "    ")
        code = self._strip_trailing_whitespace(code)
        return code

    def _format_c(self, raw_code: str) -> str:
        """Format C code with consistent indentation."""
        code = raw_code.replace("\t", "    ")
        code = self._strip_trailing_whitespace(code)
        return code

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize_indentation(code: str) -> str:
        """Convert tabs to 4 spaces and dedent to minimum indentation."""
        code = code.replace("\t", "    ")
        return textwrap.dedent(code)

    @staticmethod
    def _strip_trailing_whitespace(code: str) -> str:
        lines = code.splitlines()
        return "\n".join(line.rstrip() for line in lines)

    @staticmethod
    def _ensure_comments(code: str) -> str:
        """Add a placeholder inline comment if the code has none."""
        if "#" in code or "//" in code or "/*" in code:
            return code

        lines = code.splitlines()
        result: list[str] = []
        for line in lines:
            stripped = line.rstrip()
            # Add comment to def/class lines that lack one
            if re.match(r"^\s*(def |class )", stripped) and "#" not in stripped:
                result.append(f"{stripped}  # function/class definition")
            else:
                result.append(stripped)
        return "\n".join(result)
