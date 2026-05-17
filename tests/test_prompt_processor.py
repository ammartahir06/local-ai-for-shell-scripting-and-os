"""Property tests for prompt processing and validation (Properties 1, 2, 6).

Property 1: Prompt validation correctness
Property 2: Over-limit error message contains limit and actual length
Property 6: Context building includes history and current prompt

Validates: Requirements 2.1, 2.2, 2.3, 2.4, 7.2
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from src.prompt_processor import PromptProcessor

processor = PromptProcessor()


# ---------------------------------------------------------------------------
# Property 1: Prompt validation correctness
# ---------------------------------------------------------------------------

@given(prompt=st.text(min_size=1, max_size=2000).filter(lambda s: s.strip()))
@settings(max_examples=100)
def test_valid_prompts_accepted(prompt: str):
    """Non-empty, non-whitespace strings up to 2000 chars are accepted."""
    result = processor.validate(prompt)
    assert result.is_valid is True
    assert result.error_message is None


@given(prompt=st.text(min_size=0, max_size=100, alphabet=" \t\n\r"))
@settings(max_examples=100)
def test_empty_or_whitespace_rejected(prompt: str):
    """Empty or whitespace-only strings are rejected."""
    result = processor.validate(prompt)
    assert result.is_valid is False
    assert result.error_message == "Please enter a valid prompt."


@given(prompt=st.text(min_size=2001, max_size=5000).filter(lambda s: s.strip()))
@settings(max_examples=100)
def test_over_limit_rejected(prompt: str):
    """Strings exceeding 2000 characters are rejected."""
    result = processor.validate(prompt)
    assert result.is_valid is False
    assert result.error_message is not None


# ---------------------------------------------------------------------------
# Property 2: Over-limit error message contains limit and actual length
# ---------------------------------------------------------------------------

@given(prompt=st.text(min_size=2001, max_size=5000).filter(lambda s: s.strip()))
@settings(max_examples=100)
def test_over_limit_message_contains_limit_and_length(prompt: str):
    """Error message for over-limit prompts contains '2000' and the actual length."""
    result = processor.validate(prompt)
    assert result.is_valid is False
    assert "2000" in result.error_message
    assert str(len(prompt)) in result.error_message


# ---------------------------------------------------------------------------
# Property 6: Context building includes history and current prompt
# ---------------------------------------------------------------------------

_exchange = st.fixed_dictionaries({
    "prompt": st.text(min_size=1, max_size=200).filter(lambda s: s.strip()),
    "response": st.text(min_size=1, max_size=200).filter(lambda s: s.strip()),
})


@given(
    prompt=st.text(min_size=1, max_size=200).filter(lambda s: s.strip()),
    history=st.lists(_exchange, min_size=0, max_size=10),
)
@settings(max_examples=100)
def test_context_contains_history_and_prompt(prompt: str, history: list[dict]):
    """build_context output contains the current prompt and all history text."""
    context = processor.build_context(prompt, history)

    # Current prompt must appear
    assert prompt in context

    # Every historical prompt and response must appear
    for exchange in history:
        assert exchange["prompt"] in context
        assert exchange["response"] in context
