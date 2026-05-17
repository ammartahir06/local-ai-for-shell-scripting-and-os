"""Tests for main.py application entry point."""

import json
import sys
import types
from unittest.mock import MagicMock, patch

import pytest

from src.config import ModelLoadError, ResourceStoreError


class TestMainStartupErrors:
    """Test that main() handles startup errors with clear messages and sys.exit(1)."""

    @patch("src.config.AppConfig.load", side_effect=FileNotFoundError)
    def test_missing_config_exits(self, _mock_load, capsys):
        from main import main

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "config.json not found" in captured.out

    @patch("src.config.AppConfig.load", side_effect=json.JSONDecodeError("bad", "", 0))
    def test_invalid_json_config_exits(self, _mock_load, capsys):
        from main import main

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "not valid JSON" in captured.out

    def test_model_load_error_exits(self, capsys, tmp_path):
        config = MagicMock()
        config.log_path = str(tmp_path / "app.log")

        # Create a fake src.ui module so we don't need rich/pyperclip installed
        fake_ui_mod = types.ModuleType("src.ui")
        fake_ui_mod.UserInterface = MagicMock  # type: ignore[attr-defined]

        with (
            patch("src.config.AppConfig.load", return_value=config),
            patch("src.model_loader.ModelLoader") as mock_ml_cls,
            patch.dict(sys.modules, {"src.ui": fake_ui_mod}),
        ):
            loader_instance = MagicMock()
            loader_instance.load.side_effect = ModelLoadError(
                "/path/to/model.gguf", "file not found"
            )
            mock_ml_cls.return_value = loader_instance

            from main import main

            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "model" in captured.out.lower()

    def test_resource_store_error_exits(self, capsys, tmp_path):
        config = MagicMock()
        config.log_path = str(tmp_path / "app.log")

        fake_ui_mod = types.ModuleType("src.ui")
        fake_ui_mod.UserInterface = MagicMock  # type: ignore[attr-defined]

        with (
            patch("src.config.AppConfig.load", return_value=config),
            patch("src.model_loader.ModelLoader") as mock_ml_cls,
            patch("src.resource_store.ResourceStore") as mock_rs_cls,
            patch.dict(sys.modules, {"src.ui": fake_ui_mod}),
        ):
            mock_ml_cls.return_value = MagicMock()
            mock_rs_cls.side_effect = ResourceStoreError("/path/to/resources")

            from main import main

            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "resource" in captured.out.lower()
