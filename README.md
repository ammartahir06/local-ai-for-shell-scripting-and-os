# Offline Coding AI Assistant

A self-contained, offline coding assistant for students. Ask questions in plain English, get working code back — no internet required. Supports **Python**, **Bash/Shell Scripting**, **Ubuntu System Administration**, and **C Operating System Concepts** (threading, fork, IPC, signals, sockets).

## How It Works

This project uses a **Markov chain / snippet-retrieval engine** with **TF-IDF vectorized scoring** — not a large language model. Here's the pipeline:

```
User Prompt → Keyword Extraction → TF-IDF Vectorization (NumPy) → Cosine Similarity → Best Match → Formatted Output
```

1. **Prompt Processing** — Validates input and classifies it as a coding request using keyword matching
2. **Keyword Extraction** — Strips stop words, identifies high-value technical terms
3. **TF-IDF Scoring (NumPy)** — Builds a term-document matrix and computes cosine similarity between the query vector and all snippet vectors using vectorized NumPy operations
4. **Intent Detection** — Determines if the prompt needs Python composition or snippet retrieval
5. **Snippet Scoring** — Combines keyword overlap scoring with TF-IDF cosine similarity for accurate retrieval
6. **Language Context Detection** — Identifies whether prompt asks for Python, Bash, or C
7. **Code Composition** — For simple Python patterns, composes code from detected intents
8. **Retrieval** — For complex requests, returns the best-matching pre-built snippet
9. **Formatting** — Applies language-appropriate formatting (PEP 8 for Python, proper indentation for Bash/C)
10. **Analytics (Pandas)** — Tracks session history, topic distribution, and usage patterns
11. **Visualization (Matplotlib)** — Generates charts for corpus statistics, TF-IDF heatmaps, and usage analytics
12. **Image Processing (OpenCV)** — Preprocesses code screenshots for OCR with adaptive thresholding, perspective correction, and structure analysis

The trained model is a small JSON file (~190 KB) containing **174 indexed code snippets** with extracted keywords. No GPU, no GGUF files needed.

## Topics Covered

### Python
- Loops, functions, file I/O, classes/OOP
- Sorting algorithms (bubble, merge, quick, heap, insertion, selection, counting)
- Data structures (linked list, doubly linked list, stack, queue, BST, heap, hash map, graph, trie)
- Dynamic programming (knapsack, LCS, coin change, edit distance, matrix chain)
- Backtracking (permutations, combinations, subsets, N-queens)
- Two pointer, sliding window techniques
- String operations, error handling, recursion

### Bash / Shell Scripting
- Variables, arrays, string operations
- Loops (for, while, until, select), conditionals (if/elif/else, case)
- Functions with local variables, return values, arithmetic
- Text processing (grep, awk, sed, cut, sort, uniq)
- File operations (find, chmod, chown, tar, rsync)
- Pipes, redirection, process substitution
- Error handling (set -e, trap, retry logic)
- Command-line argument parsing (getopts)
- Complete scripts: file organizers, calculators, number analysis, backup scripts

### Ubuntu System Administration
- Package management (apt, dpkg)
- Service management (systemctl, journalctl)
- User/group management (useradd, usermod, passwd)
- Cron jobs and scheduled tasks
- Disk usage monitoring (df, du, lsblk)
- Network configuration (ip, ss, ufw, iptables, ssh, scp)
- Process management (ps, top, kill, nice, nohup)
- Log analysis and system health checks

### C / Operating System Concepts
- Process creation (fork, exec, wait, waitpid)
- Zombie and orphan processes
- POSIX threads (pthread_create, pthread_join)
- Synchronization (mutex, semaphore, rwlock, barrier, condition variables)
- Classic problems (producer-consumer, reader-writer, dining philosophers)
- Inter-process communication (pipes, named pipes/FIFO, shared memory)
- Signal handling (signal, sigaction, SIGUSR1/SIGUSR2)
- Socket programming (TCP server/client, UDP server/client)
- Memory management (malloc, calloc, realloc, free)
- Low-level file I/O (open, read, write, lseek, file descriptors)
- Compilation (gcc flags, Makefile structure)

## AI/ML Concepts Used

| Concept | How It's Used | Library |
|---------|---------------|---------|
| **TF-IDF Vectorization** | Builds term-document matrix, computes IDF weights | NumPy |
| **Cosine Similarity** | Vectorized dot product between query and document vectors | NumPy |
| **N-gram Model** | Tokenizes code into n-grams for potential augmentation | stdlib |
| **Weighted Scoring** | High-value words get 2x IDF boost during matching | NumPy |
| **Keyword Extraction** | Stop-word removal + regex-based tokenization | stdlib |
| **Intent Classification** | Regex pattern matching to detect user intent | stdlib |
| **Retrieval-Based Generation** | Finds best-matching snippet from indexed corpus | NumPy |
| **Coverage Scoring** | Rewards snippets that match more prompt keywords | NumPy |
| **Language Context Detection** | Identifies whether prompt asks for Python, Bash, or C | stdlib |
| **Code Composition** | Builds Python functions from detected structural patterns | stdlib |
| **Session Analytics** | DataFrame analysis of usage patterns and topic frequency | Pandas |
| **Data Visualization** | Charts for corpus distribution, TF-IDF heatmaps, usage trends | Matplotlib |
| **Image Preprocessing** | Adaptive thresholding, morphological ops for code OCR | OpenCV |
| **Perspective Correction** | Warp transform for angled photos of code | OpenCV |
| **Structure Analysis** | Horizontal projection to estimate code lines/indentation | OpenCV + NumPy |

## Libraries Used

| Library | Version | Purpose |
|---------|---------|---------|
| **NumPy** | ≥1.24 | TF-IDF matrix operations, cosine similarity, vectorized scoring |
| **Pandas** | ≥2.0 | Session analytics, corpus statistics, topic frequency analysis |
| **Matplotlib** | ≥3.7 | Visualization of corpus distribution, TF-IDF heatmaps, usage charts |
| **OpenCV** | ≥4.8 | Image preprocessing for code screenshots (thresholding, perspective correction, contour detection) |
| **Rich** | ≥13.0 | Terminal UI with syntax highlighting, panels, spinners |
| **pyperclip** | ≥1.8 | Clipboard support (copy generated code) |
| **pytest** | — | Test framework |
| **hypothesis** | — | Property-based testing |

## Prerequisites

- **Python 3.10 or later**
- **NumPy**, **Pandas**, **Matplotlib**, **OpenCV** (installed via `pip install -r requirements.txt`)

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the model

```bash
python train_model.py
```

This builds `models/markov_model.json` from the training corpus (~174 snippets across Python, Bash, and C).

### 3. Run the assistant

**Windows** — double-click `run.bat` or from a terminal:

```cmd
run.bat
```

**macOS / Linux:**

```bash
chmod +x run.sh
./run.sh
```

The launcher script will automatically:
- Check your Python version
- Create a virtual environment (`.venv/`) on first run
- Install dependencies (`rich`, `pyperclip`)
- Start the assistant

### 4. Use it

Type a coding question in plain English and press Enter. Examples:

```
> Write a function that reads a CSV file and returns a list of dictionaries
> Write a bash script with sum_of_digits and multiplication_table functions
> Write a C program demonstrating fork and exec
> How to use grep awk sed for text processing
> Producer consumer problem using pthreads in C
```

Session context is maintained — follow-up questions reference your previous exchanges (up to 10).

### 5. Run model analysis (demonstrates all 4 libraries)

```bash
python analyze_model.py
```

This generates:
- **TF-IDF statistics** (NumPy) — vocabulary size, matrix sparsity, cosine similarity scores
- **Corpus analytics** (Pandas) — topic distribution, keyword frequency, session stats
- **Visualizations** (Matplotlib) — pie charts, bar charts, heatmaps, scatter plots saved to `output/charts/`
- **Image processing demo** (OpenCV) — creates a code image, applies preprocessing, analyzes structure

## Project Structure

```
├── run.bat / run.sh           # Launcher scripts (start here)
├── main.py                    # Application entry point
├── train_model.py             # Model training script
├── analyze_model.py           # Analysis & visualization (NumPy/Pandas/Matplotlib/OpenCV)
├── setup_check.py             # Pre-flight environment checker
├── config.json                # App configuration
├── requirements.txt           # Python dependencies
├── src/                       # Source code
│   ├── ui.py                  # Terminal UI (Rich)
│   ├── prompt_processor.py    # Input validation & classification
│   ├── code_generator.py      # Multi-language code formatting
│   ├── code_composer.py       # Intent-based Python code composition
│   ├── markov_engine.py       # Core retrieval engine (scoring, matching)
│   ├── tfidf_scorer.py        # TF-IDF vectorized scoring (NumPy)
│   ├── analytics.py           # Session & corpus analytics (Pandas)
│   ├── visualizer.py          # Chart generation (Matplotlib)
│   ├── image_processor.py     # Code image preprocessing (OpenCV)
│   ├── model_loader.py        # Model file loading
│   ├── session_manager.py     # Conversation history (SQLite)
│   ├── resource_store.py      # Documentation search
│   └── config.py              # Configuration dataclass
├── models/                    # Trained model (markov_model.json)
├── resources/                 # Training data & documentation
│   ├── training_corpus.py     # Python code snippets (61 snippets)
│   ├── shell_corpus.py        # Bash/Shell snippets (40 snippets)
│   ├── c_os_corpus.py         # C/OS concept snippets (26 snippets)
│   ├── docs/stdlib/           # Reference docs (Python, Bash, Ubuntu, C)
│   └── examples/              # Code examples by topic
├── output/                    # Generated output
│   ├── charts/                # Matplotlib visualizations (PNG)
│   └── processed/             # OpenCV processed images
├── tests/                     # Test suite (34 tests)
├── data/                      # Runtime data (SQLite session DB)
└── logs/                      # Application logs
```

## Configuration

Edit `config.json` to customize:

```json
{
    "model_filename": "markov_model.json",
    "model_dir": "models",
    "resource_dir": "resources",
    "data_dir": "data",
    "log_dir": "logs",
    "max_prompt_length": 2000,
    "max_context_pairs": 10,
    "response_timeout_seconds": 30
}
```

All directory paths are relative to the project root. The entire folder is portable.

## Running Tests

```bash
pip install pytest hypothesis
pytest
```

Tests cover prompt validation, session history, code formatting, resource search, path resolution, and context building. Includes property-based tests via Hypothesis.

## Adding New Snippets

To expand the assistant's knowledge:

1. Add snippets to the appropriate corpus file:
   - `resources/training_corpus.py` — Python
   - `resources/shell_corpus.py` — Bash/Shell/Ubuntu
   - `resources/c_os_corpus.py` — C/OS concepts

2. Each snippet should start with a descriptive comment (used for keyword matching):
   ```python
   '''
   #!/bin/bash
   # Process .txt files by word count - move to short/medium/long directories
   ...
   '''
   ```

3. Re-train the model:
   ```bash
   python train_model.py
   ```

4. Optionally add reference documentation in `resources/docs/stdlib/`

## Portability

The project is fully self-contained. Copy the entire folder to a USB drive, another machine, or zip it up — as long as Python 3.10+ is available, it just works. No Docker, no cloud, no GPU, no system-wide installs.

## How Each Library Is Used

### NumPy (`src/tfidf_scorer.py`)
- Builds a **term-document matrix** (174 snippets × 1773 terms) as a 2D NumPy array
- Computes **IDF (Inverse Document Frequency)** weights using `np.log()` and `np.sum()`
- Applies **high-value word boosting** by multiplying IDF values for important terms
- Normalizes document vectors using `np.linalg.norm()` for unit-length vectors
- Computes **cosine similarity** between query and all documents using `np.dot()` (vectorized)
- Finds top-K results using `np.argsort()` — no Python loops needed
- Used in `markov_engine.py` to boost snippet scoring during real-time inference

### Pandas (`src/analytics.py`)
- Loads session history from SQLite into a **DataFrame** using `pd.read_sql_query()`
- Enriches data with computed columns (word count, response lines, topic category, language)
- Computes **topic distribution** using `value_counts()` and percentage calculations
- Groups usage data by date using `groupby()` and `agg()` for time-series analysis
- Analyzes **keyword frequency** across the corpus using `pd.Series.value_counts()`
- Generates **corpus summary statistics** (mean, max, min, sum) per language
- Provides structured DataFrames to Matplotlib for visualization

### Matplotlib (`src/visualizer.py`)
- **Pie chart**: Snippet distribution by programming language (Python/Bash/C)
- **Bar chart**: Average code lines per snippet by language
- **Horizontal bar chart**: Top keywords in the training corpus with frequency
- **Heatmap**: TF-IDF weight matrix showing term importance across snippets
- **Scatter plot**: Snippet complexity (keywords vs code lines, colored by language)
- **Line chart**: Usage over time (queries per day)
- All charts saved as high-resolution PNG files in `output/charts/`

### OpenCV (`src/image_processor.py`)
- **Grayscale conversion**: `cv2.cvtColor()` for preprocessing
- **Gaussian blur**: `cv2.GaussianBlur()` for noise reduction
- **Adaptive thresholding**: `cv2.adaptiveThreshold()` for varying lighting conditions
- **Morphological operations**: `cv2.morphologyEx()` to clean text regions
- **Canny edge detection**: `cv2.Canny()` to find code block boundaries
- **Contour detection**: `cv2.findContours()` to locate code regions
- **Perspective transform**: `cv2.getPerspectiveTransform()` + `cv2.warpPerspective()` for angled photos
- **CLAHE contrast enhancement**: `cv2.createCLAHE()` for better text visibility
- **Horizontal projection analysis**: NumPy array operations on pixel rows to estimate line count
