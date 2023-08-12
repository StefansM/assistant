import dataclasses
import os

import click
import openai
import tiktoken
from dotenv import load_dotenv

import assistant.model


@dataclasses.dataclass
class AppContext:
    model: str
    max_tokens: int
    temperature: float
    tokenizer: tiktoken.Encoding


@click.group()
@click.version_option()
@click.option(
    "--model",
    type=str,
    help="Transformer model",
    default="gpt-3.5-turbo",
)
@click.option(
    "-t",
    "--temperature",
    type=float,
    help="Model temperature",
    default=1.0,
)
@click.pass_context
def main(
    ctx: click.Context,
    model: str,
    temperature: float,
) -> None:
    """Coding assistant, using OpenAI's APIs to generate code."""
    # During development, the OpenAPI key can be stored in a .env file.
    load_dotenv()
    if key := os.getenv("OPENAI_API_KEY"):
        openai.api_key = key

    tokenizer = tiktoken.encoding_for_model(model)

    ctx.obj = AppContext(
        model=model,
        max_tokens=assistant.model.MAX_TOKENS[model],
        temperature=temperature,
        tokenizer=tokenizer,
    )


@main.command()
def list_models() -> None:
    """List available OpenAI models."""
    print("Available models:")
    models = sorted(openai.Model.list()["data"], key=lambda m: m["id"])  # type: ignore
    for model in models:
        print(f"  {model['id']}")
