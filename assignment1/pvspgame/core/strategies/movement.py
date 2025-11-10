from __future__ import annotations

from typing import Protocol

from ..creature import Creature, allowed_movements
from ..types import MOVEMENT_STATS, MovementKind


class MovementStrategy(Protocol):
    def choose(self, creature: Creature) -> MovementKind | None: ...


class GreedyMovementStrategy:
    def choose(self, creature: Creature) -> MovementKind | None:
        movements = allowed_movements(creature)
        if not movements:
            return None
        return max(movements, key=lambda m: MOVEMENT_STATS[m].speed)
