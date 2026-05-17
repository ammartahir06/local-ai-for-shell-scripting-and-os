"""Offline resource store for documentation and code examples.

Loads and indexes markdown files from the resources directory,
providing keyword-based search for documentation and examples.
"""

import json
import os
import re
from dataclasses import dataclass

from src.config import AppConfig, ResourceStoreError


@dataclass
class ResourceEntry:
    """A single documentation or example resource."""

    topic: str
    title: str
    content: str
    entry_type: str  # "documentation" or "example"


class ResourceStore:
    """Provides offline documentation and example lookup.

    Resources are loaded from markdown files under the configured
    resource directory and indexed by topic keywords for fast search.
    """

    def __init__(self, config: AppConfig) -> None:
        """Initialize the store and load resources.

        Raises ResourceStoreError if the resource directory is missing.
        """
        self._resource_path = config.resource_path
        if not os.path.isdir(self._resource_path):
            raise ResourceStoreError(self._resource_path)

        self._entries: list[ResourceEntry] = []
        self._topic_index: dict[str, list[ResourceEntry]] = {}
        self._load_index()
        self._load_docs()
        self._load_examples()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def search(self, query: str) -> list[ResourceEntry]:
        """Search for resources matching topic keywords in the query.

        Uses word-boundary matching so that short keywords like "oop"
        don't accidentally match inside unrelated words like "loops".
        Returns matching ResourceEntry items, or an empty list if none match.
        """
        query_lower = query.lower()
        # Tokenize the query into individual words for exact matching
        query_words = set(re.findall(r"[a-z0-9_]+", query_lower))
        results: list[ResourceEntry] = []
        seen: set[int] = set()
        for keyword, entries in self._topic_index.items():
            # Match if the keyword is one of the query words, or if a
            # multi-word keyword phrase appears in the query as a substring.
            keyword_words = set(re.findall(r"[a-z0-9_]+", keyword))
            if " " in keyword:
                matched = keyword in query_lower
            else:
                matched = keyword_words & query_words
            if matched:
                for entry in entries:
                    eid = id(entry)
                    if eid not in seen:
                        seen.add(eid)
                        results.append(entry)
        return results

    def get_topics(self) -> list[str]:
        """List all available topics in the resource store."""
        return sorted(self._topic_index.keys())

    # ------------------------------------------------------------------
    # Internal loading helpers
    # ------------------------------------------------------------------

    def _load_index(self) -> None:
        """Load the topic index from resources/docs/index.json if present."""
        index_path = os.path.join(self._resource_path, "docs", "index.json")
        if os.path.isfile(index_path):
            with open(index_path, encoding="utf-8") as f:
                self._raw_index = json.load(f)
        else:
            self._raw_index = {}

    def _load_docs(self) -> None:
        """Load markdown documentation files from resources/docs/stdlib/."""
        stdlib_dir = os.path.join(self._resource_path, "docs", "stdlib")
        if not os.path.isdir(stdlib_dir):
            return
        for filename in sorted(os.listdir(stdlib_dir)):
            if not filename.endswith(".md"):
                continue
            filepath = os.path.join(stdlib_dir, filename)
            topic = filename[:-3]  # strip .md
            content = self._read_file(filepath)
            title = self._extract_title(content, topic)
            entry = ResourceEntry(
                topic=topic,
                title=title,
                content=content,
                entry_type="documentation",
            )
            self._entries.append(entry)
            self._index_entry(topic, entry)

    def _load_examples(self) -> None:
        """Load markdown example files from resources/examples/."""
        examples_dir = os.path.join(self._resource_path, "examples")
        if not os.path.isdir(examples_dir):
            return
        for filename in sorted(os.listdir(examples_dir)):
            if not filename.endswith(".md"):
                continue
            filepath = os.path.join(examples_dir, filename)
            topic = filename[:-3]  # strip .md
            content = self._read_file(filepath)
            title = self._extract_title(content, topic)
            entry = ResourceEntry(
                topic=topic,
                title=title,
                content=content,
                entry_type="example",
            )
            self._entries.append(entry)
            self._index_entry(topic, entry)

    def _index_entry(self, topic: str, entry: ResourceEntry) -> None:
        """Add an entry to the topic index under its topic keyword."""
        key = topic.lower()
        self._topic_index.setdefault(key, []).append(entry)
        # Also index any aliases from the index.json
        for alias_topic, aliases in self._raw_index.items():
            if alias_topic.lower() == key and isinstance(aliases, list):
                for alias in aliases:
                    alias_key = alias.lower()
                    self._topic_index.setdefault(alias_key, []).append(entry)

    @staticmethod
    def _read_file(filepath: str) -> str:
        """Read a file and return its content."""
        with open(filepath, encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def _extract_title(content: str, fallback: str) -> str:
        """Extract the first markdown heading as the title, or use fallback."""
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip()
        return fallback
