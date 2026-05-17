# Offline Coding AI Assistant

A self-contained, offline Python coding assistant for students. Ask questions in plain English, get Python code back — no internet required.

## Prerequisites

- **Python 3.10 or later** — the only system requirement
- A **GGUF model file** (e.g., `codellama-7b-instruct.Q4_K_M.gguf`)

## Quick Start

### 1. Get the model

Download a GGUF model (such as CodeLlama 7B Instruct Q4_K_M) and place it in the `models/` directory:

```
models/codellama-7b-instruct.Q4_K_M.gguf
```

The expected filename is configured in `config.json` under `model_filename`. Change it there if your file has a different name.

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
- Install dependencies (`llama-cpp-python`, `rich`, `pyperclip`)
- Start the assistant

### 3. Use it

Type a coding question in plain English and press Enter. For example:

```
> Write a function that reads a CSV file and returns a list of dictionaries
```

The assistant will generate Python code with inline comments and PEP 8 formatting. You can copy the output to your clipboard directly from the UI.

Session context is maintained — follow-up questions reference your previous exchanges (up to 10).

## Pre-flight Check

Run the setup checker to verify everything is in place before launching:

```bash
python setup_check.py
```

This validates:
- Python version
- Required directories (`models/`, `resources/`)
- `config.json` is valid
- Model file exists

## Project Structure

```
├── run.bat / run.sh       # Launcher scripts (start here)
├── main.py                # Application entry point
├── setup_check.py         # Pre-flight environment checker
├── config.json            # App configuration (all paths are relative)
├── requirements.txt       # Python dependencies
├── src/                   # Source code
│   ├── ui.py              # Terminal UI (Rich)
│   ├── prompt_processor.py
│   ├── code_generator.py
│   ├── model_loader.py
│   ├── session_manager.py
│   └── resource_store.py
├── models/                # Place your GGUF model file here
├── resources/             # Offline docs and code examples
│   ├── docs/stdlib/       # Python stdlib reference (markdown)
│   └── examples/          # Code examples by topic
├── data/                  # Runtime data (SQLite session DB, auto-created)
└── logs/                  # Application logs (auto-created)
```

## Configuration

Edit `config.json` to customize:

```json
{
    "model_filename": "codellama-7b-instruct.Q4_K_M.gguf",
    "model_dir": "models",
    "resource_dir": "resources",
    "data_dir": "data",
    "log_dir": "logs",
    "max_prompt_length": 2000,
    "max_context_pairs": 10,
    "response_timeout_seconds": 30
}
```

All directory paths are relative to the project root. The entire folder is portable — move or rename it freely.

## Running Tests

```bash
pip install pytest hypothesis
pytest
```

Tests include property-based tests (via Hypothesis) covering prompt validation, session history, code formatting, resource search, path resolution, and context building.

## Portability

The project is fully self-contained. Copy the entire folder to a USB drive, another machine, or zip it up — as long as Python 3.10+ is available, it just works. No Docker, no cloud, no system-wide installs.
