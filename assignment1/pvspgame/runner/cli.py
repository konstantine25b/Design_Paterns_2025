from __future__ import annotations

import typer

from ..core.simulation import run_many_simulations
from ..infra.logging_setup import configure_logging

app = typer.Typer(add_completion=False)


@app.command()
def run(
    count: int = typer.Option(100, help="Number of simulations to run."),
    seed: int | None = typer.Option(None, help="Random seed for reproducibility."),
    visualize: bool = typer.Option(
        False,
        help="Render a simple ASCII visualization of positions.",
    ),
    verbose: bool = typer.Option(False, help="Print detailed per-step logs."),
) -> None:
    configure_logging()
    run_many_simulations(count=count, seed=seed, visualize=visualize, verbose=verbose)


def main() -> None:
    run()


if __name__ == "__main__":
    app()
