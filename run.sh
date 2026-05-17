#!/usr/bin/env bash
set -e

echo "============================================"
echo "  Offline Coding AI Assistant - Starting..."
echo "============================================"

# Determine project root from script location
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

# Check for Python 3.10+ — try py, python3, python
PYTHON=""
for cmd in py python3 python; do
    if command -v "$cmd" &>/dev/null; then
        if "$cmd" -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null; then
            PYTHON="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "[ERROR] Could not find Python 3.10 or later."
    echo ""
    echo "Tried: py, python3, python - none worked."
    echo ""
    echo "Install Python 3.10+ from https://www.python.org/downloads/"
    echo ""
    echo "If Python is already installed, try running manually:"
    echo "  python3 main.py"
    echo "  python main.py"
    exit 1
fi

echo "Found Python: $PYTHON"
"$PYTHON" --version

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    "$PYTHON" -m venv .venv
fi

# Activate and install dependencies
source .venv/bin/activate
pip install -q -r requirements.txt

# Train model if it doesn't exist
if [ ! -f "models/markov_model.json" ]; then
    echo "Training the AI model (first run only)..."
    python train_model.py
fi

# Launch the application
echo "Starting the assistant..."
python main.py
