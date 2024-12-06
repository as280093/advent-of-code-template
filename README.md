# 🎅 Advent of Code Template
![Made with Python](https://img.shields.io/badge/Python-v3.13-blue?logo=python&logoColor=white)
[![AoC](https://img.shields.io/badge-⭐%200-gray?logo=adventofcode&labelColor=8a2be2)](https://adventofcode.com/)
[![License: MIT](https://img.shields.io/github/license/as280093/advent-of-code-template)](https://github.com/as280093/advent-of-code-template/blob/main/LICENSE)

This project is a fork of [TeKrop/advent-of-code-template](https://github.com/TeKrop/advent-of-code-template) with many changes, including:
1. Support for multiple years.

Advent of Code Template  in Python. It uses `uv` for dependencies management, `typer` for CLI commands, and `pyinstrument` for profiling. My goal is to write the most readable, understandable and maintainable solutions IMO, which are not necessarily the most performant ones.

The project comes with a dotenv file in which you can specify an `AOC_SESSION_ID` if you wish to automate your input retrieval, and make an answer from CLI directly.

## 💽 Install
The project uses `uv` for dependencies management, install it first : https://docs.astral.sh/uv/getting-started/installation/

Then, install dependencies with `uv sync`

## 🏃 Run

Global usage
```
Usage: aoc.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                         │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.  │
│ --help                        Show this message and exit.                                                       │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ run               Run the solution for a given day.                                                             │
│ create            Create the folder structure and files for a specific day                                      │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Run solution for a given day
```
Usage: aoc.py run [OPTIONS] DAY

Run the solution for a given day.
If --benchmark is used, pyinstrument will profile the process.
If --submit is used, the solution will be submitted on the AoC website using your AOC_SESSION_ID.

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    day      INTEGER RANGE  Day of solution to run (ex: 1 for day01) [default: None] [required]                                       │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --year                        INTEGER  Year of the solution to run (defaults to current year) [default: None]                          │
│ --data-type                  [example|input]  Data type: 'input' for user data, or 'example' for example data [default: input]         │
│ --benchmark    --no-benchmark                     Activate benchmark mode if specified [default: no-benchmark]                         │
│ --submit       --no-submit                        Submit the solution on AoC (AOC_SESSION_ID needed) [default: no-submit]              │
│ --help                                            Show this message and exit.                                                          │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Example Commands
- To run the solution for day 1 of the current year:
```
uv run aoc.py run 1
```

- To run the solution for day 2 of the year 2024:
```
uv run aoc.py run 2 --year 2024
```

- To run the solution for day 3 and benchmark the execution:
```
uv run aoc.py run 3 --benchmark
```

- To run the solution for day 4 and submit the answer:
```
uv run aoc.py run 4 --submit
```

### Create a new day
```
Usage: aoc.py create [OPTIONS]

Create the folder structure and files for a specific day.

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --day          INTEGER  Day to create (1-25) [default: None]. Defaults to the next day if not provided.     │
│ --year         INTEGER  Year to create (defaults to current year) [default: None]                           │
│ --help                  Show this message and exit.                                                         │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Example Command
- To create the folder structure and files for day 1 of the current year:
```
uv run aoc.py create --day 1
```

- To create the folder structure and files for the next day (if today is day 2):
```
uv run aoc.py create
```

- To create the folder structure and files for day 2 of the year 2024:
```
uv run aoc.py create --day 2 --year 2024
```