"""Offline Coding AI Assistant - Application Entry Point."""

import json
import logging
import sys

from src.config import AppConfig, ModelLoadError, ResourceStoreError


def main() -> None:
    """Launch the Offline Coding AI Assistant."""
    # --- Load configuration (before heavy imports) ---
    try:
        config = AppConfig.load()
    except FileNotFoundError:
        print("Error: config.json not found. Please ensure config.json exists in the project root.")
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"Error: config.json is not valid JSON. {exc}")
        sys.exit(1)

    # --- Configure logging ---
    logging.basicConfig(
        filename=config.log_path,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting Offline Coding AI Assistant")

    # --- Import heavy components after config is validated ---
    from src.code_generator import CodeGenerator
    from src.model_loader import ModelLoader
    from src.prompt_processor import PromptProcessor
    from src.resource_store import ResourceStore
    from src.session_manager import SessionManager
    from src.ui import UserInterface

    # --- Load model ---
    try:
        model_loader = ModelLoader(config)
        model_loader.load()
    except ModelLoadError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    # --- Initialize components ---
    try:
        resource_store = ResourceStore(config)
    except ResourceStoreError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    session_manager = SessionManager(config)
    prompt_processor = PromptProcessor()
    code_generator = CodeGenerator(model_loader)
    ui = UserInterface()

    # --- Create session ---
    session_id = session_manager.new_session()

    # --- Define the prompt callback ---
    def handle_prompt(user_input: str):
        """Process a user prompt through the full pipeline."""
        # Validate
        result = prompt_processor.validate(user_input)
        if not result.is_valid:
            ui.display_error(result.error_message)
            return ""

        # Check if it's a coding request
        if not prompt_processor.is_coding_request(user_input):
            return (
                "I couldn't interpret that as a coding request. "
                "Try asking me to write, explain, or fix Python code, "
                "shell scripts, Ubuntu commands, or C programs (threading, fork, etc.)."
            )

        # Build context from session history
        history = session_manager.get_history(session_id)
        context = prompt_processor.build_context(user_input, history)

        # Search for relevant resources — only include if strongly relevant
        resource_results = resource_store.search(user_input)
        # Only show references if the resource topic directly matches the prompt
        references = []
        prompt_lower = user_input.lower()
        for entry in resource_results:
            topic = entry.topic.lower().replace("_", " ")
            # Only include if the topic name appears as a distinct phrase in the prompt
            if topic in prompt_lower:
                references.append(entry.title)

        # Generate code via streaming
        tokens: list[str] = []
        for token in code_generator.generate(user_input, context):
            tokens.append(token)

        raw_code = "".join(tokens)
        formatted = code_generator.format_output(raw_code)
        response = code_generator.build_response(formatted, references)

        # Store exchange in session
        session_manager.add_exchange(session_id, user_input, response)

        return response

    # --- Start the UI loop ---
    logger.info("All components initialized. Starting UI session.")
    ui.start_session(on_prompt=handle_prompt)


if __name__ == "__main__":
    main()
