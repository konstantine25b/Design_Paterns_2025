import random

from pvspgame.core.creature import Creature, apply_movement
from pvspgame.core.evolution import evolve_predator_and_prey
from pvspgame.core.types import ClawSize, MovementKind


def test_evolve_predator_and_prey_positions() -> None:
    rng = random.Random(123)
    predator, prey = evolve_predator_and_prey(rng)
    assert predator.position == 0
    assert 0 <= prey.position <= 1000


def test_apply_movement_no_stamina_no_move() -> None:
    c = Creature(
        legs_count=2,
        wings_count=0,
        claws=ClawSize.NONE,
        teeth_sharpness=0,
        base_power=1,
        position=0,
        stamina=1,
        health=10,
    )
    apply_movement(c, MovementKind.WALK)
    assert c.position == 0
    assert c.stamina == 1
