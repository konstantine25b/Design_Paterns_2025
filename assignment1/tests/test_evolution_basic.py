import random

from pvspgame.core.evolution import evolve_random_creature
from pvspgame.core.types import ClawSize


def test_evolution_creature_fields_are_in_expected_ranges() -> None:
    rng = random.Random(0)
    c = evolve_random_creature(rng, position=5)
    assert 0 <= c.legs_count <= 4
    assert 0 <= c.wings_count <= 4
    assert c.claws in {ClawSize.NONE, ClawSize.SMALL, ClawSize.MEDIUM, ClawSize.BIG}
    assert c.teeth_sharpness in {0, 3, 6, 9}
    assert 3 <= c.base_power <= 10
    assert c.position == 5
    assert 40 <= c.stamina <= 160
    assert 30 <= c.health <= 120


