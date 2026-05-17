# Implementation Plan: Offline Coding AI Assistant

## Overview

Build a self-contained, offline Python coding AI assistant for students. The implementation follows a bottom-up approach: core utilities and data models first, then individual components, then wiring everything together with the UI layer. All code is Python, using llama-cpp-python for inference, Rich for the terminal UI, and SQLite for session storage.

## Tasks

- [x] 1. Set up project structure, configuration, and path utilities
  - [x] 1.1 Create project skeleton with directory structure and `requirements.txt`
    - Create `main.py`, `src/__init__.py`, `config.json`, `requirements.txt`
    - Create empty `models/`, `resources/docs/stdlib/`, `resources/examples/`, `data/`, `logs/` directories with `.gitkeep` files
    - Pin dependencies: `llama-cpp-python>=0.2.0`, `rich>=13.0.0`, `pyperclip>=1.8.0`
    - _Requirements: 1.1, 4.1_

  - [x] 1.2 Implement `src/path_utils.py` with `get_project_root()` and `resolve_path()`
    - `get_project_root()` derives root from the file's own location
    - `resolve_path(*parts)` joins parts relative to project root
    - All other components will import from this module
    - _Requirements: 1.1, 4.1_

  - [x] 1.3 Implement `src/config.py` with `AppConfig` dataclass and config loading
    - Define `AppConfig` with fields: `model_filename`, `model_dir`, `resource_dir`, `data_dir`, `log_dir`, `max_prompt_length`, `max_context_pairs`, `response_timeout_seconds`
    - Implement `model_path`, `resource_path`, `database_path`, `log_path` properties using `resolve_path`
    - Implement `AppConfig.load()` classmethod to read from `config.json`
    - Define custom exception types: `ModelLoadError`, `InferenceError`, `ResourceStoreError`
    - _Requirements: 1.1, 4.1_

  - [x] 1.4 Write property test for path resolution (Property 7)
    - **Property 7: All resolved paths are relative to project root**
    - Generate random AppConfig values with various relative directory names, verify all resolved paths start with project root
    - **Validates: Requirements 1.1, 4.1**

- [x] 2. Implement prompt processing and validation
  - [x] 2.1 Implement `src/prompt_processor.py` with `PromptProcessor` class
    - Implement `validate(prompt)` returning `ValidationResult` — accept non-empty, non-whitespace strings up to 2000 chars
    - Empty/whitespace-only → `ValidationResult(False, "Please enter a valid prompt.")`
    - Over 2000 chars → `ValidationResult(False, "Prompt exceeds the 2000 character limit. Your prompt is {length} characters.")`
    - Implement `build_context(prompt, session_history)` combining current prompt with history
    - Implement `is_coding_request(prompt)` with basic keyword heuristic
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 7.2_

  - [x] 2.2 Write property test for prompt validation (Property 1)
    - **Property 1: Prompt validation correctness**
    - Generate random strings (empty, whitespace, within limit, over limit) and verify validation accepts/rejects correctly
    - **Validates: Requirements 2.1, 2.2, 2.3**

  - [x] 2.3 Write property test for over-limit error message (Property 2)
    - **Property 2: Over-limit error message contains limit and actual length**
    - Generate strings > 2000 chars and verify error message contains "2000" and actual length
    - **Validates: Requirements 2.4**

  - [x] 2.4 Write property test for context building (Property 6)
    - **Property 6: Context building includes history and current prompt**
    - Generate random history lists and prompt strings, verify build_context output contains all text
    - **Validates: Requirements 7.2**

- [-] 3. Implement session manager with SQLite storage
  - [x] 3.1 Implement `src/session_manager.py` with `SessionManager` class
    - Initialize SQLite database at `<project_root>/data/sessions.db`, auto-create `data/` directory if missing
    - Implement `new_session()` returning a UUID session ID
    - Implement `add_exchange(session_id, prompt, response)` storing pairs, evicting oldest when exceeding 10
    - Implement `get_history(session_id)` returning up to 10 most recent exchanges in chronological order
    - Implement `clear_session(session_id)` removing all context for a session
    - Define `SessionData` and `Exchange` dataclasses
    - _Requirements: 7.1, 7.3, 7.4_

  - [x] 3.2 Write property test for session history retention (Property 5)
    - **Property 5: Session history retention with capacity limit**
    - Generate random sequences of 1–20 exchanges, add to session, verify history returns correct count and order
    - **Validates: Requirements 7.1, 7.3**

- [x] 4. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Implement model loader and code generator
  - [x] 5.1 Implement `src/model_loader.py` with `ModelLoader` class
    - Load GGUF model from `models/` directory using `llama-cpp-python`
    - Raise `ModelLoadError` with resolved file path and failure reason if model file is missing or corrupted
    - Implement `infer(prompt)` as a generator yielding streamed tokens
    - Implement `get_model_info()` returning model name/version dict
    - Log model name and version on successful load
    - _Requirements: 1.2, 1.4, 4.1, 4.2, 4.3, 4.4_

  - [x] 5.2 Implement `src/code_generator.py` with `CodeGenerator` class
    - Implement `generate(prompt, context)` streaming tokens from ModelLoader
    - Implement `format_output(raw_code)` applying PEP 8 formatting and ensuring inline comments
    - Implement `build_response(code, references)` combining code with documentation references
    - Handle `InferenceError` with user-friendly message suggesting restart
    - Handle non-coding prompts with descriptive message
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 4.4, 8.1_

  - [x] 5.3 Write property test for code formatting (Property 3)
    - **Property 3: Code formatting preserves valid Python and applies PEP 8**
    - Generate valid Python code snippets and verify format_output produces parseable PEP 8 output
    - **Validates: Requirements 3.3**

- [-] 6. Implement resource store
  - [x] 6.1 Implement `src/resource_store.py` with `ResourceStore` class
    - Load and index markdown files from `resources/docs/` and `resources/examples/`
    - Implement `search(query)` returning `ResourceEntry` items matched by topic keyword
    - Implement `get_topics()` listing all available topics
    - Raise `ResourceStoreError` if resource directory is missing
    - Return empty list when no matching resources found
    - Define `ResourceEntry` dataclass
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 6.2 Create sample offline resource files
    - Create `resources/docs/index.json` with topic index
    - Create sample stdlib docs: `resources/docs/stdlib/os.md`, `json.md`, `sys.md`
    - Create sample examples: `resources/examples/loops.md`, `file_io.md`, `classes.md`
    - _Requirements: 5.1, 5.2_

  - [X] 6.3 Write property test for resource search (Property 4)
    - **Property 4: Resource search returns topic-relevant entries**
    - Generate queries from known topic keywords and verify all results match the topic
    - **Validates: Requirements 5.3**

- [x] 7. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Implement user interface
  - [x] 8.1 Implement `src/ui.py` with `UserInterface` class using Rich
    - Implement `start_session()` launching the terminal UI and entering the input loop
    - Implement `display_welcome()` showing welcome message with usage instructions
    - Implement `get_prompt()` reading user input
    - Implement `display_output(code, references)` rendering code in a separated, scrollable output area
    - Implement `display_loading()` showing a spinner during generation
    - Implement `display_error(message)` for error display
    - Implement `copy_to_clipboard(text)` using pyperclip
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 8.2_

- [x] 9. Wire components together and implement main entry point
  - [x] 9.1 Implement `main.py` application entry point
    - Load `AppConfig` from `config.json`
    - Initialize all components: `ModelLoader`, `SessionManager`, `ResourceStore`, `PromptProcessor`, `CodeGenerator`, `UserInterface`
    - Wire the prompt → validate → build context → generate → format → display pipeline
    - Handle startup errors (missing config, missing model, missing resources) with clear messages
    - _Requirements: 1.1, 1.2, 1.3_

  - [x] 9.2 Create launcher scripts `run.bat` and `run.sh`
    - `run.bat`: Check Python, create `.venv`, install deps, launch `main.py`
    - `run.sh`: Check Python 3.10+, create `.venv`, install deps, launch `main.py`
    - Both scripts resolve paths relative to their own location
    - _Requirements: 1.1, 1.3_

  - [x] 9.3 Create `setup_check.py` pre-flight check script
    - Verify Python version >= 3.10
    - Verify required directories exist (`models/`, `resources/`)
    - Verify `config.json` is valid JSON
    - Verify model file exists at configured path
    - _Requirements: 1.1, 1.2, 1.4_

- [x] 10. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document using Hypothesis
- The model GGUF file must be manually placed in `models/` — it is not created by these tasks
