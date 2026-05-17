"""Session management with SQLite storage.

Manages conversation context within sessions, storing prompt-response
exchanges in a SQLite database at <project_root>/data/sessions.db.
"""

import os
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from src.config import AppConfig


@dataclass
class Exchange:
    """A single prompt-response pair within a session."""

    prompt: str
    response: str
    timestamp: datetime


@dataclass
class SessionData:
    """Full session state including history."""

    session_id: str
    history: list[Exchange] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class SessionManager:
    """Manages conversation sessions backed by SQLite storage."""

    MAX_CONTEXT_PAIRS: int = 10

    def __init__(self, config: AppConfig) -> None:
        """Initialize the session manager and ensure the database exists.

        Creates the data directory and SQLite database if they don't exist.
        """
        self._db_path = config.database_path
        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Return a new connection to the SQLite database."""
        conn = sqlite3.connect(self._db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _init_db(self) -> None:
        """Create the sessions and exchanges tables if they don't exist."""
        conn = self._get_connection()
        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS exchanges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    response TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
                """
            )
            conn.commit()
        finally:
            conn.close()

    def new_session(self) -> str:
        """Create a new session with empty context. Returns a UUID session ID."""
        session_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc).isoformat()
        conn = self._get_connection()
        try:
            conn.execute(
                "INSERT INTO sessions (session_id, created_at) VALUES (?, ?)",
                (session_id, created_at),
            )
            conn.commit()
        finally:
            conn.close()
        return session_id

    def add_exchange(self, session_id: str, prompt: str, response: str) -> None:
        """Store a prompt-response pair, evicting the oldest if at MAX_CONTEXT_PAIRS."""
        timestamp = datetime.now(timezone.utc).isoformat()
        conn = self._get_connection()
        try:
            conn.execute(
                "INSERT INTO exchanges (session_id, prompt, response, timestamp) VALUES (?, ?, ?, ?)",
                (session_id, prompt, response, timestamp),
            )
            # Evict oldest exchanges if we exceed the limit
            conn.execute(
                """
                DELETE FROM exchanges
                WHERE id NOT IN (
                    SELECT id FROM exchanges
                    WHERE session_id = ?
                    ORDER BY id DESC
                    LIMIT ?
                ) AND session_id = ?
                """,
                (session_id, self.MAX_CONTEXT_PAIRS, session_id),
            )
            conn.commit()
        finally:
            conn.close()

    def get_history(self, session_id: str) -> list[dict]:
        """Retrieve up to 10 most recent exchanges in chronological order."""
        conn = self._get_connection()
        try:
            cursor = conn.execute(
                """
                SELECT prompt, response, timestamp FROM exchanges
                WHERE session_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (session_id, self.MAX_CONTEXT_PAIRS),
            )
            rows = cursor.fetchall()
        finally:
            conn.close()
        # Reverse to chronological order (oldest first)
        rows.reverse()
        return [
            {"prompt": row[0], "response": row[1], "timestamp": row[2]}
            for row in rows
        ]

    def clear_session(self, session_id: str) -> None:
        """Remove all exchanges for a session."""
        conn = self._get_connection()
        try:
            conn.execute(
                "DELETE FROM exchanges WHERE session_id = ?",
                (session_id,),
            )
            conn.commit()
        finally:
            conn.close()
