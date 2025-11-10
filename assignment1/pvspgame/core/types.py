from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum


class ClawSize(Enum):
    NONE = 0
    SMALL = 2
    MEDIUM = 3
    BIG = 4

    @property
    def multiplier(self) -> int:
        if self is ClawSize.SMALL:
            return 2
        if self is ClawSize.MEDIUM:
            return 3
        if self is ClawSize.BIG:
            return 4
        return 1


class MovementKind(Enum):
    CRAWL = "crawl"
    HOP = "hop"
    WALK = "walk"
    RUN = "run"
    FLY = "fly"


@dataclass(frozen=True)
class MovementStats:
    required_stamina: int
    stamina_cost: int
    speed: int


MOVEMENT_STATS = {
    MovementKind.CRAWL: MovementStats(required_stamina=0, stamina_cost=1, speed=1),
    MovementKind.HOP: MovementStats(required_stamina=20, stamina_cost=2, speed=3),
    MovementKind.WALK: MovementStats(required_stamina=40, stamina_cost=2, speed=4),
    MovementKind.RUN: MovementStats(required_stamina=60, stamina_cost=4, speed=6),
    MovementKind.FLY: MovementStats(required_stamina=80, stamina_cost=4, speed=8),
}


def ordered_by_speed_desc(movements: Iterable[MovementKind]) -> list[MovementKind]:
    return sorted(movements, key=lambda m: MOVEMENT_STATS[m].speed, reverse=True)
