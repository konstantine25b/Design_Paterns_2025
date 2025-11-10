from __future__ import annotations

from ..creature import Creature
from ..simulation import SimulationResult  # type: ignore


def fight(
    predator: Creature,
    prey: Creature,
    *,
    verbose: bool = False,
) -> SimulationResult:
    logs: list[str] = []
    while predator.health > 0 and prey.health > 0:
        prey.health -= predator.attack_power()
        predator.health -= prey.attack_power()
        if verbose:
            logs.append(
                f"pred hp={predator.health} atk={predator.attack_power()}; "
                f"prey hp={prey.health} atk={prey.attack_power()}"
            )
    if predator.health <= 0 and prey.health > 0:
        logs.append("Pray ran into infinity")
        return SimulationResult(caught=True, predator_won=False, logs=logs)
    logs.append("Some R-rated things have happened")
    return SimulationResult(caught=True, predator_won=True, logs=logs)
