"""Unit tests for SessionManager.

Tests cover session creation, exchange storage with eviction,
history retrieval, and session clearing.
"""

import os
import tempfile
import uuid

import pytest

from src.config import AppConfig
from src.session_manager import Exchange, SessionData, SessionManager


@pytest.fixture
def config(tmp_path):
    """Create an AppConfig pointing to a temporary data directory."""
    return AppConfig(
        model_filename="test.gguf",
        model_dir="models",
        resource_dir="resources",
        data_dir=str(tmp_path / "data"),
        log_dir="logs",
        max_prompt_length=2000,
        max_context_pairs=10,
        response_timeout_seconds=30,
    )


@pytest.fixture
def manager(config):
    """Create a SessionManager with a temp database."""
    return SessionManager(config)


class TestNewSession:
    def test_returns_valid_uuid(self, manager):
        session_id = manager.new_session()
        uuid.UUID(session_id)  # raises if invalid

    def test_each_session_is_unique(self, manager):
        ids = {manager.new_session() for _ in range(5)}
        assert len(ids) == 5


class TestGetHistory:
    def test_new_session_has_empty_history(self, manager):
        sid = manager.new_session()
        assert manager.get_history(sid) == []

    def test_returns_exchanges_in_chronological_order(self, manager):
        sid = manager.new_session()
        for i in range(3):
            manager.add_exchange(sid, f"prompt_{i}", f"response_{i}")
        history = manager.get_history(sid)
        assert len(history) == 3
        assert history[0]["prompt"] == "prompt_0"
        assert history[2]["prompt"] == "prompt_2"

    def test_returns_at_most_10_exchanges(self, manager):
        sid = manager.new_session()
        for i in range(15):
            manager.add_exchange(sid, f"p{i}", f"r{i}")
        history = manager.get_history(sid)
        assert len(history) == 10
        # Should be the 10 most recent
        assert history[0]["prompt"] == "p5"
        assert history[-1]["prompt"] == "p14"


class TestAddExchange:
    def test_stores_prompt_and_response(self, manager):
        sid = manager.new_session()
        manager.add_exchange(sid, "hello", "world")
        history = manager.get_history(sid)
        assert len(history) == 1
        assert history[0]["prompt"] == "hello"
        assert history[0]["response"] == "world"

    def test_evicts_oldest_when_exceeding_limit(self, manager):
        sid = manager.new_session()
        for i in range(12):
            manager.add_exchange(sid, f"p{i}", f"r{i}")
        history = manager.get_history(sid)
        assert len(history) == 10
        # Oldest two (p0, p1) should be evicted
        prompts = [h["prompt"] for h in history]
        assert "p0" not in prompts
        assert "p1" not in prompts
        assert prompts[0] == "p2"


class TestClearSession:
    def test_removes_all_exchanges(self, manager):
        sid = manager.new_session()
        for i in range(5):
            manager.add_exchange(sid, f"p{i}", f"r{i}")
        manager.clear_session(sid)
        assert manager.get_history(sid) == []

    def test_does_not_affect_other_sessions(self, manager):
        sid1 = manager.new_session()
        sid2 = manager.new_session()
        manager.add_exchange(sid1, "p1", "r1")
        manager.add_exchange(sid2, "p2", "r2")
        manager.clear_session(sid1)
        assert manager.get_history(sid1) == []
        assert len(manager.get_history(sid2)) == 1


class TestDataclasses:
    def test_exchange_fields(self):
        from datetime import datetime, timezone

        ts = datetime.now(timezone.utc)
        ex = Exchange(prompt="hi", response="hello", timestamp=ts)
        assert ex.prompt == "hi"
        assert ex.response == "hello"
        assert ex.timestamp == ts

    def test_session_data_defaults(self):
        sd = SessionData(session_id="abc")
        assert sd.session_id == "abc"
        assert sd.history == []
        assert sd.created_at is not None


class TestDatabaseCreation:
    def test_auto_creates_data_directory(self, tmp_path):
        data_dir = str(tmp_path / "nonexistent" / "nested")
        config = AppConfig(
            model_filename="test.gguf",
            model_dir="models",
            resource_dir="resources",
            data_dir=data_dir,
            log_dir="logs",
            max_prompt_length=2000,
            max_context_pairs=10,
            response_timeout_seconds=30,
        )
        manager = SessionManager(config)
        sid = manager.new_session()
        assert sid  # session created successfully
        assert os.path.isdir(data_dir)
