<p align="center">
  <img alt="hexdoc logo" src="https://github.com/hexdoc-dev/hexdoc/raw/main/media/hexdoc.svg" height="200" />
  <br /><br />
  <a href="https://hexdoc.hexxy.media/"><img alt="Docs - hexdoc.hexxy.media" src="https://img.shields.io/badge/docs-hexdoc.hexxy.media-darkmagenta"></a>
  <a href="https://pypi.org/project/hexdoc/"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/hexdoc"></a>
  <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/hexdoc">
  <a href="https://github.com/hexdoc-dev/hexdoc/actions/workflows/ci.yml"><img alt="GitHub Workflow Status (with event)" src="https://img.shields.io/github/actions/workflow/status/hexdoc-dev/hexdoc/ci.yml?logo=github&label=ci"></a>
  <a href="https://github.com/hexdoc-dev/hexdoc#badges"><img src="https://img.shields.io/endpoint?url=https://hexxy.media/api/v0/badge/hexdoc" alt="hexdoc" style="max-width:100%;"></a>
</p>

# hexdoc

A [Jinja](https://jinja.palletsprojects.com/en/3.1.x/)-based documentation generator for [Patchouli](https://github.com/VazkiiMods/Patchouli) books.

This is the library that powers [Hex Casting](https://github.com/gamma-delta/HexMod)'s web book.

## Plugins

See [hexdoc-hexcasting-template](https://github.com/hexdoc-dev/hexdoc-hexcasting-template) for instructions to set up a hexdoc plugin for a pre-existing Hex Casting addon.

## Contributing

### Setup

```sh
git submodule update --init

python3.11 -m venv venv

.\venv\Scripts\activate   # Windows
. venv/bin/activate.fish  # fish
source venv/bin/activate  # everything else

pip install -e .[dev]
pre-commit install
```

### Usage

For local testing, create a file called `.env` in the repo root following this template:
```sh
GITHUB_SHA=main
GITHUB_REPOSITORY=hexdoc-dev/hexdoc
GITHUB_PAGES_URL=https://hexdoc.hexxy.media
```

Useful commands:
```sh
# show help
hexdoc -h

# serve hexdoc resources locally
# this is useful if serving other books locally that depend on hexdoc resources
nodemon --exec "hexdoc serve --port 8001 --no-merge"

# render and serve the Hex Casting web book in watch mode
nodemon

# start the Python interpreter with some extra local variables
hexdoc repl

# run tests
pytest  # fast, skips Cookiecutter
nox  # slow, full test suite in an isolated venv
nox --no-install  # after the first Nox run, use this to skip reinstalling everything

# update test snapshots (only running sessions with the tag "test")
nox -t test -- --snapshot-update

# run hexdoc commands in an isolated environment to ensure it works on its own
nox -s hexdoc -- build
nox -s hexdoc -- repl

# set up a dummy book for local testing
nox -s dummy_setup
nox -s dummy_serve

nox -s dummy_hexdoc -- build

nox -s dummy_clean
```

## Badges

<a href="https://github.com/hexdoc-dev/hexdoc"><img src="https://img.shields.io/endpoint?url=https://hexxy.media/api/v0/badge/hexdoc" alt="hexdoc" style="max-width:100%;"></a>
<a href="https://github.com/hexdoc-dev/hexdoc"><img src="https://img.shields.io/endpoint?url=https://hexxy.media/api/v0/badge/hexdoc?label=1" alt="powered by hexdoc" style="max-width:100%;"></a>

### Markdown

```md
[![hexdoc](https://img.shields.io/endpoint?url=https://hexxy.media/api/v0/badge/hexdoc)](https://github.com/hexdoc-dev/hexdoc)

[![powered by hexdoc](https://img.shields.io/endpoint?url=https://hexxy.media/api/v0/badge/hexdoc?label=1)](https://github.com/hexdoc-dev/hexdoc)
```

### HTML

```html
<a href="https://github.com/hexdoc-dev/hexdoc"><img src="https://img.shields.io/endpoint?url=https://hexxy.media/api/v0/badge/hexdoc" alt="hexdoc" style="max-width:100%;"></a>

<a href="https://github.com/hexdoc-dev/hexdoc"><img src="https://img.shields.io/endpoint?url=https://hexxy.media/api/v0/badge/hexdoc?label=1" alt="powered by hexdoc" style="max-width:100%;"></a>
```

### reStructuredText

```rst
.. image:: https://img.shields.io/endpoint?url=https://hexxy.media/api/v0/badge/hexdoc
    :target: https://github.com/hexdoc-dev/hexdoc
    :alt: hexdoc

.. image:: https://img.shields.io/endpoint?url=https://hexxy.media/api/v0/badge/hexdoc?label=1
    :target: https://github.com/hexdoc-dev/hexdoc
    :alt: powered by hexdoc
```
