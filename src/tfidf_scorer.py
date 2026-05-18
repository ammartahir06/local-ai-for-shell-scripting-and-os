"""TF-IDF based snippet scoring using NumPy.

Provides vectorized cosine similarity scoring between user prompts
and stored code snippets. Uses NumPy for efficient matrix operations
on the term-frequency inverse-document-frequency vectors.

This module replaces the basic keyword-overlap scoring with a proper
information retrieval approach using TF-IDF weighting and cosine similarity.
"""

import numpy as np
import re
from collections import Counter


class TFIDFScorer:
    """Vectorized TF-IDF scorer using NumPy for snippet retrieval.

    Builds a term-document matrix from snippet keywords and uses
    cosine similarity to find the best-matching snippets for a query.
    """

    def __init__(self, snippets: list[dict], high_value_words: frozenset = None):
        """Initialize the scorer with indexed snippets.

        Args:
            snippets: List of snippet dicts with 'keywords', 'code', 'description'
            high_value_words: Set of words that get boosted weight
        """
        self._snippets = snippets
        self._high_value_words = high_value_words or frozenset()
        self._vocabulary: list[str] = []
        self._word_to_idx: dict[str, int] = {}
        self._tfidf_matrix: np.ndarray | None = None
        self._idf: np.ndarray | None = None

        if snippets:
            self._build_index()

    def _build_index(self) -> None:
        """Build the TF-IDF matrix from all snippets using NumPy."""
        # Step 1: Build vocabulary from all snippet keywords
        vocab_set: set[str] = set()
        for snippet in self._snippets:
            vocab_set.update(snippet.get("keywords", []))
        self._vocabulary = sorted(vocab_set)
        self._word_to_idx = {word: i for i, word in enumerate(self._vocabulary)}

        n_docs = len(self._snippets)
        n_terms = len(self._vocabulary)

        if n_terms == 0:
            return

        # Step 2: Build term-frequency matrix (n_docs x n_terms)
        tf_matrix = np.zeros((n_docs, n_terms), dtype=np.float32)

        for doc_idx, snippet in enumerate(self._snippets):
            keywords = snippet.get("keywords", [])
            word_counts = Counter(keywords)
            for word, count in word_counts.items():
                if word in self._word_to_idx:
                    term_idx = self._word_to_idx[word]
                    tf_matrix[doc_idx, term_idx] = count

        # Step 3: Compute IDF (inverse document frequency)
        # IDF = log(N / (1 + df)) where df = number of docs containing the term
        doc_freq = np.sum(tf_matrix > 0, axis=0).astype(np.float32)
        self._idf = np.log((n_docs + 1) / (1 + doc_freq)) + 1  # smoothed IDF

        # Step 4: Apply high-value word boost
        for word in self._high_value_words:
            if word in self._word_to_idx:
                idx = self._word_to_idx[word]
                self._idf[idx] *= 2.0  # Double the IDF for high-value words

        # Step 5: Compute TF-IDF matrix
        # TF-IDF = TF * IDF
        self._tfidf_matrix = tf_matrix * self._idf

        # Step 6: Normalize each document vector (for cosine similarity)
        norms = np.linalg.norm(self._tfidf_matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1  # Avoid division by zero
        self._tfidf_matrix = self._tfidf_matrix / norms

    def score(self, query_keywords: set[str], top_k: int = 10) -> list[tuple[float, int]]:
        """Score all snippets against query keywords using cosine similarity.

        Args:
            query_keywords: Set of keywords extracted from the user prompt
            top_k: Number of top results to return

        Returns:
            List of (score, snippet_index) tuples, sorted by score descending
        """
        if self._tfidf_matrix is None or len(self._vocabulary) == 0:
            return []

        # Build query vector
        query_vector = np.zeros(len(self._vocabulary), dtype=np.float32)
        for word in query_keywords:
            if word in self._word_to_idx:
                idx = self._word_to_idx[word]
                query_vector[idx] = 1.0

        # Apply IDF weighting to query
        query_vector = query_vector * self._idf

        # Normalize query vector
        query_norm = np.linalg.norm(query_vector)
        if query_norm == 0:
            return []
        query_vector = query_vector / query_norm

        # Compute cosine similarity with all documents (vectorized dot product)
        similarities = np.dot(self._tfidf_matrix, query_vector)

        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score > 0:
                results.append((score, int(idx)))

        return results

    def get_vocabulary_stats(self) -> dict:
        """Return statistics about the TF-IDF index."""
        return {
            "vocabulary_size": len(self._vocabulary),
            "num_documents": len(self._snippets),
            "matrix_shape": self._tfidf_matrix.shape if self._tfidf_matrix is not None else (0, 0),
            "avg_idf": float(np.mean(self._idf)) if self._idf is not None else 0.0,
            "max_idf": float(np.max(self._idf)) if self._idf is not None else 0.0,
            "sparsity": float(np.sum(self._tfidf_matrix == 0) / self._tfidf_matrix.size)
            if self._tfidf_matrix is not None else 1.0,
        }
