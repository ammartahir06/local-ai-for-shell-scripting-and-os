"""Property-based tests for SessionManager history retention.

Property 5: Session history retention with capacity limit
For any sequence of N prompt-response exchanges added to a session,
get_history SHALL return exactly min(N, 10) entries, and those entries
SHALL be the most recent min(N, 10) exchanges in chronological order.

Validates: Requirements 7.1, 7.3
"""

import tempfile
import os

from hypothesis import given, settings, strategies as st

from src.config import AppConfig
from src.session_manager import SessionManager


def _make_manager():
    """Create a SessionManager backed by a fresh temp directory."""
    tmp = tempfile.mkdtemp()
    config = AppConfig(
        model_filename="test.gguf",
        model_dir="models",
        resource_dir="resources",
        data_dir=os.path.join(tmp, "data"),
        log_dir="logs",
        max_prompt_length=2000,
        max_context_pairs=10,
        response_timeout_seconds=30,
    )
    return SessionManager(config)


# Strategy: list of (prompt, response) pairs, length 1–20
exchange_list = st.lists(
    st.tuples(
        st.text(min_size=1, max_size=100),
        st.text(min_size=1, max_size=100),
    ),
    min_size=1,
    max_size=20,
)


class TestSessionHistoryRetentionProperty:
    """Feature: offline-coding-ai, Property 5: Session history retention with capacity limit"""

    @settings(max_examples=100, deadline=None)
    @given(exchanges=exchange_list)
    def test_history_count_equals_min_n_and_limit(self, exchanges):
        """History length is exactly min(N, 10)."""
        manager = _make_manager()
        sid = manager.new_session()
        for prompt, response in exchanges:
            manager.add_exchange(sid, prompt, response)

        history = manager.get_history(sid)
        expected_count = min(len(exchanges), SessionManager.MAX_CONTEXT_PAIRS)
        assert len(history) == expected_count

    @settings(max_examples=100, deadline=None)
    @given(exchanges=exchange_list)
    def test_history_contains_most_recent_exchanges(self, exchanges):
        """History entries are the most recent min(N, 10) exchanges."""
        manager = _make_manager()
        sid = manager.new_session()
        for prompt, response in exchanges:
            manager.add_exchange(sid, prompt, response)

        history = manager.get_history(sid)
        keep = min(len(exchanges), SessionManager.MAX_CONTEXT_PAIRS)
        expected_tail = exchanges[-keep:]

        for entry, (exp_prompt, exp_response) in zip(history, expected_tail):
            assert entry["prompt"] == exp_prompt
            assert entry["response"] == exp_response

    @settings(max_examples=100, deadline=None)
    @given(exchanges=exchange_list)
    def test_history_is_in_chronological_order(self, exchanges):
        """Returned history preserves insertion (chronological) order."""
        manager = _make_manager()
        sid = manager.new_session()
        for prompt, response in exchanges:
            manager.add_exchange(sid, prompt, response)

        history = manager.get_history(sid)
        keep = min(len(exchanges), SessionManager.MAX_CONTEXT_PAIRS)
        expected_prompts = [p for p, _ in exchanges[-keep:]]
        actual_prompts = [h["prompt"] for h in history]
        assert actual_prompts == expected_prompts
