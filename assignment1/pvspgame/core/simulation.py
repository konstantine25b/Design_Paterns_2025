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


def chase(
    predator: Creature,
    prey: Creature,
    movement_strategy: MovementStrategy,
) -> SimulationResult:
    logs: list[str] = []
    while True:
        chosen = movement_strategy.choose(predator)
        if chosen is None:
            logs.append("Pray ran into infinity")
            return SimulationResult(caught=False, predator_won=None, logs=logs)
        apply_movement(predator, chosen)
        if predator.position >= prey.position:
            break
        prey_choice = movement_strategy.choose(prey)
        if prey_choice is None:
            prey_choice = MovementKind.CRAWL
        apply_movement(prey, prey_choice)
        if predator.position >= prey.position:
            break
    return SimulationResult(caught=True, predator_won=None, logs=logs)


def fight(predator: Creature, prey: Creature) -> SimulationResult:
    logs: list[str] = []
    while predator.health > 0 and prey.health > 0:
        prey.health -= predator.attack_power()
        predator.health -= prey.attack_power()
    if predator.health <= 0 and prey.health > 0:
        logs.append("Pray ran into infinity")
        return SimulationResult(caught=True, predator_won=False, logs=logs)
    logs.append("Some R-rated things have happened")
    return SimulationResult(caught=True, predator_won=True, logs=logs)


def run_single_simulation(
    rng: random.Random,
    movement_strategy: MovementStrategy | None = None,
) -> SimulationResult:
    from .evolution import evolve_predator_and_prey

    strategy = movement_strategy or GreedyMovementStrategy()
    predator, prey = evolve_predator_and_prey(rng)
    chase_result = chase(predator, prey, strategy)
    if not chase_result.caught:
        for m in chase_result.logs:
            logger.info(m)
        return chase_result
    fight_result = fight(predator, prey)
    for m in fight_result.logs:
        logger.info(m)
    return fight_result


def run_many_simulations(count: int, seed: int | None = None) -> list[SimulationResult]:
    rng = random.Random(seed)
    results: list[SimulationResult] = []
    for _ in range(count):
        result = run_single_simulation(rng)
        results.append(result)
    return results
