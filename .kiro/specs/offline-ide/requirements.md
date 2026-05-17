# Requirements Document

## Introduction

This document defines the requirements for building an offline AI-powered IDE by forking Code - OSS (the open-source base of VS Code) and integrating the existing Python-based Markov chain / retrieval AI engine as a local backend. The architecture mirrors how Cursor, Kiro, and Windsurf extend VS Code — a custom VS Code extension communicates with a Python backend server running on localhost. All AI features operate fully offline with zero cloud API calls.

The system consists of three deliverables: (1) a Python backend server wrapping the existing AI engine behind an HTTP/WebSocket API, (2) a VS Code extension providing inline completion, AI chat, code explanation, and refactoring commands, and (3) build/packaging scripts that fork Code - OSS and bundle the extension and Python backend into a single distributable application.

## Glossary

- **IDE**: The forked Code - OSS application bundled with the AI extension and Python backend — the top-level offline IDE product.
- **Backend_Server**: A Python HTTP/WebSocket server (Flask or FastAPI) that wraps the existing AI engine and exposes it on localhost.
- **Extension**: The VS Code extension that integrates with the Backend_Server to provide AI features inside the editor.
- **AI_Engine**: The existing Markov chain / retrieval-based code generation engine (MarkovGenerator + CodeComposer + CodeGenerator) that powers all AI features.
- **Completion_Provider**: The Extension component registered as a VS Code InlineCompletionItemProvider that supplies AI-powered code completions.
- **Chat_Participant**: The Extension component registered as a VS Code Chat Participant that provides conversational AI interaction in the editor's chat panel.
- **Session_Manager**: The existing component that persists conversation history in SQLite, accessed through the Backend_Server.
- **Resource_Store**: The existing component that provides offline documentation and example lookup, accessed through the Backend_Server.
- **Prompt_Processor**: The existing component that validates prompts and builds conversational context, used by the Backend_Server.
- **Build_System**: The scripts and configuration that fork Code - OSS, bundle the Extension and Backend_Server, and produce a distributable application.

## Requirements

### Requirement 1: Python Backend Server

**User Story:** As a developer, I want the existing AI engine exposed as a local HTTP/WebSocket server, so that the VS Code extension can communicate with it over a well-defined API.

#### Acceptance Criteria

1. THE Backend_Server SHALL expose an HTTP REST API on a configurable localhost port (default 18080) using Flask or FastAPI.
2. THE Backend_Server SHALL provide a `POST /api/completions` endpoint that accepts a JSON body containing `file_content`, `cursor_line`, `cursor_column`, and `language` fields and returns a JSON response containing a `suggestion` string.
3. THE Backend_Server SHALL provide a `POST /api/chat` endpoint that accepts a JSON body containing `prompt`, `session_id`, and optional `file_context` fields and returns a JSON response containing `response` and `references` fields.
4. THE Backend_Server SHALL provide a `POST /api/explain` endpoint that accepts a JSON body containing `code` and optional `file_context` fields and returns a JSON response containing an `explanation` string.
5. THE Backend_Server SHALL provide a `POST /api/refactor` endpoint that accepts a JSON body containing `code`, `refactor_type`, and optional `full_source` fields and returns a JSON response containing `refactored_code` and `description` fields.
6. THE Backend_Server SHALL provide a `GET /api/health` endpoint that returns HTTP 200 with a JSON body containing `status`, `model_loaded`, and `version` fields.
7. THE Backend_Server SHALL provide a `POST /api/sessions` endpoint to create a new session and return a `session_id`, and a `DELETE /api/sessions/{session_id}` endpoint to clear session history.
8. WHEN the Backend_Server starts, THE Backend_Server SHALL load the Markov model from `models/markov_model.json` using the existing ModelLoader and report readiness on stdout.
9. IF the Markov model file is missing or corrupted, THEN THE Backend_Server SHALL log the error and exit with a non-zero exit code.
10. THE Backend_Server SHALL use the existing PromptProcessor to validate all incoming prompts and return HTTP 400 with a descriptive error message for invalid prompts.
11. THE Backend_Server SHALL use the existing SessionManager to persist and retrieve conversation history for chat interactions.
12. THE Backend_Server SHALL use the existing ResourceStore to include relevant documentation references in chat and explanation responses.
13. THE Backend_Server SHALL accept only connections from localhost (127.0.0.1 / ::1) and reject connections from external network addresses.
14. IF the AI_Engine raises an error during inference, THEN THE Backend_Server SHALL return HTTP 500 with a JSON body containing an `error` field describing the failure.

### Requirement 2: Backend Server API Request and Response Serialization

**User Story:** As a developer, I want the API request and response formats to be well-defined and parseable, so that the extension can reliably communicate with the backend.

#### Acceptance Criteria

1. THE Backend_Server SHALL accept request bodies as JSON with `Content-Type: application/json` and return response bodies as JSON with `Content-Type: application/json`.
2. THE Backend_Server SHALL validate that all required fields are present in each request body and return HTTP 400 with a descriptive `error` field for missing or malformed fields.
3. FOR ALL valid API request JSON payloads, serializing the request to JSON and deserializing it back SHALL produce an equivalent object (round-trip property).
4. FOR ALL valid API response objects, serializing to JSON and deserializing back SHALL produce an equivalent object (round-trip property).

### Requirement 3: VS Code Extension — Inline Code Completion

**User Story:** As a developer, I want AI-powered inline code completions as I type, so that I can write code faster with contextual suggestions.

#### Acceptance Criteria

1. THE Extension SHALL register an InlineCompletionItemProvider with VS Code for all file types.
2. WHEN VS Code triggers an inline completion request, THE Completion_Provider SHALL send the current file content, cursor line, cursor column, and language identifier to the Backend_Server `POST /api/completions` endpoint.
3. WHEN the Backend_Server returns a non-empty suggestion, THE Completion_Provider SHALL return it as an InlineCompletionItem positioned at the current cursor location.
4. WHEN the Backend_Server returns an empty suggestion, THE Completion_Provider SHALL return an empty completion list.
5. IF the Backend_Server is unreachable or returns an error, THEN THE Completion_Provider SHALL return an empty completion list without displaying an error to the user.
6. THE Completion_Provider SHALL include a cancellation token check and abort the request if the user continues typing before the response arrives.

### Requirement 4: VS Code Extension — AI Chat Panel

**User Story:** As a developer, I want an AI chat panel in VS Code, so that I can ask coding questions and get AI-generated answers without leaving the editor.

#### Acceptance Criteria

1. THE Extension SHALL register a Chat Participant with VS Code that appears in the editor's built-in chat panel.
2. WHEN the user submits a message to the Chat_Participant, THE Extension SHALL send the prompt, session ID, and the content of the currently active editor file to the Backend_Server `POST /api/chat` endpoint.
3. WHEN the Backend_Server returns a response, THE Chat_Participant SHALL display the response text in the chat panel.
4. WHEN the Backend_Server response contains code blocks (delimited by triple backticks), THE Chat_Participant SHALL render them with syntax highlighting.
5. THE Extension SHALL create a new backend session via `POST /api/sessions` when the extension activates and store the session ID for subsequent chat requests.
6. THE Extension SHALL persist the session ID across VS Code window reloads using VS Code workspace state storage.
7. WHEN the user triggers the "Clear AI Chat History" command, THE Extension SHALL call `DELETE /api/sessions/{session_id}` on the Backend_Server and start a new session.
8. IF the Backend_Server is unreachable, THEN THE Chat_Participant SHALL display an error message indicating the backend is not running and suggest restarting the IDE.

### Requirement 5: VS Code Extension — Code Explanation Command

**User Story:** As a developer, I want to select code and ask the AI to explain it, so that I can understand unfamiliar code in my project.

#### Acceptance Criteria

1. THE Extension SHALL register a command `offlineIDE.explainCode` accessible from the editor context menu and the command palette.
2. WHEN the user triggers the "Explain Code" command with a text selection active, THE Extension SHALL send the selected code and the full file content to the Backend_Server `POST /api/explain` endpoint.
3. WHEN the Backend_Server returns an explanation, THE Extension SHALL display the explanation in the chat panel as a new message.
4. IF no text is selected when the user triggers the "Explain Code" command, THEN THE Extension SHALL display an information message instructing the user to select code first.
5. IF the Backend_Server is unreachable or returns an error, THEN THE Extension SHALL display an error notification describing the failure.

### Requirement 6: VS Code Extension — Code Refactoring Command

**User Story:** As a developer, I want AI-assisted refactoring suggestions, so that I can improve my code structure with guidance.

#### Acceptance Criteria

1. THE Extension SHALL register a command `offlineIDE.refactorCode` accessible from the editor context menu and the command palette.
2. WHEN the user triggers the "Refactor Code" command with a text selection active, THE Extension SHALL present a quick-pick menu with refactoring options: "Rename Symbol", "Extract Function", and "Extract Variable".
3. WHEN the user selects a refactoring option, THE Extension SHALL send the selected code, the refactoring type, and the full file content to the Backend_Server `POST /api/refactor` endpoint.
4. WHEN the Backend_Server returns refactored code, THE Extension SHALL open a diff editor showing the original code alongside the proposed refactored code.
5. WHEN the user accepts the refactoring from the diff view, THE Extension SHALL apply the refactored code to the active editor by replacing the selected text.
6. IF no text is selected when the user triggers the "Refactor Code" command, THEN THE Extension SHALL display an information message instructing the user to select code first.
7. IF the Backend_Server returns an error or indicates no applicable refactoring, THEN THE Extension SHALL display an information message explaining that no refactoring is applicable.

### Requirement 7: VS Code Extension — Backend Connection Management

**User Story:** As a developer, I want the extension to manage the connection to the Python backend reliably, so that AI features work seamlessly when the backend is running.

#### Acceptance Criteria

1. WHEN the Extension activates, THE Extension SHALL attempt to connect to the Backend_Server by calling `GET /api/health` on the configured localhost port.
2. WHEN the health check succeeds, THE Extension SHALL set a status bar item to display "AI: Online" with a green indicator.
3. WHEN the health check fails, THE Extension SHALL set the status bar item to display "AI: Offline" with a red indicator.
4. THE Extension SHALL retry the health check every 10 seconds while the backend is unreachable, up to a maximum of 30 retries.
5. THE Extension SHALL read the backend port from a VS Code setting `offlineIDE.backendPort` with a default value of 18080.
6. WHEN the backend transitions from unreachable to reachable, THE Extension SHALL update the status bar to "AI: Online" and enable all AI commands.
7. WHILE the backend is unreachable, THE Extension SHALL disable AI commands (completion, chat, explain, refactor) and display a warning when the user attempts to use them.

### Requirement 8: Build and Packaging System

**User Story:** As a developer, I want a single build command that produces a distributable offline IDE application, so that end users can install and run the IDE without manual setup.

#### Acceptance Criteria

1. THE Build_System SHALL provide a build script (`scripts/build.sh` for Linux/macOS, `scripts/build.ps1` for Windows) that clones the Code - OSS repository at a pinned commit hash.
2. THE Build_System SHALL apply custom branding (application name, icon, about text) to the forked Code - OSS build via product.json modifications.
3. THE Build_System SHALL compile the VS Code extension from TypeScript source in `extension/` and package it as a `.vsix` file.
4. THE Build_System SHALL bundle the Python backend (all `src/` modules, `models/`, `resources/`, `config.json`, and `requirements.txt`) into the application package.
5. THE Build_System SHALL include a Python virtual environment with all backend dependencies pre-installed in the application package.
6. THE Build_System SHALL configure the forked Code - OSS to auto-install the bundled extension on first launch.
7. THE Build_System SHALL configure a launch script that starts the Backend_Server process before launching the Code - OSS editor, and terminates the Backend_Server when the editor exits.
8. THE Build_System SHALL produce platform-specific distributable artifacts: `.tar.gz` for Linux, `.dmg` for macOS, and `.zip` for Windows.
9. IF the Code - OSS clone or build fails, THEN THE Build_System SHALL exit with a non-zero exit code and print a descriptive error message.

### Requirement 9: Extension Command Contributions and Keybindings

**User Story:** As a developer, I want keyboard shortcuts and command palette entries for all AI features, so that I can access them quickly.

#### Acceptance Criteria

1. THE Extension SHALL register the following commands in its `package.json` contribution: `offlineIDE.explainCode`, `offlineIDE.refactorCode`, `offlineIDE.clearChat`, and `offlineIDE.restartBackend`.
2. THE Extension SHALL assign default keybindings: `Ctrl+Shift+E` for Explain Code, `Ctrl+Shift+R` for Refactor Code, and `Ctrl+Shift+L` for Clear Chat.
3. WHEN the user triggers the `offlineIDE.restartBackend` command, THE Extension SHALL send a restart signal to the Backend_Server process and re-run the health check sequence.
4. THE Extension SHALL contribute a context menu group "Offline AI" in the editor context menu containing the Explain Code and Refactor Code commands.
5. THE Extension SHALL contribute all commands to the VS Code command palette with descriptive titles prefixed with "Offline AI:".

### Requirement 10: Offline Guarantee

**User Story:** As a developer, I want the IDE to function entirely offline, so that I can use AI features without any internet connection.

#### Acceptance Criteria

1. THE Backend_Server SHALL operate without making any outbound network requests during startup or inference.
2. THE Extension SHALL communicate exclusively with localhost addresses (127.0.0.1 or ::1) and make no outbound network requests.
3. THE Build_System SHALL include all required dependencies (Python packages, Node modules, model files, resource files) in the distributable package so that no downloads are needed at runtime.
4. WHEN the IDE is launched on a machine with no network connectivity, THE IDE SHALL start successfully and all AI features SHALL function normally.
