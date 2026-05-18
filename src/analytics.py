"""Session analytics and model statistics using Pandas.

Provides data analysis capabilities for tracking usage patterns,
topic frequency, response quality metrics, and model performance.
Uses Pandas DataFrames for structured data manipulation and analysis.
"""

import os
import re
import sqlite3
from datetime import datetime

import pandas as pd
import numpy as np


class SessionAnalytics:
    """Analyze session data using Pandas DataFrames.

    Reads session history from the SQLite database and provides
    statistical analysis of usage patterns, popular topics, and
    response characteristics.
    """

    def __init__(self, db_path: str):
        """Initialize with path to the sessions database."""
        self._db_path = db_path

    def get_session_dataframe(self) -> pd.DataFrame:
        """Load all exchanges into a Pandas DataFrame.

        Returns DataFrame with columns:
            session_id, prompt, response, timestamp, word_count,
            response_length, topic_category, language
        """
        if not os.path.isfile(self._db_path):
            return pd.DataFrame(columns=[
                "session_id", "prompt", "response", "timestamp",
                "prompt_words", "response_lines", "topic_category", "language"
            ])

        conn = sqlite3.connect(self._db_path)
        try:
            df = pd.read_sql_query(
                """
                SELECT e.session_id, e.prompt, e.response, e.timestamp
                FROM exchanges e
                ORDER BY e.timestamp
                """,
                conn,
            )
        finally:
            conn.close()

        if df.empty:
            df["prompt_words"] = []
            df["response_lines"] = []
            df["topic_category"] = []
            df["language"] = []
            return df

        # Enrich with computed columns
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["prompt_words"] = df["prompt"].apply(lambda x: len(x.split()))
        df["response_lines"] = df["response"].apply(lambda x: len(x.splitlines()))
        df["topic_category"] = df["prompt"].apply(self._classify_topic)
        df["language"] = df["response"].apply(self._detect_language)

        return df

    def get_topic_distribution(self) -> pd.DataFrame:
        """Get frequency distribution of topics asked about.

        Returns DataFrame with columns: topic, count, percentage
        """
        df = self.get_session_dataframe()
        if df.empty:
            return pd.DataFrame(columns=["topic", "count", "percentage"])

        topic_counts = df["topic_category"].value_counts().reset_index()
        topic_counts.columns = ["topic", "count"]
        topic_counts["percentage"] = (
            topic_counts["count"] / topic_counts["count"].sum() * 100
        ).round(1)

        return topic_counts

    def get_language_distribution(self) -> pd.DataFrame:
        """Get distribution of response languages (Python, Bash, C).

        Returns DataFrame with columns: language, count, percentage
        """
        df = self.get_session_dataframe()
        if df.empty:
            return pd.DataFrame(columns=["language", "count", "percentage"])

        lang_counts = df["language"].value_counts().reset_index()
        lang_counts.columns = ["language", "count"]
        lang_counts["percentage"] = (
            lang_counts["count"] / lang_counts["count"].sum() * 100
        ).round(1)

        return lang_counts

    def get_usage_over_time(self) -> pd.DataFrame:
        """Get usage statistics grouped by date.

        Returns DataFrame with columns: date, query_count, avg_prompt_words
        """
        df = self.get_session_dataframe()
        if df.empty:
            return pd.DataFrame(columns=["date", "query_count", "avg_prompt_words"])

        df["date"] = df["timestamp"].dt.date
        daily = df.groupby("date").agg(
            query_count=("prompt", "count"),
            avg_prompt_words=("prompt_words", "mean"),
        ).reset_index()
        daily["avg_prompt_words"] = daily["avg_prompt_words"].round(1)

        return daily

    def get_summary_stats(self) -> dict:
        """Get overall summary statistics as a dictionary."""
        df = self.get_session_dataframe()

        if df.empty:
            return {
                "total_queries": 0,
                "total_sessions": 0,
                "avg_prompt_length": 0,
                "avg_response_lines": 0,
                "most_popular_topic": "N/A",
                "most_used_language": "N/A",
            }

        return {
            "total_queries": len(df),
            "total_sessions": df["session_id"].nunique(),
            "avg_prompt_length": round(df["prompt_words"].mean(), 1),
            "avg_response_lines": round(df["response_lines"].mean(), 1),
            "most_popular_topic": df["topic_category"].mode().iloc[0] if not df["topic_category"].mode().empty else "N/A",
            "most_used_language": df["language"].mode().iloc[0] if not df["language"].mode().empty else "N/A",
        }

    @staticmethod
    def _classify_topic(prompt: str) -> str:
        """Classify a prompt into a topic category."""
        lower = prompt.lower()

        # Shell/Bash topics
        shell_keywords = {"bash", "shell", "script", "grep", "awk", "sed",
                          "chmod", "cron", "apt", "systemctl", "ssh", "find"}
        if any(kw in lower for kw in shell_keywords):
            return "Shell/Bash"

        # C/OS topics
        c_keywords = {"fork", "pthread", "mutex", "semaphore", "pipe",
                      "socket", "malloc", "signal", "thread", "#include"}
        if any(kw in lower for kw in c_keywords):
            return "C/OS Concepts"

        # DSA topics
        dsa_keywords = {"sort", "search", "tree", "graph", "linked list",
                        "stack", "queue", "dynamic programming", "recursion"}
        if any(kw in lower for kw in dsa_keywords):
            return "Data Structures"

        # File I/O
        if any(kw in lower for kw in {"file", "read", "write", "csv", "json"}):
            return "File I/O"

        # OOP
        if any(kw in lower for kw in {"class", "inheritance", "object", "oop"}):
            return "OOP"

        return "General Python"

    @staticmethod
    def _detect_language(response: str) -> str:
        """Detect the programming language of a response."""
        if "#include" in response or "int main(" in response:
            return "C"
        if "#!/bin/bash" in response or "#!/bin/sh" in response:
            return "Bash"
        if response.strip().startswith("echo ") or "fi\n" in response:
            return "Bash"
        return "Python"


class ModelAnalytics:
    """Analyze model corpus statistics using Pandas and NumPy."""

    def __init__(self, snippets: list[dict]):
        """Initialize with the model's snippet list."""
        self._snippets = snippets

    def get_corpus_dataframe(self) -> pd.DataFrame:
        """Convert snippets to a Pandas DataFrame for analysis.

        Returns DataFrame with columns:
            description, keyword_count, code_lines, language, code_length
        """
        records = []
        for snippet in self._snippets:
            code = snippet.get("code", "")
            records.append({
                "description": snippet.get("description", ""),
                "keyword_count": len(snippet.get("keywords", [])),
                "code_lines": len(code.splitlines()),
                "code_length": len(code),
                "language": self._detect_snippet_language(code),
            })

        return pd.DataFrame(records)

    def get_corpus_summary(self) -> dict:
        """Get summary statistics about the training corpus."""
        df = self.get_corpus_dataframe()

        if df.empty:
            return {"total_snippets": 0}

        return {
            "total_snippets": len(df),
            "by_language": df["language"].value_counts().to_dict(),
            "avg_keywords_per_snippet": round(df["keyword_count"].mean(), 1),
            "avg_code_lines": round(df["code_lines"].mean(), 1),
            "total_code_lines": int(df["code_lines"].sum()),
            "longest_snippet_lines": int(df["code_lines"].max()),
            "shortest_snippet_lines": int(df["code_lines"].min()),
        }

    def get_keyword_frequency(self, top_n: int = 20) -> pd.DataFrame:
        """Get the most frequent keywords across all snippets.

        Returns DataFrame with columns: keyword, frequency
        """
        all_keywords = []
        for snippet in self._snippets:
            all_keywords.extend(snippet.get("keywords", []))

        keyword_series = pd.Series(all_keywords)
        freq = keyword_series.value_counts().head(top_n).reset_index()
        freq.columns = ["keyword", "frequency"]

        return freq

    @staticmethod
    def _detect_snippet_language(code: str) -> str:
        """Detect language from code content."""
        if "#include" in code or "int main(" in code or "void " in code:
            return "C"
        if code.lstrip().startswith("#!/bin/bash") or code.lstrip().startswith("#!/bin/sh"):
            return "Bash"
        shell_patterns = ["echo ", "fi\n", "done\n", "esac"]
        if any(p in code for p in shell_patterns):
            return "Bash"
        return "Python"
