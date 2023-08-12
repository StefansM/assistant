import dataclasses

import click

from assistant.cli import AppContext
from assistant.conversation.model import Conversation
from assistant.conversation.model import Message


@dataclasses.dataclass
class ConversationContext:
    app: AppContext
    conversation: Conversation


@click.command()
@click.option(
    "-p",
    "--prompt",
    type=(click.Choice(["system", "user", "assistant"]), str),
    multiple=True,
    help="Prompt to include in this",
)
@click.pass_context
def converse(ctx: click.Context, prompt: list[tuple[str, str]]) -> None:
    """Converse with ChatGPT.

    The Chat completions API is stateless, so every request must include the
    entire conversation history. This command allows you to specify the
    conversation history using the `--prompt` option. The prompt is a list of
    pairs, where the first element is the role of the message (either `system`,
    `user`, or `assistant`) and the second element is the content of the
    message. For example, the following prompt:

    \b
        --prompt system "Hello, world!" \\
        --prompt user "How are you?" \\
        --prompt assistant "I'm doing well, thanks!"

    will result in the following conversation:

    \b
        system: Hello, world!
        user: How are you?
        assistant: I'm doing well, thanks!

    """
    messages: list[Message] = []

    for message_type, content in prompt:
        if content.startswith("@"):
            with open(content[1:]) as f:
                content = f.read()

        messages.append(Message(role=message_type, content=content))

    app_ctx: AppContext = ctx.obj
    conversation = Conversation(
        model=app_ctx.model,
        messages=messages,
        temperature=app_ctx.temperature,
    )

    ctx.obj = ConversationContext(
        app=app_ctx,
        conversation=conversation,
    )

    response = conversation.request()
    print(response.choices[0].message.content)
