from __future__ import annotations

import logging
import random

from .sim_types import SimulationResult
from .strategies.chase import chase
from .strategies.fight import fight
from .strategies.movement import GreedyMovementStrategy, MovementStrategy

logger = logging.getLogger(__name__)
__all__ = ["run_single_simulation", "run_many_simulations", "chase", "fight"]


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
