"""Visualization module using Matplotlib.

Generates charts and plots for model statistics, topic distribution,
usage patterns, and TF-IDF analysis. Saves visualizations as PNG files
in the project's output directory.
"""

import os

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd

# Use non-interactive backend for file output
matplotlib.use("Agg")


class Visualizer:
    """Generate statistical visualizations for the coding assistant.

    Creates charts showing corpus composition, topic distribution,
    keyword frequency, TF-IDF weights, and usage analytics.
    """

    def __init__(self, output_dir: str = "output/charts"):
        """Initialize with output directory for saved charts."""
        self._output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def plot_corpus_distribution(self, corpus_df: pd.DataFrame) -> str:
        """Plot the distribution of snippets by programming language.

        Args:
            corpus_df: DataFrame with 'language' column from ModelAnalytics

        Returns:
            Path to saved chart image
        """
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Pie chart of language distribution
        lang_counts = corpus_df["language"].value_counts()
        colors = ["#3498db", "#2ecc71", "#e74c3c", "#f39c12"]
        axes[0].pie(
            lang_counts.values,
            labels=lang_counts.index,
            autopct="%1.1f%%",
            colors=colors[:len(lang_counts)],
            startangle=90,
            shadow=True,
        )
        axes[0].set_title("Snippet Distribution by Language", fontsize=12, fontweight="bold")

        # Bar chart of code lines per language
        lang_lines = corpus_df.groupby("language")["code_lines"].agg(["mean", "sum"])
        bars = axes[1].bar(
            lang_lines.index,
            lang_lines["mean"],
            color=colors[:len(lang_lines)],
            edgecolor="black",
            linewidth=0.5,
        )
        axes[1].set_title("Average Code Lines per Snippet", fontsize=12, fontweight="bold")
        axes[1].set_ylabel("Lines of Code")
        axes[1].set_xlabel("Language")

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            axes[1].annotate(
                f"{height:.0f}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center", va="bottom", fontsize=10,
            )

        plt.tight_layout()
        path = os.path.join(self._output_dir, "corpus_distribution.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def plot_keyword_frequency(self, keyword_df: pd.DataFrame) -> str:
        """Plot top keywords as a horizontal bar chart.

        Args:
            keyword_df: DataFrame with 'keyword' and 'frequency' columns

        Returns:
            Path to saved chart image
        """
        fig, ax = plt.subplots(figsize=(10, 8))

        # Horizontal bar chart (reversed for top at top)
        y_pos = np.arange(len(keyword_df))
        bars = ax.barh(
            y_pos,
            keyword_df["frequency"].values,
            color=plt.cm.viridis(np.linspace(0.3, 0.9, len(keyword_df))),
            edgecolor="black",
            linewidth=0.3,
        )
        ax.set_yticks(y_pos)
        ax.set_yticklabels(keyword_df["keyword"].values)
        ax.invert_yaxis()  # Top keyword at top
        ax.set_xlabel("Frequency", fontsize=11)
        ax.set_title("Top Keywords in Training Corpus", fontsize=13, fontweight="bold")

        # Add value labels
        for bar in bars:
            width = bar.get_width()
            ax.annotate(
                f"{width:.0f}",
                xy=(width, bar.get_y() + bar.get_height() / 2),
                xytext=(3, 0),
                textcoords="offset points",
                ha="left", va="center", fontsize=9,
            )

        plt.tight_layout()
        path = os.path.join(self._output_dir, "keyword_frequency.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def plot_tfidf_heatmap(self, tfidf_matrix: np.ndarray, vocab: list[str],
                           top_n_terms: int = 20, top_n_docs: int = 15) -> str:
        """Plot a heatmap of TF-IDF weights for top terms and documents.

        Args:
            tfidf_matrix: NumPy array of shape (n_docs, n_terms)
            vocab: List of vocabulary terms
            top_n_terms: Number of top terms to show
            top_n_docs: Number of documents to show

        Returns:
            Path to saved chart image
        """
        # Select top terms by average TF-IDF weight
        avg_weights = np.mean(tfidf_matrix, axis=0)
        top_term_indices = np.argsort(avg_weights)[::-1][:top_n_terms]

        # Select subset of documents
        doc_indices = np.arange(min(top_n_docs, tfidf_matrix.shape[0]))

        # Extract submatrix
        submatrix = tfidf_matrix[np.ix_(doc_indices, top_term_indices)]
        term_labels = [vocab[i] for i in top_term_indices]

        fig, ax = plt.subplots(figsize=(14, 8))
        im = ax.imshow(submatrix, cmap="YlOrRd", aspect="auto")

        ax.set_xticks(np.arange(len(term_labels)))
        ax.set_xticklabels(term_labels, rotation=45, ha="right", fontsize=9)
        ax.set_yticks(np.arange(len(doc_indices)))
        ax.set_yticklabels([f"Snippet {i+1}" for i in doc_indices], fontsize=9)

        ax.set_title("TF-IDF Weight Heatmap (Top Terms × Snippets)",
                     fontsize=13, fontweight="bold")
        plt.colorbar(im, ax=ax, label="TF-IDF Weight")

        plt.tight_layout()
        path = os.path.join(self._output_dir, "tfidf_heatmap.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def plot_topic_distribution(self, topic_df: pd.DataFrame) -> str:
        """Plot topic distribution from session analytics.

        Args:
            topic_df: DataFrame with 'topic' and 'count' columns

        Returns:
            Path to saved chart image
        """
        if topic_df.empty:
            return ""

        fig, ax = plt.subplots(figsize=(8, 6))

        colors = plt.cm.Set3(np.linspace(0, 1, len(topic_df)))
        wedges, texts, autotexts = ax.pie(
            topic_df["count"].values,
            labels=topic_df["topic"].values,
            autopct="%1.1f%%",
            colors=colors,
            startangle=140,
            shadow=True,
        )

        ax.set_title("Query Topic Distribution", fontsize=13, fontweight="bold")
        plt.tight_layout()
        path = os.path.join(self._output_dir, "topic_distribution.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def plot_usage_timeline(self, usage_df: pd.DataFrame) -> str:
        """Plot usage over time as a line chart.

        Args:
            usage_df: DataFrame with 'date' and 'query_count' columns

        Returns:
            Path to saved chart image
        """
        if usage_df.empty:
            return ""

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(
            usage_df["date"],
            usage_df["query_count"],
            marker="o",
            linewidth=2,
            color="#3498db",
            markersize=6,
        )
        ax.fill_between(
            usage_df["date"],
            usage_df["query_count"],
            alpha=0.2,
            color="#3498db",
        )

        ax.set_title("Queries Over Time", fontsize=13, fontweight="bold")
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Queries")
        ax.grid(True, alpha=0.3)

        plt.xticks(rotation=45)
        plt.tight_layout()
        path = os.path.join(self._output_dir, "usage_timeline.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path

    def plot_snippet_complexity(self, corpus_df: pd.DataFrame) -> str:
        """Plot snippet complexity analysis (lines vs keywords scatter).

        Args:
            corpus_df: DataFrame with 'code_lines', 'keyword_count', 'language'

        Returns:
            Path to saved chart image
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        languages = corpus_df["language"].unique()
        colors = {"Python": "#3498db", "Bash": "#2ecc71", "C": "#e74c3c"}

        for lang in languages:
            subset = corpus_df[corpus_df["language"] == lang]
            ax.scatter(
                subset["keyword_count"],
                subset["code_lines"],
                label=lang,
                color=colors.get(lang, "#95a5a6"),
                alpha=0.7,
                s=60,
                edgecolors="black",
                linewidth=0.3,
            )

        ax.set_xlabel("Number of Keywords", fontsize=11)
        ax.set_ylabel("Lines of Code", fontsize=11)
        ax.set_title("Snippet Complexity: Keywords vs Code Length",
                     fontsize=13, fontweight="bold")
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        path = os.path.join(self._output_dir, "snippet_complexity.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        return path
