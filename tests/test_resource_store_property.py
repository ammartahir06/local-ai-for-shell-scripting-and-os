"""Property-based tests for ResourceStore search.

Property 4: Resource search returns topic-relevant entries
For any query string that matches a known topic keyword in the Resource_Store,
all returned ResourceEntry items SHALL have a topic field that matches
the queried topic.

Validates: Requirements 5.3
"""

import os
import json
import tempfile

from hypothesis import given, settings, strategies as st

from src.config import AppConfig
from src.resource_store import ResourceStore


# Known topics that exist in the sample resource files
KNOWN_TOPICS = ["os", "json", "sys", "loops", "file_io", "classes"]


def _make_store():
    """Create a ResourceStore backed by a temp resource directory with sample files."""
    tmp = tempfile.mkdtemp()
    res_dir = os.path.join(tmp, "resources")
    docs_dir = os.path.join(res_dir, "docs", "stdlib")
    examples_dir = os.path.join(res_dir, "examples")
    os.makedirs(docs_dir)
    os.makedirs(examples_dir)

    # Write index.json mapping topics to keyword aliases
    index = {
        "os": ["operating system", "file system", "path", "directory"],
        "json": ["serialization", "parsing", "data format"],
        "sys": ["system", "interpreter", "argv"],
        "loops": ["for", "while", "iteration", "loop"],
        "file_io": ["file", "read", "write", "open"],
        "classes": ["class", "object", "oop", "inheritance"],
    }
    with open(os.path.join(res_dir, "docs", "index.json"), "w") as f:
        json.dump(index, f)

    # Create minimal doc files
    for topic in ["os", "json", "sys"]:
        with open(os.path.join(docs_dir, f"{topic}.md"), "w") as f:
            f.write(f"# {topic} module\n\nDocumentation for {topic}.\n")

    # Create minimal example files
    for topic in ["loops", "file_io", "classes"]:
        with open(os.path.join(examples_dir, f"{topic}.md"), "w") as f:
            f.write(f"# {topic}\n\nExample for {topic}.\n")

    config = AppConfig(
        model_filename="test.gguf",
        model_dir="models",
        resource_dir=res_dir,
        data_dir="data",
        log_dir="logs",
        max_prompt_length=2000,
        max_context_pairs=10,
        response_timeout_seconds=30,
    )
    # Override resource_path to use the absolute temp path directly
    config.resource_dir = res_dir
    return ResourceStore.__new__(ResourceStore), config, res_dir


def _build_store(res_dir):
    """Build a ResourceStore from an absolute resource directory path."""
    config = AppConfig(
        model_filename="test.gguf",
        model_dir="models",
        resource_dir="resources",
        data_dir="data",
        log_dir="logs",
        max_prompt_length=2000,
        max_context_pairs=10,
        response_timeout_seconds=30,
    )
    # Monkey-patch resource_path to point to our temp dir
    config.__class__ = type(
        "TestAppConfig",
        (AppConfig,),
        {"resource_path": property(lambda self: res_dir)},
    )
    return ResourceStore(config)


def _create_temp_store():
    """Create a fully initialized ResourceStore with sample data in a temp dir."""
    tmp = tempfile.mkdtemp()
    res_dir = os.path.join(tmp, "resources")
    docs_dir = os.path.join(res_dir, "docs", "stdlib")
    examples_dir = os.path.join(res_dir, "examples")
    os.makedirs(docs_dir)
    os.makedirs(examples_dir)

    index = {
        "os": ["operating system", "file system", "path", "directory"],
        "json": ["serialization", "parsing", "data format"],
        "sys": ["system", "interpreter", "argv"],
        "loops": ["for", "while", "iteration", "loop"],
        "file_io": ["file", "read", "write", "open"],
        "classes": ["class", "object", "oop", "inheritance"],
    }
    with open(os.path.join(res_dir, "docs", "index.json"), "w") as f:
        json.dump(index, f)

    for topic in ["os", "json", "sys"]:
        with open(os.path.join(docs_dir, f"{topic}.md"), "w") as f:
            f.write(f"# {topic} module\n\nDocumentation for {topic}.\n")

    for topic in ["loops", "file_io", "classes"]:
        with open(os.path.join(examples_dir, f"{topic}.md"), "w") as f:
            f.write(f"# {topic}\n\nExample for {topic}.\n")

    return _build_store(res_dir)


# Strategy: pick a known topic keyword
topic_strategy = st.sampled_from(KNOWN_TOPICS)


class TestResourceSearchProperty:
    """Feature: offline-coding-ai, Property 4: Resource search returns topic-relevant entries"""

    @settings(max_examples=100, deadline=None)
    @given(topic=topic_strategy)
    def test_search_by_topic_returns_matching_entries(self, topic):
        """All results from a topic keyword search have a matching topic."""
        store = _create_temp_store()
        results = store.search(topic)
        assert len(results) > 0, f"Expected results for known topic '{topic}'"
        for entry in results:
            assert entry.topic.lower() == topic.lower()

    @settings(max_examples=100, deadline=None)
    @given(query=st.text(min_size=1, max_size=50).filter(
        lambda q: not any(t in q.lower() for t in KNOWN_TOPICS)
        and not any(
            alias in q.lower()
            for aliases in [
                ["operating system", "file system", "path", "directory"],
                ["serialization", "parsing", "data format"],
                ["system", "interpreter", "argv"],
                ["for", "while", "iteration", "loop"],
                ["file", "read", "write", "open"],
                ["class", "object", "oop", "inheritance"],
            ]
            for alias in aliases
        )
    ))
    def test_search_unknown_topic_returns_empty(self, query):
        """Searching for an unknown topic returns an empty list."""
        store = _create_temp_store()
        results = store.search(query)
        assert results == []

    @settings(max_examples=100, deadline=None)
    @given(topic=topic_strategy)
    def test_all_known_topics_are_discoverable(self, topic):
        """Every known topic appears in get_topics()."""
        store = _create_temp_store()
        available = store.get_topics()
        assert topic in available
