"""Model loading and inference for the Offline Coding AI Assistant.

Loads a lightweight Markov chain model from models/markov_model.json
and provides streaming token inference. No external ML libraries needed.
"""

import logging
import os
from collections.abc import Generator

from src.config import AppConfig, ModelLoadError, InferenceError
from src.markov_engine import MarkovModel, MarkovGenerator

logger = logging.getLogger(__name__)


class ModelLoader:
    """Loads and manages the local Markov chain model for inference."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize with application config. Model is not loaded until load() is called."""
        self._config = config
        self._model: MarkovModel | None = None
        self._generator: MarkovGenerator | None = None
        self._model_path = config.model_path

    def load(self) -> None:
        """Load the Markov model from the models/ directory.

        Raises ModelLoadError if the file is missing or cannot be loaded.
        Logs model name and version on success.
        """
        if not os.path.isfile(self._model_path):
            raise ModelLoadError(self._model_path, "file not found")

        try:
            self._model = MarkovModel.load(self._model_path)
            self._generator = MarkovGenerator(self._model)
        except Exception as exc:
            raise ModelLoadError(
                self._model_path,
                f"file corrupted or failed to load: {exc}",
            ) from exc

        info = self.get_model_info()
        logger.info("Model loaded: %s (version: %s)", info["name"], info["version"])

    def infer(self, prompt: str) -> Generator[str, None, None]:
        """Run inference on the loaded model, streaming tokens.

        Yields partial output as string chunks (line by line).
        Raises InferenceError on failure.
        """
        if self._generator is None:
            raise InferenceError("Model is not loaded. Call load() first.")

        try:
            chunks = self._generator.generate_stream(prompt, max_tokens=200)
            for chunk in chunks:
                yield chunk
        except Exception as exc:
            raise InferenceError(str(exc)) from exc

    def get_model_info(self) -> dict:
        """Return model name and version metadata."""
        model_name = os.path.basename(self._model_path)
        n_transitions = len(self._model.transitions) if self._model else 0
        return {
            "name": model_name,
            "version": f"markov-ngram-{n_transitions}-transitions",
        }
