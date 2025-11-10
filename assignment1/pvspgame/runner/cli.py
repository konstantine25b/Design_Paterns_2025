from __future__ import annotations

import typer

from ..core.simulation import run_many_simulations
from ..infra.logging_setup import configure_logging

app = typer.Typer(add_completion=False)


@app.command()
def run(count: int = 100, seed: int | None = None) -> None:
    configure_logging()
    run_many_simulations(count=count, seed=seed)


def main() -> None:
    run()


if __name__ == "__main__":
    app()
