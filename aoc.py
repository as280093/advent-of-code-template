import importlib
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from pyinstrument import Profiler
from rich import print
from typing_extensions import Annotated

from scripts.utils import (
    AnswerResult,
    DataType,
    create_empty_file,
    get_input,
    submit_answer,
)

app = typer.Typer()


@app.command()
def run(
    year: Optional[int] = typer.Option(
        None, help="Year of the solution to run (defaults to current year)."
    ),
    day: Optional[int] = typer.Option(None, help="Day of the solution to run (1-25)."),
    data_type: str = typer.Option(
        "input", help="Data type: 'input' for user data, or 'example' for example data."
    ),
    benchmark: bool = typer.Option(False, help="Activate benchmark mode if specified."),
    submit: bool = typer.Option(
        False, help="Submit the solution on AoC (AOC_SESSION_ID needed)."
    ),
):
    """
    Run the solution for a given day.
    """
    if year is None:
        year = datetime.now().year

    if day is None:
        day = datetime.now().day + 1

    if day < 1 or day > 25:
        print("[red]Day must be between 1 and 25.[/red]")
        raise typer.Exit(1)

    try:
        day_module = importlib.import_module(f"solutions.{year}.day{day:02d}.main")
    except ModuleNotFoundError:
        print(
            f"[red]No puzzle solver for [bold]day {day} of year {year}[/bold] yet.[/red]"
        )
        raise typer.Exit(1)

    try:
        puzzle_solver = day_module.PuzzleSolver(year=year, day=day, data_type=data_type)
    except FileNotFoundError:
        print(
            f"[red]File [bold]{data_type.value}.txt[/bold] not found for day {day} of year {year}.[/red]"
        )
        raise typer.Exit(1)

    print(f"Running puzzle solver for day {day}...")
    if data_type == DataType.EXAMPLE:
        print("Computing example data...")

    if benchmark:
        print("Benchmark mode activated!")
        profiler = Profiler()
        profiler.start()
        results = puzzle_solver.solve()
        profiler.stop()
        print(f"[green]Results : [bold]{results}[/bold][/green]")
        profiler.print()
    else:
        results = puzzle_solver.solve()
        print(f"[green]Results : [bold]{results}[/bold][/green]")

    if not submit:
        return

    if data_type == DataType.EXAMPLE:
        print(f"[red]You can't send an answer for example data[/red]")
        raise typer.Exit(1)

    for task, result in enumerate(results, 1):
        if result is None:
            continue

        match submit_answer(day=day, year=year, task=task, answer=result):
            case AnswerResult.ALREADY_SOLVED:
                print(f"[red]Task {task} has already been solved![/red]")
            case AnswerResult.RIGHT_ANSWER:
                print(f"[green]Your answer for task {task} is right![/green]")
            case AnswerResult.WRONG_ANSWER:
                print(f"[red]Your answer for task {task} is wrong![/red]")
            case _:
                continue


@app.command()
def create(
    day: Optional[int] = typer.Option(
        None, help="Day of the solution to create (1-25)."
    ),
    year: Optional[int] = typer.Option(
        None, help="Year of the solution to create (defaults to current year)."
    ),
):
    """
    Scaffold files to start a new Advent of Code solution.
    """
    if year is None:
        year = datetime.now().year

    if day is None:
        day = datetime.now().day + 1
        
    if day < 1 or day > 25:
        print("[red]Day must be between 1 and 25.[/red]")
        raise typer.Exit(1)

    days_path = Path(__file__).parent / "solutions" / str(year)
    days_path.mkdir(parents=True, exist_ok=True)

    template_path = Path(__file__).parent / "scripts" / "day_template.py"
    if not template_path.exists():
        print(
            "[red]Model [bold]day_template.py[/bold] not found in [bold]scripts[/bold] folder.[/red]"
        )
        raise typer.Exit(1)

    template_content = template_path.read_text()

    day_str = f"day{day:02d}"
    day_path = days_path / day_str

    if day_path.exists():
        if not typer.confirm(
            f"The folder for [bold]{day_str}[/bold] already exists in year [bold]{year}[/bold]. Do you want to overwrite it?",
            default=False,
        ):
            print("[red]Operation cancelled. No changes made.[/red]")
            raise typer.Exit(1)
        else:
            import shutil

            shutil.rmtree(day_path)

    day_path.mkdir(parents=True)
    print(
        f"[green]Folder [bold]{day_str}[/bold] created in year [bold]{year}[/bold].[/green]"
    )

    main_file = day_path / "main.py"
    main_content = template_content.replace("X", f"{day:02d}")
    main_file.write_text(main_content)
    print(
        f"[green]File [bold]{main_file.name}[/bold] created successfully from model.[/green]"
    )

    create_empty_file(file_path=day_path / "example.txt")
    input_file_path = day_path / "input.txt"
    if input_content := get_input(day=day, year=year):
        input_file_path.write_text(input_content, encoding="utf-8")
    else:
        create_empty_file(file_path=input_file_path)


if __name__ == "__main__":
    app()
