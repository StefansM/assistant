# Assistant

_WIP: This project is a work in progress, and will change without warning.
At the moment, it's just a testbed for experimentation with the OpenAI API._

```
Usage: assistant [OPTIONS] COMMAND [ARGS]...

  Coding assistant, using OpenAI's APIs to generate code.

Options:
  --version                Show the version and exit.
  --model TEXT             Transformer model
  -t, --temperature FLOAT  Model temperature
  --help                   Show this message and exit.

Commands:
  add-docstrings  Add docstrings to Python modules, classes and functions.
  converse        Converse with ChatGPT.
  list-models     List available OpenAI models.
```

## Features

## Requirements

- TODO

## Installation

You can install _Assistant_ via [pip] from [PyPI]:

```console
$ pip install assistant
```

## Usage

Please see the [Command-line Reference] for details.

## License

Distributed under the terms of the [MIT license][license],
_Assistant_ is free and open source software.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/stefansm/assistant/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/stefansm/assistant/blob/main/LICENSE
[command-line reference]: https://assistant.readthedocs.io/en/latest/usage.html
