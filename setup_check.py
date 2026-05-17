"""Pre-flight check script for the Offline Coding AI Assistant.

Verifies that the environment meets all requirements before launching:
- Python version >= 3.10
- Required directories exist (models/, resources/)
- config.json is valid JSON
- Model file exists at the configured path
"""

import json
import os
import sys


def get_project_root() -> str:
    """Return the project root based on this script's location."""
    return os.path.dirname(os.path.abspath(__file__))


def check_python_version() -> bool:
    """Verify Python >= 3.10."""
    if sys.version_info >= (3, 10):
        print(f"[OK] Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        return True
    print(f"[FAIL] Python 3.10+ required, found {sys.version}")
    return False


def check_directory(root: str, name: str) -> bool:
    """Verify a required directory exists."""
    path = os.path.join(root, name)
    if os.path.isdir(path):
        print(f"[OK] Directory: {name}/")
        return True
    print(f"[FAIL] Missing directory: {name}/")
    return False


def check_config(root: str) -> dict | None:
    """Verify config.json exists and is valid JSON. Returns parsed data or None."""
    path = os.path.join(root, "config.json")
    if not os.path.isfile(path):
        print("[FAIL] config.json not found")
        return None
    try:
        with open(path) as f:
            data = json.load(f)
        print("[OK] config.json is valid JSON")
        return data
    except json.JSONDecodeError as exc:
        print(f"[FAIL] config.json is not valid JSON: {exc}")
        return None


def check_model(root: str, config: dict) -> bool:
    """Verify the model file exists at the configured path."""
    model_dir = config.get("model_dir", "models")
    model_filename = config.get("model_filename", "")
    model_path = os.path.join(root, model_dir, model_filename)
    if os.path.isfile(model_path):
        print(f"[OK] Model file: {model_dir}/{model_filename}")
        return True
    print(f"[INFO] Model file not found: {model_dir}/{model_filename}")
    print(f"       Run 'python train_model.py' to generate it.")
    return False


def main() -> int:
    """Run all pre-flight checks. Returns 0 if all pass, 1 otherwise."""
    root = get_project_root()
    print(f"Project root: {root}\n")

    results = []
    results.append(check_python_version())
    results.append(check_directory(root, "models"))
    results.append(check_directory(root, "resources"))

    config = check_config(root)
    results.append(config is not None)

    if config is not None:
        results.append(check_model(root, config))

    print()
    if all(results):
        print("All checks passed.")
        return 0
    else:
        print("Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
