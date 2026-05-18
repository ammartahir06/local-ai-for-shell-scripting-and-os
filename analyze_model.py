"""Model Analysis & Visualization Script.

Demonstrates the use of NumPy, Pandas, Matplotlib, and OpenCV
in the Offline Coding AI Assistant project.

Usage:
    python analyze_model.py

This script:
1. Loads the trained model
2. Builds a TF-IDF index using NumPy
3. Analyzes corpus statistics using Pandas
4. Generates visualizations using Matplotlib
5. Demonstrates image processing using OpenCV
"""

import os
import sys
import numpy as np

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.markov_engine import MarkovModel, _HIGH_VALUE_WORDS
from src.tfidf_scorer import TFIDFScorer
from src.analytics import ModelAnalytics, SessionAnalytics
from src.visualizer import Visualizer
from src.image_processor import ImageProcessor


def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(project_root, "models", "markov_model.json")

    print("=" * 60)
    print("   OFFLINE CODING AI ASSISTANT - MODEL ANALYSIS")
    print("=" * 60)
    print()

    # --- Load Model ---
    print("[1/5] Loading trained model...")
    model = MarkovModel.load(model_path)
    print(f"  Loaded {len(model.snippets)} snippets")
    print()

    # --- NumPy: TF-IDF Scoring ---
    print("[2/5] Building TF-IDF index with NumPy...")
    scorer = TFIDFScorer(model.snippets, _HIGH_VALUE_WORDS)
    stats = scorer.get_vocabulary_stats()
    print(f"  Vocabulary size: {stats['vocabulary_size']} terms")
    print(f"  Matrix shape: {stats['matrix_shape']}")
    print(f"  Average IDF: {stats['avg_idf']:.3f}")
    print(f"  Matrix sparsity: {stats['sparsity']:.1%}")
    print()

    # Test TF-IDF scoring
    print("  Testing TF-IDF cosine similarity scoring:")
    test_queries = [
        {"fork", "process", "child", "wait"},
        {"bash", "loop", "for", "while"},
        {"mutex", "thread", "pthread", "lock"},
        {"sort", "bubble", "binary", "search"},
    ]
    for query in test_queries:
        results = scorer.score(query, top_k=3)
        if results:
            best_score, best_idx = results[0]
            desc = model.snippets[best_idx].get("description", "")[:50]
            print(f"    Query {query} -> score={best_score:.3f} '{desc}'")
    print()

    # --- Pandas: Corpus Analytics ---
    print("[3/5] Analyzing corpus with Pandas...")
    analytics = ModelAnalytics(model.snippets)
    corpus_df = analytics.get_corpus_dataframe()
    summary = analytics.get_corpus_summary()

    print(f"  Total snippets: {summary['total_snippets']}")
    print(f"  By language: {summary['by_language']}")
    print(f"  Avg keywords/snippet: {summary['avg_keywords_per_snippet']}")
    print(f"  Avg code lines: {summary['avg_code_lines']}")
    print(f"  Total code lines: {summary['total_code_lines']}")
    print()

    # Keyword frequency analysis
    keyword_df = analytics.get_keyword_frequency(top_n=15)
    print("  Top 15 keywords in corpus:")
    for _, row in keyword_df.iterrows():
        print(f"    {row['keyword']:20s} -> {row['frequency']} occurrences")
    print()

    # Session analytics (if database exists)
    db_path = os.path.join(project_root, "data", "sessions.db")
    session_analytics = SessionAnalytics(db_path)
    session_summary = session_analytics.get_summary_stats()
    print(f"  Session stats: {session_summary['total_queries']} total queries, "
          f"{session_summary['total_sessions']} sessions")
    print()

    # --- Matplotlib: Visualizations ---
    print("[4/5] Generating visualizations with Matplotlib...")
    viz = Visualizer(os.path.join(project_root, "output", "charts"))

    # Corpus distribution chart
    path1 = viz.plot_corpus_distribution(corpus_df)
    print(f"  Saved: {path1}")

    # Keyword frequency chart
    path2 = viz.plot_keyword_frequency(keyword_df)
    print(f"  Saved: {path2}")

    # Snippet complexity scatter plot
    path3 = viz.plot_snippet_complexity(corpus_df)
    print(f"  Saved: {path3}")

    # TF-IDF heatmap
    if scorer._tfidf_matrix is not None:
        path4 = viz.plot_tfidf_heatmap(
            scorer._tfidf_matrix,
            scorer._vocabulary,
            top_n_terms=20,
            top_n_docs=15,
        )
        print(f"  Saved: {path4}")
    print()

    # --- OpenCV: Image Processing Demo ---
    print("[5/5] Demonstrating OpenCV image processing...")
    processor = ImageProcessor(os.path.join(project_root, "output", "processed"))

    # Create a sample code image for demonstration
    demo_image_path = _create_demo_code_image(project_root)
    if demo_image_path:
        # Preprocess for OCR
        processed_path = processor.preprocess_for_ocr(demo_image_path)
        print(f"  Preprocessed image: {processed_path}")

        # Enhance contrast
        enhanced_path = processor.enhance_contrast(demo_image_path)
        print(f"  Enhanced image: {enhanced_path}")

        # Analyze code structure
        structure = processor.analyze_code_structure(demo_image_path)
        print(f"  Code structure analysis:")
        print(f"    Estimated lines: {structure['estimated_lines']}")
        print(f"    Image size: {structure['image_dimensions']}")
        print(f"    Code density: {structure['code_density']}%")
        print(f"    Has indentation: {structure['has_indentation']}")

        # Detect code region
        _, bbox = processor.detect_code_region(demo_image_path)
        print(f"    Code region: x={bbox[0]}, y={bbox[1]}, w={bbox[2]}, h={bbox[3]}")
    print()

    print("=" * 60)
    print("   ANALYSIS COMPLETE")
    print(f"   Charts saved to: output/charts/")
    print(f"   Processed images saved to: output/processed/")
    print("=" * 60)


def _create_demo_code_image(project_root: str) -> str:
    """Create a sample code image using OpenCV for demonstration."""
    import cv2

    # Create a white image
    img = np.ones((400, 600, 3), dtype=np.uint8) * 255

    # Add code text using OpenCV putText
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    color = (0, 0, 0)  # Black text
    thickness = 1
    line_height = 25

    code_lines = [
        "#!/bin/bash",
        "# Demo script for image processing",
        "",
        "sum_of_digits() {",
        "    local num=$1",
        "    local sum=0",
        "    while [ $num -gt 0 ]; do",
        "        digit=$((num % 10))",
        "        sum=$((sum + digit))",
        "        num=$((num / 10))",
        "    done",
        "    echo \"Sum: $sum\"",
        "}",
        "",
        "read -p \"Enter number: \" n",
        "sum_of_digits $n",
    ]

    y_offset = 30
    for i, line in enumerate(code_lines):
        y = y_offset + i * line_height
        cv2.putText(img, line, (20, y), font, font_scale, color, thickness)

    # Save the demo image
    output_dir = os.path.join(project_root, "output", "processed")
    os.makedirs(output_dir, exist_ok=True)
    demo_path = os.path.join(output_dir, "demo_code_input.png")
    cv2.imwrite(demo_path, img)
    print(f"  Created demo code image: {demo_path}")

    return demo_path


if __name__ == "__main__":
    main()
