from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from .types import MOVEMENT_STATS, ClawSize, MovementKind


@dataclass
class Creature:
    legs_count: int
    wings_count: int
    claws: ClawSize
    teeth_sharpness: int
    base_power: int
    position: int
    stamina: int
    health: int

    def can_crawl(self) -> bool:
        return True

    def can_hop(self) -> bool:
        return self.legs_count >= 1

    def can_walk(self) -> bool:
        return self.legs_count >= 2

    def can_run(self) -> bool:
        return self.legs_count >= 2

    def can_fly(self) -> bool:
        return self.wings_count >= 2

    def attack_power(self) -> int:
        return int((self.base_power + self.teeth_sharpness) * self.claws.multiplier)


ABILITY_CHECKS: dict[MovementKind, Callable[[Creature], bool]] = {
    MovementKind.CRAWL: lambda c: c.can_crawl(),
    MovementKind.HOP: lambda c: c.can_hop(),
    MovementKind.WALK: lambda c: c.can_walk(),
    MovementKind.RUN: lambda c: c.can_run(),
    MovementKind.FLY: lambda c: c.can_fly(),
}


def can_use_movement(creature: Creature, movement: MovementKind) -> bool:
    stats = MOVEMENT_STATS[movement]
    if creature.stamina < stats.required_stamina:
        return False
    if creature.stamina < stats.stamina_cost:
        return False
    return ABILITY_CHECKS[movement](creature)


def allowed_movements(creature: Creature) -> list[MovementKind]:
    return [m for m in MovementKind if can_use_movement(creature, m)]


def apply_movement(creature: Creature, movement: MovementKind) -> None:
    stats = MOVEMENT_STATS[movement]
    if creature.stamina < stats.stamina_cost:
        return
    creature.position += stats.speed
    creature.stamina -= stats.stamina_cost
