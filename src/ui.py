"""Terminal-based user interface for the Offline Coding AI Assistant.

Simple terminal output with plain code display.
Provides clipboard support via pyperclip.
"""

from collections.abc import Generator

try:
    import pyperclip
except ImportError:
    pyperclip = None  # type: ignore[assignment]


class UserInterface:
    """Simple text-based terminal UI."""

    def __init__(self) -> None:
        self._last_code: str = ""

    def start_session(
        self,
        *,
        on_prompt: "callable[[str], Generator[str, None, None] | str] | None" = None,
    ) -> None:
        """Launch the terminal UI and enter the input loop."""
        self.display_welcome()

        while True:
            prompt = self.get_prompt()
            if prompt is None:
                print("\nGoodbye!")
                break

            stripped = prompt.strip()
            if stripped.lower() in {"exit", "quit", ":q"}:
                print("Goodbye!")
                break

            if stripped.lower() == "copy":
                self.copy_to_clipboard(self._last_code)
                continue

            if on_prompt is None:
                print(f"Echo: {prompt}")
                continue

            result = on_prompt(stripped)

            if isinstance(result, str):
                self.display_output(result)
            else:
                self._stream_output(result)

    def display_welcome(self) -> None:
        """Show a welcome message with brief usage instructions."""
        print()
        print("=" * 50)
        print("  Offline Coding AI Assistant")
        print("=" * 50)
        print()
        print("  Type a coding question and press Enter.")
        print("  Supports: Python, Bash/Shell, C/OS concepts")
        print()
        print("  Commands:")
        print("    exit / quit  - end the session")
        print("    copy         - copy last output to clipboard")
        print()

    def get_prompt(self) -> str | None:
        """Read user input from the terminal."""
        try:
            return input(">>> ")
        except (EOFError, KeyboardInterrupt):
            return None

    def display_output(self, code: str, references: list[str] | None = None) -> None:
        """Print code output plainly without borders or panels."""
        self._last_code = code
        print()
        print(code)
        print()

    def display_loading(self):
        """Return a no-op context manager (no spinner)."""
        class _NoOp:
            def __enter__(self): return self
            def __exit__(self, *a): pass
        return _NoOp()

    def display_error(self, message: str) -> None:
        """Display an error message."""
        print(f"[ERROR] {message}")

    def copy_to_clipboard(self, text: str) -> None:
        """Copy text to the system clipboard via pyperclip."""
        if not text:
            print("Nothing to copy.")
            return
        if pyperclip is None:
            print("[ERROR] Clipboard not available: pyperclip is not installed.")
            return
        try:
            pyperclip.copy(text)
            print("Copied to clipboard.")
        except Exception as exc:
            print(f"[ERROR] Clipboard not available: {exc}")

    def _stream_output(self, token_gen: Generator[str, None, None]) -> None:
        """Consume a token generator and display the result."""
        tokens: list[str] = []
        for token in token_gen:
            tokens.append(token)
        full_output = "".join(tokens)
        self.display_output(full_output)
