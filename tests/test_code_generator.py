"""Property test for code formatting (Property 3).

Property 3: Code formatting preserves valid Python and applies PEP 8
- For any valid Python code string, format_output produces output that
  is also valid Python (parseable by ast.parse) and conforms to PEP 8
  indentation rules (4-space indents, no tabs).

Validates: Requirements 3.3
"""

import ast
import re

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from src.code_generator import CodeGenerator

generator = CodeGenerator.__new__(CodeGenerator)


# ---------------------------------------------------------------------------
# Strategies for generating valid Python code snippets
# ---------------------------------------------------------------------------

_SIMPLE_STATEMENTS = [
    "x = 1",
    "print('hello')",
    "result = 2 + 3",
    "name = 'world'",
    "values = [1, 2, 3]",
    "data = {'a': 1}",
    "flag = True",
    "count = 0",
]

_FUNCTION_TEMPLATES = [
    "def greet(name):\n    return f'Hello, {name}'",
    "def add(a, b):\n    return a + b",
    "def square(x):\n    return x * x",
    "def is_even(n):\n    return n % 2 == 0",
]

_CLASS_TEMPLATES = [
    "class Dog:\n    def bark(self):\n        return 'woof'",
    "class Counter:\n    def __init__(self):\n        self.count = 0",
]

_LOOP_TEMPLATES = [
    "for i in range(10):\n    print(i)",
    "while True:\n    break",
    "for x in [1, 2, 3]:\n    print(x)",
]

_COMPOUND_TEMPLATES = [
    "if True:\n    pass",
    "try:\n    x = 1\nexcept Exception:\n    pass",
]

_ALL_SNIPPETS = (
    _SIMPLE_STATEMENTS
    + _FUNCTION_TEMPLATES
    + _CLASS_TEMPLATES
    + _LOOP_TEMPLATES
    + _COMPOUND_TEMPLATES
)

valid_python = st.sampled_from(_ALL_SNIPPETS)


# ---------------------------------------------------------------------------
# Property 3: Code formatting preserves valid Python and applies PEP 8
# ---------------------------------------------------------------------------

@given(code=valid_python)
@settings(max_examples=100)
def test_format_output_preserves_valid_python(code: str):
    """format_output of valid Python is still parseable by ast.parse."""
    formatted = generator.format_output(code)
    # Must parse without raising SyntaxError
    ast.parse(formatted)


@given(code=valid_python)
@settings(max_examples=100)
def test_format_output_uses_spaces_not_tabs(code: str):
    """Formatted output uses 4-space indentation, never tabs."""
    formatted = generator.format_output(code)
    assert "\t" not in formatted


@given(code=valid_python)
@settings(max_examples=100)
def test_format_output_no_trailing_whitespace(code: str):
    """No line in the formatted output has trailing whitespace."""
    formatted = generator.format_output(code)
    for line in formatted.splitlines():
        assert line == line.rstrip(), f"Trailing whitespace found: {line!r}"


@given(code=valid_python)
@settings(max_examples=100)
def test_format_output_pep8_indent_multiple_of_four(code: str):
    """All indented lines use a multiple-of-4 space indent."""
    formatted = generator.format_output(code)
    for line in formatted.splitlines():
        if not line.strip():
            continue
        leading = len(line) - len(line.lstrip(" "))
        assert leading % 4 == 0, (
            f"Indent {leading} is not a multiple of 4: {line!r}"
        )


# ---------------------------------------------------------------------------
# Additional: tab-indented input is normalised
# ---------------------------------------------------------------------------

@given(code=valid_python)
@settings(max_examples=100)
def test_format_output_normalises_tabs(code: str):
    """Input with tabs is converted to 4-space indentation."""
    tabbed = code.replace("    ", "\t")
    formatted = generator.format_output(tabbed)
    assert "\t" not in formatted
    ast.parse(formatted)
