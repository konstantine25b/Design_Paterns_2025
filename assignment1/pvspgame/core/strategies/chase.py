from __future__ import annotations

from ..creature import Creature, apply_movement
from ..sim_types import SimulationResult
from ..types import MovementKind
from ..visualization import describe_creature, render_world
from .movement import MovementStrategy


def chase(
    predator: Creature,
    prey: Creature,
    movement_strategy: MovementStrategy,
    *,
    verbose: bool = False,
    visualize: bool = False,
) -> SimulationResult:
    logs: list[str] = []
    if visualize:
        pred_desc = describe_creature(predator)
        prey_desc = describe_creature(prey)
        logs.append(f"Predator: {pred_desc}")
        logs.append(f"Prey: {prey_desc}")
    while True:
        chosen = movement_strategy.choose(predator)
        if chosen is None:
            logs.append("Pray ran into infinity")
            return SimulationResult(caught=False, predator_won=None, logs=logs)
        apply_movement(predator, chosen)
        if visualize:
            logs.append(render_world(predator, prey))
        if predator.position >= prey.position:
            break
        prey_choice = movement_strategy.choose(prey)
        if prey_choice is None:
            prey_choice = MovementKind.CRAWL
        apply_movement(prey, prey_choice)
        if visualize:
            logs.append(render_world(predator, prey))
        if verbose:
            pred_msg = (
                f"pred pos={predator.position} "
                f"stam={predator.stamina} move={chosen.name}"
            )
            prey_msg = (
                f"prey pos={prey.position} stam={prey.stamina} move={prey_choice.name}"
            )
            logs.append(f"{pred_msg}; {prey_msg}")
        if predator.position >= prey.position:
            break
    return SimulationResult(caught=True, predator_won=None, logs=logs)
