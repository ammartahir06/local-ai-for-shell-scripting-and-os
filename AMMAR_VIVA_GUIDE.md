# Ammar's Viva Preparation Guide — NumPy + Pandas + Model Loading + Training

---

## File 1: `src/tfidf_scorer.py`

### Purpose
Builds a TF-IDF (Term Frequency - Inverse Document Frequency) scoring system using NumPy. This is how the AI finds the best matching code snippet for a user's question.

### Library Used
**NumPy** — for matrix operations, vectorized math, no Python loops needed

### How TF-IDF Works (Simple Explanation)

```
TF  = How often a word appears in ONE snippet
IDF = How rare a word is across ALL snippets (rare words = more important)
TF-IDF = TF × IDF

Example:
  "for" appears in 92 snippets → low IDF → not very useful for matching
  "semaphore" appears in 3 snippets → high IDF → very useful for matching
```

### What the Code Does Step by Step

```
Step 1: Build vocabulary (1773 unique terms from all 230 snippets)
Step 2: Create TF matrix — shape (230, 1773) — each row is a snippet, each column is a term
Step 3: Compute IDF — log(N / (1 + doc_freq)) for each term
Step 4: Boost high-value words — multiply IDF by 2 for important terms like "fork", "mutex"
Step 5: TF-IDF matrix = TF × IDF
Step 6: Normalize each row to unit length (for cosine similarity)
```

### Key NumPy Functions Used

| Function | What It Does |
|----------|-------------|
| `np.zeros((230, 1773), dtype=np.float32)` | Creates the empty TF matrix |
| `np.sum(tf_matrix > 0, axis=0)` | Counts how many documents contain each term (document frequency) |
| `np.log()` | Computes IDF weights |
| `np.linalg.norm(matrix, axis=1)` | Calculates vector lengths for normalization |
| `np.dot(tfidf_matrix, query_vector)` | Cosine similarity — one operation scores ALL 230 snippets at once |
| `np.argsort(similarities)[::-1][:top_k]` | Finds the top-K highest scoring snippets |

### The `score()` Function — How a Query is Matched

```python
def score(self, query_keywords, top_k=10):
    # 1. Build query vector (1773 dimensions, mostly zeros)
    query_vector[word_index] = 1.0  # for each keyword in the query

    # 2. Apply IDF weighting
    query_vector = query_vector * self._idf

    # 3. Normalize
    query_vector = query_vector / np.linalg.norm(query_vector)

    # 4. Cosine similarity with ALL documents (single dot product)
    similarities = np.dot(self._tfidf_matrix, query_vector)

    # 5. Return top-K results
    top_indices = np.argsort(similarities)[::-1][:top_k]
```

### How to Explain in Viva

> "I built the TF-IDF scoring system using NumPy. It creates a 230×1773 matrix where each row is a code snippet and each column is a keyword. IDF gives higher weight to rare, specific terms like 'semaphore' over common ones like 'for'. To find the best match for a user's query, I compute cosine similarity using `np.dot()` — this scores all 230 snippets in one vectorized operation, no loops needed. The matrix sparsity is 98% meaning most cells are zero, which is normal for text data."

---

## File 2: `src/analytics.py`

### Purpose
Analyzes session data and model statistics using Pandas DataFrames. Provides structured data for visualization.

### Library Used
**Pandas** — for tabular data manipulation, SQL queries, grouping, statistics

### Two Classes

#### `SessionAnalytics` — Analyzes User Behavior

| Function | What It Does | Pandas Used |
|----------|-------------|-------------|
| `get_session_dataframe()` | Loads all exchanges from SQLite into a DataFrame | `pd.read_sql_query()`, `pd.to_datetime()`, `.apply()` |
| `get_topic_distribution()` | Counts how many queries per topic | `.value_counts()`, `.reset_index()` |
| `get_language_distribution()` | Counts responses by language (Python/Bash/C) | `.value_counts()` |
| `get_usage_over_time()` | Groups queries by date | `.groupby()`, `.agg()` |
| `get_summary_stats()` | Overall stats (total queries, avg length, etc.) | `.mean()`, `.nunique()`, `.mode()` |

#### `ModelAnalytics` — Analyzes Training Corpus

| Function | What It Does | Pandas Used |
|----------|-------------|-------------|
| `get_corpus_dataframe()` | Converts 230 snippets to a DataFrame with columns | `pd.DataFrame(records)` |
| `get_corpus_summary()` | Stats: snippets per language, avg lines, total lines | `.value_counts().to_dict()`, `.mean()`, `.sum()` |
| `get_keyword_frequency()` | Top N most common keywords | `pd.Series(keywords).value_counts().head(n)` |

### Key Pandas Functions Used

| Function | What It Does |
|----------|-------------|
| `pd.read_sql_query(sql, conn)` | Loads SQL query result directly into a DataFrame |
| `pd.DataFrame(list_of_dicts)` | Creates DataFrame from a list of dictionaries |
| `df["col"].value_counts()` | Counts frequency of each unique value |
| `df.groupby("col").agg(...)` | Groups rows and computes aggregates (count, mean, sum) |
| `df["col"].apply(func)` | Applies a function to every row in a column |
| `df["col"].mean()` / `.sum()` / `.max()` | Basic statistics |
| `df["col"].nunique()` | Count of unique values |
| `df["col"].mode()` | Most frequent value |

### Example Output of `get_corpus_summary()`

```python
{
    "total_snippets": 230,
    "by_language": {"Python": 95, "Bash": 44, "C": 35},
    "avg_keywords_per_snippet": 33.3,
    "avg_code_lines": 28.2,
    "total_code_lines": 4901,
}
```

### How to Explain in Viva

> "I used Pandas to analyze both the training corpus and user session data. `SessionAnalytics` loads the SQLite database into a DataFrame using `pd.read_sql_query`, then computes topic distribution with `value_counts()` and usage over time with `groupby('date')`. `ModelAnalytics` converts our 230 snippets into a DataFrame and calculates stats like average code lines per language and the most frequent keywords. This data feeds into Matplotlib for visualization."

---

## File 3: `src/model_loader.py`

### Purpose
Loads the trained model from disk and provides the inference interface that the rest of the app uses.

### Key Functions

| Function | What It Does |
|----------|-------------|
| `load()` | Reads `models/markov_model.json`, creates MarkovModel and MarkovGenerator objects |
| `infer(prompt)` | Calls the generator's `generate_stream()` method, yields code line by line |
| `get_model_info()` | Returns model name and version metadata |

### How It Connects

```
main.py creates ModelLoader(config)
    → load() reads JSON file → creates MarkovModel → creates MarkovGenerator
    → MarkovGenerator initializes TFIDFScorer (NumPy)

main.py calls code_generator.generate(prompt, context)
    → code_generator calls model_loader.infer(context)
    → model_loader calls generator.generate_stream(prompt)
    → returns code line by line
```

### How to Explain in Viva

> "model_loader.py is the bridge between the application and the AI engine. It loads the JSON model file, creates the MarkovGenerator which internally builds the TF-IDF index using NumPy. The `infer()` method is a generator function — it yields code line by line for streaming output. If the model file is missing or corrupted, it raises a clear ModelLoadError."

---

## File 4: `train_model.py`

### Purpose
Builds the model from all training data sources. Run once to create `models/markov_model.json`.

### Data Sources It Collects From

| Source | What It Contains | Count |
|--------|-----------------|-------|
| `resources/training_corpus.py` | Python snippets (loops, functions, DSA, OOP) | 61 |
| `resources/shell_corpus.py` | Bash/Shell scripts (loops, functions, file ops, admin) | 41 |
| `resources/c_os_corpus.py` | C/OS code (fork, threads, IPC, sockets, semaphores) | 35 |
| `resources/docs/stdlib/*.md` | Reference documentation with code blocks | 39 |
| `Doc/*.md.txt` | Exam guides with embedded code examples | 54 |
| **Total** | | **230 snippets** |

### How Training Works

```
For each snippet:
    1. Extract all words from code + comments + description
    2. Remove stop words ("the", "is", "a", etc.)
    3. Store as: { "code": "...", "keywords": [...], "description": "..." }

Save all snippets to JSON file (256 KB)
```

### The `extract_code_from_markdown()` Function

Scans markdown files for code blocks tagged as python, bash, sh, c, or makefile:

```markdown
    ```c
    #include <stdio.h>
    int main() { ... }
    ```
```

It extracts the code and uses the nearest heading as the description.

### How to Explain in Viva

> "train_model.py collects code snippets from 5 sources — Python corpus, Shell corpus, C corpus, resource docs, and the Doc/ exam guides. For each snippet, it extracts keywords by removing stop words and tokenizing. The result is a JSON file with 230 indexed snippets. The `extract_code_from_markdown` function parses markdown files and pulls out code blocks tagged as python, bash, c, or makefile."

---

## File 5: `src/markov_engine.py`

### Purpose
The core retrieval engine. Given a user prompt, it finds the best matching code snippet using keyword scoring + TF-IDF cosine similarity.

### Key Classes

| Class | What It Does |
|-------|-------------|
| `MarkovModel` | Data container — holds snippets, transitions, starters. Loads/saves JSON. |
| `MarkovTrainer` | Builds the model from snippets — extracts keywords, stores indexed data |
| `MarkovGenerator` | The brain — scores snippets, detects language, returns best match |

### How `generate()` Works — The Core Algorithm

```
1. Extract keywords from user prompt (remove stop words)
2. Score all 230 snippets using keyword overlap:
   - 1 point per matching keyword
   - 3 points for high-value words (fork, mutex, grep, etc.)
   - Coverage bonus (more keywords matched = higher multiplier)
   - Code content bonus (keywords found in actual code)
3. Boost scores with TF-IDF cosine similarity (NumPy)
4. Apply language context (if prompt says "bash", penalize C snippets)
5. Return the highest-scoring snippet with minimal comments
```

### Language Detection Priority

```
C keywords checked FIRST: fork, exec, pthread, mutex, semaphore, malloc, gcc, 
                          shmget, msgget, semget, dup2, pipe, socket...
Shell keywords checked SECOND: bash, shell, grep, awk, sed, chmod, apt, cron...
Default: Python
```

### Integration with TF-IDF (NumPy)

```python
# In __init__:
self._tfidf_scorer = TFIDFScorer(model.snippets, _HIGH_VALUE_WORDS)

# In generate():
tfidf_results = self._tfidf_scorer.score(prompt_keywords, top_k=5)
# Boost keyword scores with TF-IDF cosine similarity
scored = [(score * (1.0 + tfidf_boost), snippet) for score, snippet in scored]
```

### How to Explain in Viva

> "markov_engine.py is the core. The `generate()` method extracts keywords from the prompt, scores all 230 snippets using weighted keyword overlap, then boosts the scores with TF-IDF cosine similarity from NumPy. It detects language context — if the prompt mentions 'fork' or 'mutex', it prioritizes C snippets and penalizes Bash/Python ones. The output is stripped of excessive comments to keep it clean."

---

## Files 6-8: Training Corpus Files

### `resources/training_corpus.py` — Python (61 snippets)

Topics: loops, functions, file I/O, classes, sorting algorithms, data structures (linked list, BST, heap, graph, trie), dynamic programming, backtracking, two pointer, sliding window

### `resources/shell_corpus.py` — Bash/Shell (41 snippets)

Topics: variables, arrays, loops, conditionals, functions, grep/awk/sed, file permissions, find, pipes, process management, cron, apt, systemctl, user management, networking, error handling, getopts, log file sorting, file organization

### `resources/c_os_corpus.py` — C/OS Concepts (35 snippets)

Topics: fork (basic, fan, chain), exec, zombie/orphan, pipes (one-way, two-way, dup2), pthreads, mutex, producer-consumer, semaphores (System V with semget/semop), reader-writer, dining philosophers, signals, shared memory (shmget/shmat), message queues (msgget/msgsnd/msgrcv), sockets (TCP/UDP), memory management, file descriptors, FIFO, barrier, LT2 complete solution, concurrent server

### How to Explain in Viva

> "The corpus files contain all the code the AI knows. Each snippet is a complete, working code example stored as a Python triple-quoted string. When `train_model.py` runs, it extracts keywords from each snippet and indexes them. The model has 230 total snippets covering Python DSA, Bash scripting, and C OS concepts like fork, threads, semaphores, and sockets."

---

## How Everything Connects — Ammar's Part in the Pipeline

```
train_model.py
    │
    ├── Reads training_corpus.py (61 Python snippets)
    ├── Reads shell_corpus.py (41 Bash snippets)
    ├── Reads c_os_corpus.py (35 C snippets)
    ├── Reads resources/docs/*.md (39 snippets)
    ├── Reads Doc/*.md.txt (54 snippets)
    │
    ▼
models/markov_model.json (230 snippets, 256 KB)
    │
    ▼
model_loader.py → load() → creates MarkovModel + MarkovGenerator
    │
    ▼
markov_engine.py → MarkovGenerator.__init__()
    │
    ├── Builds TF-IDF matrix using tfidf_scorer.py (NumPy)
    │       → 230 × 1773 matrix
    │       → IDF weights computed
    │       → High-value words boosted 2x
    │
    ▼
User asks "semaphore" → generate()
    │
    ├── Extract keywords: {"semaphore"}
    ├── Keyword scoring: loop through 230 snippets, compute overlap
    ├── TF-IDF boost: np.dot(tfidf_matrix, query_vector) → cosine similarity
    ├── Language detection: "semaphore" → C context → boost C snippets
    ├── Return top match with minimal comments
    │
    ▼
Output: System V semaphore code with semget/semop
```

---

## Quick Answers for Common Viva Questions

**Q: What is TF-IDF?**
> Term Frequency × Inverse Document Frequency. TF measures how often a word appears in one document. IDF measures how rare it is across all documents. Rare words get higher weight because they're more useful for distinguishing between snippets.

**Q: What is cosine similarity?**
> It measures the angle between two vectors. If two vectors point in the same direction, cosine = 1 (perfect match). If perpendicular, cosine = 0 (no match). We use `np.dot()` on normalized vectors to compute it.

**Q: Why NumPy instead of Python loops?**
> NumPy does the math in compiled C code internally. Scoring 230 snippets with a loop would need 230 iterations. With NumPy, `np.dot(matrix, vector)` does it in one operation — much faster.

**Q: What is the matrix shape (230, 1773)?**
> 230 rows = 230 code snippets. 1773 columns = 1773 unique keywords in our vocabulary. Each cell = the TF-IDF weight of that keyword for that snippet.

**Q: What is sparsity 98%?**
> 98% of the matrix cells are zero. This is normal — each snippet only uses ~30 keywords out of 1773 total. Sparse matrices are memory-efficient.

**Q: Why Pandas?**
> To analyze structured data. SQLite gives us raw rows — Pandas converts them to DataFrames where we can do `groupby`, `value_counts`, `mean` in one line. It also feeds data to Matplotlib for charts.

**Q: What does `pd.read_sql_query()` do?**
> It runs a SQL query on the SQLite database and returns the result directly as a Pandas DataFrame. No manual row-by-row processing needed.

**Q: How does the model file work?**
> It's a JSON file containing 230 objects. Each has `"code"` (the actual code), `"keywords"` (extracted terms), and `"description"` (first comment line). The model_loader reads this and builds the scoring index.

**Q: What are high-value words?**
> Technical terms that are very specific — like "fork", "mutex", "semaphore", "grep", "pthread". They get 2x IDF boost because matching them is a strong signal that we found the right snippet.

**Q: How does language detection work?**
> If the prompt contains C-specific words (fork, malloc, pthread, shmget), we boost C snippets and penalize Bash/Python ones. If it contains shell words (bash, grep, chmod), we boost shell snippets. This prevents "fork" from returning a Python snippet.

---

## How to Run Training

```bash
python train_model.py
```

Output:
```
Training Markov model...
  Adding 61 built-in Python snippets...
  Adding 41 shell/bash snippets...
  Adding 35 C/OS snippets...
  Adding 39 resource snippets...
  Adding 54 Doc/ guide snippets...

Model saved to: models/markov_model.json
  Size: 256.9 KB
  Snippets: 230
```
