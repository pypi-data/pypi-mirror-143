# Mite CLI

A command line tool to create a new [mite](https://github.com/sky-uk/mite/) project. 

## Installation

```bash
pip install mite-cli
```

## Usage

```
Usage:
    mite-cli new <project_dir> [options]

Options:
    --log-level=LEVEL       Set logger level: DEBUG, INFO, WARNING, ERROR, CRITICAL [default: INFO]
    -e --createvenv         Create a python virtual environment
```

### Create new mite project

```bash
mite-cli new my_project_dir
```