"""Application configuration and custom exception types.

Provides the AppConfig dataclass for loading settings from config.json,
and custom exceptions for model loading, inference, and resource store errors.
"""

import json
from dataclasses import dataclass

from src.path_utils import resolve_path


@dataclass
class AppConfig:
    """Application configuration loaded from config.json.

    All directory fields are relative to the project root and resolved
    at runtime via the path properties.
    """

    model_filename: str
    model_dir: str
    resource_dir: str
    data_dir: str
    log_dir: str
    max_prompt_length: int
    max_context_pairs: int
    response_timeout_seconds: int

    @property
    def model_path(self) -> str:
        """Full resolved path to the GGUF model file."""
        return resolve_path(self.model_dir, self.model_filename)

    @property
    def resource_path(self) -> str:
        """Full resolved path to the resource directory."""
        return resolve_path(self.resource_dir)

    @property
    def database_path(self) -> str:
        """Full resolved path to the SQLite database."""
        return resolve_path(self.data_dir, "sessions.db")

    @property
    def log_path(self) -> str:
        """Full resolved path to the log file."""
        return resolve_path(self.log_dir, "app.log")

    @classmethod
    def load(cls, config_file: str = "config.json") -> "AppConfig":
        """Load configuration from a JSON file relative to the project root."""
        path = resolve_path(config_file)
        with open(path) as f:
            data = json.load(f)
        return cls(**data)


class ModelLoadError(Exception):
    """Raised when the model file is missing or corrupted."""

    def __init__(self, file_path: str, failure_reason: str) -> None:
        self.file_path = file_path
        self.failure_reason = failure_reason
        super().__init__(f"Failed to load model at '{file_path}': {failure_reason}")


class InferenceError(Exception):
    """Raised when model inference fails."""

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(f"Inference error: {detail}")


class ResourceStoreError(Exception):
    """Raised when the resource directory is missing."""

    def __init__(self, expected_path: str) -> None:
        self.expected_path = expected_path
        super().__init__(f"Resource directory missing: '{expected_path}'")
