import pathlib

import click
import tiktoken

import assistant.cli
import assistant.coding.model
from assistant.coding.applier import ApplierMode
from assistant.coding.applier import DocstringApplier
from assistant.coding.iterator import FileIterator
from assistant.coding.iterator import RepositoryIterator
from assistant.coding.sanitizer import ResponseSanitizer
from assistant.conversation.model import Conversation
from assistant.conversation.model import Message


def iterate_single_file(
    model: str, tokenizer: tiktoken.Encoding, max_tokens: int, file_path: pathlib.Path
) -> str:
    file_iterator = FileIterator(file_path)

    directives = [
        "Add docstrings to this code, where necessary.",
        "Use the Google docstring convention.",
        "Elide the code itself. Only return function signatures and docstrings.",
    ]

    sanitizer = ResponseSanitizer()

    for node in file_iterator.iterate():
        node_text = node.code_snippet or node.combine_child_code()

        if not node_text:
            continue

        message = Message(
            "user",
            " ".join(directives) + "\n\n✂✂✂✂✂✂✂✂✂✂✂\n\n" + node_text,
        )
        node_tokens = tokenizer.encode(message.content)

        if len(node_tokens) < max_tokens:
            conversation = Conversation(model, [message])
            response = conversation.request()
            response_text = response.choices[0].message.content
            sanitized_text = sanitizer.sanitize(response_text)

            applier = DocstringApplier(node_text, ApplierMode.KEEP)
            reformatted_text = applier.apply(sanitized_text)
            return reformatted_text
        else:
            raise Exception(
                "Node too large to process. If necessary, we could split it up but I"
                "haven't had a need yet. Let me know if you need this feature."
            )

    raise Exception("No docstring nodes found in file")


@click.command()
@click.argument(
    "repo_root",
    type=click.Path(
        exists=True,
        dir_okay=True,
        file_okay=True,
        path_type=pathlib.Path,  # type: ignore
    ),
)
@click.option(
    "-i",
    "--inplace",
    is_flag=True,
    help="Overwrite the file in-place.",
    default=False,
)
@click.pass_context
def add_docstrings(ctx: click.Context, repo_root: pathlib.Path, inplace: bool) -> None:
    """Add docstrings to Python modules, classes and functions.

    REPO_ROOT: Either a single Python file or a directory containing Python files.
    """
    app_context: assistant.cli.AppContext = ctx.obj

    if repo_root.is_file():
        reformatted_text = iterate_single_file(
            app_context.model,
            app_context.tokenizer,
            app_context.max_tokens,
            repo_root,
        )
        if inplace:
            repo_root.write_text(reformatted_text)
        else:
            print(f"FILE: {repo_root}")
            print(reformatted_text)

    else:
        file_iterator = RepositoryIterator(repo_root)
        for file_path in file_iterator.iterate():
            try:
                reformatted_text = iterate_single_file(
                    app_context.model,
                    app_context.tokenizer,
                    app_context.max_tokens,
                    file_path,
                )
                if inplace:
                    file_path.write_text(reformatted_text)
                else:
                    print(f"FILE: {file_path}")
                    print(reformatted_text)
            except Exception as e:
                print(f"ERROR: {file_path}")
                print(e)
