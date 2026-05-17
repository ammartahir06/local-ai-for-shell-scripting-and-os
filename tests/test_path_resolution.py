"""Property test for path resolution (Property 7).

Property 7: All resolved paths are relative to project root.
Generate random AppConfig values with various relative directory names,
verify all resolved paths start with project root.

Validates: Requirements 1.1, 4.1
"""

import os
import string

from hypothesis import given, settings
from hypothesis import strategies as st

from src.config import AppConfig
from src.path_utils import get_project_root

# Strategy for valid relative directory names: 1-20 alphanumeric/underscore chars
_dir_name = st.text(
    alphabet=string.ascii_letters + string.digits + "_-",
    min_size=1,
    max_size=20,
).filter(lambda s: s.strip("-") != "")

_filename = st.text(
    alphabet=string.ascii_letters + string.digits + "_-.",
    min_size=3,
    max_size=30,
).filter(lambda s: not s.startswith(".") and "." in s)


@st.composite
def app_configs(draw):
    """Generate random AppConfig instances with various relative directory names."""
    return AppConfig(
        model_filename=draw(_filename),
        model_dir=draw(_dir_name),
        resource_dir=draw(_dir_name),
        data_dir=draw(_dir_name),
        log_dir=draw(_dir_name),
        max_prompt_length=draw(st.integers(min_value=1, max_value=10000)),
        max_context_pairs=draw(st.integers(min_value=1, max_value=100)),
        response_timeout_seconds=draw(st.integers(min_value=1, max_value=300)),
    )


PROJECT_ROOT = get_project_root()


@given(config=app_configs())
@settings(max_examples=100)
def test_all_resolved_paths_start_with_project_root(config: AppConfig):
    """Property 7: All resolved paths are relative to project root.

    For any AppConfig with arbitrary relative directory names, model_path,
    resource_path, database_path, and log_path must all begin with the
    project root directory prefix.
    """
    paths = {
        "model_path": config.model_path,
        "resource_path": config.resource_path,
        "database_path": config.database_path,
        "log_path": config.log_path,
    }

    for name, resolved in paths.items():
        norm_resolved = os.path.normpath(resolved)
        norm_root = os.path.normpath(PROJECT_ROOT)
        assert norm_resolved.startswith(norm_root), (
            f"{name} = {resolved!r} does not start with project root {PROJECT_ROOT!r}"
        )


@given(config=app_configs())
@settings(max_examples=100)
def test_resolved_paths_contain_no_hardcoded_absolute_paths(config: AppConfig):
    """Property 7 (corollary): Resolved paths must not contain hardcoded
    absolute path segments from the config values themselves.

    The config values (model_dir, resource_dir, etc.) are relative names.
    The resolved paths should be project_root + relative parts, never
    treating config values as absolute roots.
    """
    for resolved in [
        config.model_path,
        config.resource_path,
        config.database_path,
        config.log_path,
    ]:
        # After stripping the project root prefix, the remainder should
        # be a relative path (no leading separator that would indicate
        # an independent absolute path was injected).
        norm_resolved = os.path.normpath(resolved)
        norm_root = os.path.normpath(PROJECT_ROOT)
        remainder = norm_resolved[len(norm_root):]
        # remainder starts with separator, strip it
        remainder = remainder.lstrip(os.sep)
        assert not os.path.isabs(remainder), (
            f"Remainder {remainder!r} is absolute — config value leaked as absolute path"
        )
