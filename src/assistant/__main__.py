"""Command-line interface to coding assistant."""
import assistant.coding.cli
import assistant.conversation.cli
from assistant.cli import main


# Register subcommands.
main.add_command(assistant.conversation.cli.converse)
main.add_command(assistant.coding.cli.add_docstrings)

if __name__ == "__main__":
    main(prog_name="assistant")  # pragma: no cover
