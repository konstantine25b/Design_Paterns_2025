from __future__ import annotations

import random

from .creature import Creature
from .types import ClawSize


def evolve_random_creature(rng: random.Random, position: int) -> Creature:
    legs = rng.choice([0, 1, 2, 3, 4])
    wings = rng.choice([0, 1, 2, 3, 4])
    claws = rng.choice([ClawSize.NONE, ClawSize.SMALL, ClawSize.MEDIUM, ClawSize.BIG])
    teeth = rng.choice([0, 3, 6, 9])
    base_power = rng.randint(3, 10)
    stamina = rng.randint(40, 160)
    health = rng.randint(30, 120)
    return Creature(
        legs_count=legs,
        wings_count=wings,
        claws=claws,
        teeth_sharpness=teeth,
        base_power=base_power,
        position=position,
        stamina=stamina,
        health=health,
    )


def evolve_predator_and_prey(rng: random.Random) -> tuple[Creature, Creature]:
    predator = evolve_random_creature(rng, 0)
    prey_position = rng.randint(0, 1000)
    prey = evolve_random_creature(rng, prey_position)
    return predator, prey
