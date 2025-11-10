from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SimulationResult:
    caught: bool
    predator_won: bool | None
    logs: list[str]
