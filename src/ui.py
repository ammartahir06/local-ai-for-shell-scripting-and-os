"""Terminal-based user interface for the Offline Coding AI Assistant.

Uses the Rich library for styled terminal output including syntax-highlighted
code blocks, spinners, and formatted error messages. Provides clipboard
support via pyperclip.
"""

from collections.abc import Generator

try:
    import pyperclip
except ImportError:
    pyperclip = None  # type: ignore[assignment]

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text


class UserInterface:
    """Text-based terminal UI powered by Rich."""

    def __init__(self) -> None:
        self._console = Console()
        self._last_code: str = ""

    def start_session(
        self,
        *,
        on_prompt: "callable[[str], Generator[str, None, None] | str] | None" = None,
    ) -> None:
        """Launch the terminal UI and enter the input loop.

        ``on_prompt`` is a callback that receives the validated user prompt
        and returns either a string response or a generator that yields
        streamed tokens.  If *None*, the loop just echoes prompts back
        (useful for testing the UI in isolation).
        """
        self.display_welcome()

        while True:
            prompt = self.get_prompt()
            if prompt is None:
                # EOF / Ctrl-D
                self._console.print("\n[dim]Goodbye![/dim]")
                break

            stripped = prompt.strip()
            if stripped.lower() in {"exit", "quit", ":q"}:
                self._console.print("[dim]Goodbye![/dim]")
                break

            if stripped.lower() == "copy":
                self.copy_to_clipboard(self._last_code)
                continue

            if on_prompt is None:
                self._console.print(f"[dim]Echo:[/dim] {prompt}")
                continue

            result = on_prompt(stripped)

            # Handle streamed or plain string responses
            if isinstance(result, str):
                self.display_output(result)
            else:
                self._stream_output(result)

    def display_welcome(self) -> None:
        """Show a welcome message with brief usage instructions."""
        welcome = Text.assemble(
            ("Offline Coding AI Assistant\n", "bold cyan"),
            ("Type a coding question in plain English and press Enter.\n\n", ""),
            ("Commands:\n", "bold"),
            ("  exit / quit  ", "green"),
            ("– end the session\n", "dim"),
            ("  copy         ", "green"),
            ("– copy the last code output to clipboard\n", "dim"),
        )
        self._console.print(Panel(welcome, border_style="cyan", expand=False))

    def get_prompt(self) -> str | None:
        """Read user input from the terminal.

        Returns *None* on EOF (Ctrl-D / Ctrl-Z).
        """
        try:
            return self._console.input("[bold green]>>> [/bold green]")
        except EOFError:
            return None

    def display_output(self, code: str, references: list[str] | None = None) -> None:
        """Render code in a syntax-highlighted panel with optional references."""
        self._last_code = code
        syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
        self._console.print(Panel(syntax, title="Generated Code", border_style="green"))

        if references:
            ref_text = "\n".join(f"  • {r}" for r in references)
            self._console.print(
                Panel(ref_text, title="References", border_style="blue")
            )

    def display_loading(self) -> "rich.status.Status":
        """Return a Rich Status context manager that shows a spinner.

        Usage::

            with ui.display_loading():
                # long-running work
        """
        return self._console.status("[cyan]Generating...[/cyan]", spinner="dots")

    def display_error(self, message: str) -> None:
        """Display an error message in a styled panel."""
        self._console.print(
            Panel(f"[bold red]Error:[/bold red] {message}", border_style="red")
        )

    def copy_to_clipboard(self, text: str) -> None:
        """Copy *text* to the system clipboard via pyperclip."""
        if not text:
            self._console.print("[dim]Nothing to copy.[/dim]")
            return
        if pyperclip is None:
            self.display_error("Clipboard not available: pyperclip is not installed.")
            return
        try:
            pyperclip.copy(text)
            self._console.print("[green]Copied to clipboard.[/green]")
        except pyperclip.PyperclipException as exc:
            self.display_error(f"Clipboard not available: {exc}")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _stream_output(self, token_gen: Generator[str, None, None]) -> None:
        """Consume a token generator, printing tokens as they arrive,
        then display the final result in a formatted panel."""
        self._console.print()
        tokens: list[str] = []
        with self._console.status("[cyan]Generating...[/cyan]", spinner="dots"):
            for token in token_gen:
                tokens.append(token)

        full_output = "".join(tokens)
        self.display_output(full_output)
