from __future__ import annotations

import logging
import random
from dataclasses import dataclass

from .creature import Creature, GreedyMovementStrategy, MovementStrategy, apply_movement
from .types import MovementKind

logger = logging.getLogger(__name__)


@dataclass
class SimulationResult:
    caught: bool
    predator_won: bool | None
    logs: list[str]


def _render_world(predator: Creature, prey: Creature, width: int = 50) -> str:
    a = predator.position
    b = prey.position
    left = min(a, b)
    right = max(a, b)
    span = right - left
    if span <= 0:
        return "X"
    if span >= width:
        pa = 0 if a == left else width - 1
        pb = 0 if b == left else width - 1
    else:
        pa = a - left
        pb = b - left
    line = ["." for _ in range(width if span >= width else span + 1)]
    line[pa] = "A"
    line[pb] = "B"
    return "".join(line)


def chase(
    predator: Creature,
    prey: Creature,
    movement_strategy: MovementStrategy,
    *,
    verbose: bool = False,
    visualize: bool = False,
) -> SimulationResult:
    logs: list[str] = []
    while True:
        chosen = movement_strategy.choose(predator)
        if chosen is None:
            logs.append("Pray ran into infinity")
            return SimulationResult(caught=False, predator_won=None, logs=logs)
        apply_movement(predator, chosen)
        if visualize:
            logs.append(_render_world(predator, prey))
        if predator.position >= prey.position:
            break
        prey_choice = movement_strategy.choose(prey)
        if prey_choice is None:
            prey_choice = MovementKind.CRAWL
        apply_movement(prey, prey_choice)
        if visualize:
            logs.append(_render_world(predator, prey))
        if verbose:
            pred_msg = (
                f"pred pos={predator.position} "
                f"stam={predator.stamina} move={chosen.name}"
            )
            prey_msg = (
                f"prey pos={prey.position} "
                f"stam={prey.stamina} move={prey_choice.name}"
            )
            logs.append(f"{pred_msg}; {prey_msg}")
        if predator.position >= prey.position:
            break
    return SimulationResult(caught=True, predator_won=None, logs=logs)


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


def run_single_simulation(
    rng: random.Random,
    movement_strategy: MovementStrategy | None = None,
    *,
    verbose: bool = False,
    visualize: bool = False,
) -> SimulationResult:
    from .evolution import evolve_predator_and_prey

    strategy = movement_strategy or GreedyMovementStrategy()
    predator, prey = evolve_predator_and_prey(rng)
    chase_result = chase(predator, prey, strategy, verbose=verbose, visualize=visualize)
    if not chase_result.caught:
        for m in chase_result.logs:
            logger.info(m)
        return chase_result
    fight_result = fight(predator, prey, verbose=verbose)
    for m in [*chase_result.logs, *fight_result.logs]:
        logger.info(m)
    return fight_result


def run_many_simulations(
    count: int,
    seed: int | None = None,
    *,
    verbose: bool = False,
    visualize: bool = False,
) -> list[SimulationResult]:
    rng = random.Random(seed)
    results: list[SimulationResult] = []
    for _ in range(count):
        result = run_single_simulation(rng, verbose=verbose, visualize=visualize)
        results.append(result)
    return results
