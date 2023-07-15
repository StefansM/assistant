"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Assistant."""


if __name__ == "__main__":
    main(prog_name="assistant")  # pragma: no cover
