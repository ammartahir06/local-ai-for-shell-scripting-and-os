"""Path resolution utilities for the Offline Coding AI Assistant.

All components use these functions to resolve paths relative to the project root,
ensuring portability regardless of where the project directory is located.
"""

import os


def get_project_root() -> str:
    """Return the absolute path to the project root directory.

    Determined from the location of this file (src/ is one level below project root),
    not the current working directory.
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def resolve_path(*parts: str) -> str:
    """Resolve a path relative to the project root.

    Example:
        resolve_path('models', 'codellama.gguf')
        -> '/abs/path/to/project/models/codellama.gguf'
    """
    return os.path.join(get_project_root(), *parts)
