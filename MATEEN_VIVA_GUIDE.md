# Mateen's Viva Preparation Guide — Core Application Flow

---

## File 1: `main.py`

### Purpose
The entry point of the entire application. It loads everything, connects all components together, and starts the interactive loop.

### What It Does Step by Step

```
1. Load config.json (settings like model path, directories)
2. Setup logging
3. Load the trained model (markov_model.json)
4. Initialize all components (prompt processor, code generator, session manager, UI)
5. Create a new session
6. Start the UI loop — user types, system responds
```

### The `handle_prompt()` Function — The Heart of the App

This is the callback that runs every time the user types something:

```
User types prompt
    → validate (not empty, not too long)
    → check if it's a coding request
    → build context from session history
    → generate code (calls the model)
    → format the output
    → store in session history
    → display to user
```

### How to Explain in Viva

> "main.py is the entry point. It loads the config, initializes all components, and starts the interactive loop. The `handle_prompt` function is the core pipeline — it validates input, generates code using the model, formats it, stores it in session history, and displays it. Everything connects here."

---

## File 2: `src/ui.py`

### Purpose
The terminal interface — handles user input and displays output. Simple plain text, no fancy styling.

### Key Functions

| Function | What It Does |
|----------|-------------|
| `start_session()` | Main loop — reads input, calls the prompt handler, displays result |
| `display_welcome()` | Prints the welcome message with instructions |
| `get_prompt()` | Reads user input with `input(">>> ")` |
| `display_output()` | Prints the generated code (plain text, no borders) |
| `display_error()` | Prints error messages with `[ERROR]` prefix |
| `copy_to_clipboard()` | Uses pyperclip to copy last output to clipboard |

### How to Explain in Viva

> "ui.py is the terminal interface. It runs a while loop — reads user input, passes it to the handler, and prints the result. It supports 'exit' to quit and 'copy' to copy the last code to clipboard using pyperclip. The output is plain text with no borders or styling."

---

## File 3: `src/prompt_processor.py`

### Purpose
Validates user input and decides if it's a coding request.

### Key Functions

| Function | What It Does |
|----------|-------------|
| `validate()` | Checks prompt is not empty and under 2000 characters |
| `is_coding_request()` | Returns True for almost anything except greetings like "hi", "hello", "thanks" |
| `build_context()` | Combines current prompt with session history for context |

### How to Explain in Viva

> "prompt_processor.py validates input — rejects empty prompts and anything over 2000 characters. The `is_coding_request` function accepts almost any input since this is a coding tool. Only pure greetings like 'hi' or 'thanks' are rejected. `build_context` combines the current prompt with previous exchanges so the model has conversation history."

---

## File 4: `src/code_generator.py`

### Purpose
Formats the generated code output and detects which programming language it is.

### Key Functions

| Function | What It Does |
|----------|-------------|
| `generate()` | Calls the model to get code tokens |
| `detect_language()` | Checks if output is Python, Bash, or C based on content |
| `format_output()` | Applies language-appropriate formatting |
| `build_response()` | Combines code with references (uses `#` for Python/Bash, `//` for C) |

### Language Detection Logic

```
If code contains "#include" or "int main(" or "void "  → C
If code contains "#!/bin/bash" or "echo " or "fi"      → Bash
Otherwise                                               → Python
```

### How to Explain in Viva

> "code_generator.py handles the output formatting. It detects whether the generated code is Python, Bash, or C by looking for patterns like `#include` for C or `#!/bin/bash` for shell. Then it applies the right formatting — tabs to spaces, trailing whitespace removal. It also builds the final response with appropriate comment style for references."

---

## File 5: `src/code_composer.py`

### Purpose
For simple Python requests, it builds code from scratch using pattern matching instead of retrieving a stored snippet.

### How It Works

```
User prompt: "filter even numbers from a list"
    → Detect intent: "filter_even"
    → Detect input type: "list[int]"
    → Generate function name: "filter_items"
    → Build function body: return [x for x in items if x % 2 == 0]
    → Add usage example
```

### Key Functions

| Function | What It Does |
|----------|-------------|
| `compose_code()` | Main function — returns composed Python code or None |
| `_is_algorithm_request()` | Checks if prompt asks for a known algorithm (defer to retrieval) |
| `_is_non_python_request()` | Checks if prompt is for Bash/C (defer to retrieval) |
| `_detect_intents()` | Uses regex patterns to find what user wants (sort, filter, group, etc.) |
| `_extract_function_name()` | Derives a snake_case function name from the prompt |
| `_generate_body()` | Builds the function body based on detected intent |

### When It Activates vs When It Defers

| Prompt | What Happens |
|--------|-------------|
| "filter even numbers" | Composer handles it — builds Python function |
| "fork in c" | Defers to retrieval — `_is_non_python_request()` returns True |
| "merge sort" | Defers to retrieval — `_is_algorithm_request()` returns True |
| "bash script loop" | Defers to retrieval — "bash" is in non-Python indicators |

### How to Explain in Viva

> "code_composer.py handles simple Python requests by building code from patterns. It uses regex to detect intent — like 'filter', 'sort', 'group by', 'reverse'. Then it generates a complete function with the right name, parameters, body, and a usage example. For anything complex like algorithms, shell scripts, or C code, it returns None and lets the retrieval engine handle it."

---

## File 6: `src/session_manager.py`

### Purpose
Stores conversation history in a SQLite database so follow-up questions have context.

### Database Structure

```
Table: sessions
  - session_id (UUID)
  - created_at (timestamp)

Table: exchanges
  - id (auto-increment)
  - session_id (foreign key)
  - prompt (user's question)
  - response (generated code)
  - timestamp
```

### Key Functions

| Function | What It Does |
|----------|-------------|
| `new_session()` | Creates a new session, returns UUID |
| `add_exchange()` | Stores a prompt-response pair, keeps max 10 |
| `get_history()` | Returns last 10 exchanges in chronological order |
| `clear_session()` | Deletes all exchanges for a session |

### How to Explain in Viva

> "session_manager.py uses SQLite to store conversation history. Each session has a UUID. When the user asks a question, both the prompt and response are saved. `get_history` returns the last 10 exchanges so the model can use previous context. If it exceeds 10, the oldest is automatically deleted."

---

## File 7: `src/resource_store.py`

### Purpose
Loads and searches offline documentation from markdown files in the `resources/` folder.

### How It Works

```
On startup:
  1. Load resources/docs/index.json (topic → keyword mapping)
  2. Load all .md files from resources/docs/stdlib/
  3. Load all .md files from resources/examples/
  4. Index everything by topic keywords

On search:
  User prompt → extract words → match against topic index → return relevant docs
```

### Key Functions

| Function | What It Does |
|----------|-------------|
| `search()` | Finds resources matching keywords in the user's prompt |
| `get_topics()` | Lists all available topics |
| `_load_index()` | Reads index.json for keyword aliases |
| `_load_docs()` | Loads stdlib markdown files |
| `_load_examples()` | Loads example markdown files |

### How to Explain in Viva

> "resource_store.py provides offline documentation. It loads markdown files from the resources folder and indexes them by topic keywords. When a user asks about 'bash' or 'fork', it can find relevant documentation to include as references in the response. The index.json file maps topics to keyword aliases."

---

## File 8: `src/config.py`

### Purpose
Loads `config.json` and provides typed access to all settings with proper path resolution.

### What It Provides

| Property | Value |
|----------|-------|
| `model_path` | `models/markov_model.json` (resolved to absolute path) |
| `resource_path` | `resources/` directory |
| `database_path` | `data/sessions.db` |
| `log_path` | `logs/app.log` |
| `max_prompt_length` | 2000 characters |
| `max_context_pairs` | 10 exchanges |

### How to Explain in Viva

> "config.py reads config.json and resolves all paths relative to the project root. It provides a clean dataclass with properties like `model_path`, `database_path`, etc. This means the project is portable — you can move the folder anywhere and paths still work."

---

## How Everything Connects — The Full Pipeline

```
User types: "fork"
    │
    ▼
main.py → handle_prompt()
    │
    ▼
prompt_processor.py → validate() ✓ → is_coding_request() ✓
    │
    ▼
session_manager.py → get_history() → build_context()
    │
    ▼
code_generator.py → generate() → calls model_loader
    │
    ▼
markov_engine.py → extract keywords → score snippets → return best match
    │
    ▼
code_generator.py → detect_language("C") → format_output()
    │
    ▼
ui.py → display_output() → prints code to terminal
    │
    ▼
session_manager.py → add_exchange() → saves to SQLite
```

---

## Quick Answers for Common Viva Questions

**Q: What does main.py do?**
> It's the entry point. Loads config, model, and all components. Starts the interactive loop where user types prompts and gets code back.

**Q: How does the system know if it's Python, Bash, or C?**
> `code_generator.py` checks the output for patterns: `#include` = C, `#!/bin/bash` = Bash, otherwise Python.

**Q: What is the code composer?**
> It builds simple Python functions from patterns. If you say "filter even numbers", it detects the intent and generates a complete function. For complex stuff, it defers to the retrieval engine.

**Q: Why SQLite for sessions?**
> It's lightweight, needs no server, and the file is portable. It stores prompt-response pairs so follow-up questions have context.

**Q: What happens if the user types "hi"?**
> `is_coding_request()` returns False for greetings. The system responds with "Just type what you need. Example: fork in c, bash loop, linked list".

**Q: What is pyperclip used for?**
> It copies the last generated code to the system clipboard when the user types "copy". So they can paste it directly into their editor.

**Q: How does context work?**
> `session_manager` stores the last 10 exchanges. `build_context` combines them with the current prompt so the model can reference previous questions.

**Q: What if config.json is missing?**
> main.py catches the FileNotFoundError and prints a clear error message, then exits.

**Q: What does resource_store do?**
> It loads offline documentation (markdown files about bash, C, Python) and searches them by keyword. Matching docs can be added as references to the response.
