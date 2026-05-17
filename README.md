# Offline Coding AI Assistant

A self-contained, offline coding assistant for students. Ask questions in plain English, get working code back — no internet required. Supports **Python**, **Bash/Shell Scripting**, **Ubuntu System Administration**, and **C Operating System Concepts** (threading, fork, IPC, signals, sockets).

## How It Works

This project uses a **Markov chain / snippet-retrieval engine** — not a large language model. Here's the pipeline:

```
User Prompt → Keyword Extraction → Snippet Scoring → Best Match Retrieval → Formatted Output
```

1. **Prompt Processing** — Validates input and classifies it as a coding request using keyword matching
2. **Keyword Extraction** — Strips stop words, identifies high-value technical terms
3. **Intent Detection** — Determines if the prompt needs Python composition or snippet retrieval
4. **Snippet Scoring** — Scores all stored snippets using weighted keyword overlap, coverage bonus, language context detection, and code content matching
5. **Code Composition** — For simple Python patterns, composes code from detected intents (group-by, filter, sort, etc.)
6. **Retrieval** — For complex requests (algorithms, shell scripts, C programs), returns the best-matching pre-built snippet
7. **Formatting** — Applies language-appropriate formatting (PEP 8 for Python, proper indentation for Bash/C)

The trained model is a small JSON file (~190 KB) containing **174 indexed code snippets** with extracted keywords. No GPU, no GGUF files, no external ML libraries needed.

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

| Concept | How It's Used |
|---------|---------------|
| **N-gram Model** | Tokenizes code into n-grams for potential augmentation |
| **TF-IDF-like Scoring** | High-value words get 3x weight during matching |
| **Keyword Extraction** | Stop-word removal + regex-based tokenization |
| **Intent Classification** | Regex pattern matching to detect user intent |
| **Retrieval-Based Generation** | Finds best-matching snippet from indexed corpus |
| **Coverage Scoring** | Rewards snippets that match more of the prompt's keywords |
| **Language Context Detection** | Identifies whether prompt asks for Python, Bash, or C |
| **Code Composition** | Builds Python functions from detected structural patterns |
| **Template Matching** | Multi-word phrase matching in descriptions for precision |

## Libraries Used

| Library | Purpose |
|---------|---------|
| **rich** | Terminal UI with syntax highlighting, panels, spinners |
| **pyperclip** | Clipboard support (copy generated code) |
| **pytest** | Test framework |
| **hypothesis** | Property-based testing |

No external ML/AI libraries (no TensorFlow, PyTorch, transformers, or llama-cpp). The engine is **pure Python + stdlib**.

## Prerequisites

- **Python 3.10 or later** — the only system requirement

## Quick Start

### 1. Train the model

```bash
python train_model.py
```

This builds `models/markov_model.json` from the training corpus (~174 snippets across Python, Bash, and C).

### 2. Run the assistant

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

### 3. Use it

Type a coding question in plain English and press Enter. Examples:

```
> Write a function that reads a CSV file and returns a list of dictionaries
> Write a bash script with sum_of_digits and multiplication_table functions
> Write a C program demonstrating fork and exec
> How to use grep awk sed for text processing
> Producer consumer problem using pthreads in C
```

Session context is maintained — follow-up questions reference your previous exchanges (up to 10).

## Project Structure

```
├── run.bat / run.sh           # Launcher scripts (start here)
├── main.py                    # Application entry point
├── train_model.py             # Model training script
├── setup_check.py             # Pre-flight environment checker
├── config.json                # App configuration
├── requirements.txt           # Python dependencies
├── src/                       # Source code
│   ├── ui.py                  # Terminal UI (Rich)
│   ├── prompt_processor.py    # Input validation & classification
│   ├── code_generator.py      # Multi-language code formatting
│   ├── code_composer.py       # Intent-based Python code composition
│   ├── markov_engine.py       # Core retrieval engine (scoring, matching)
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
