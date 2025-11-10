from pvspgame.core.creature import Creature, allowed_movements
from pvspgame.core.types import ClawSize, MovementKind


def make_creature(legs: int, wings: int, stamina: int) -> Creature:
    return Creature(
        legs_count=legs,
        wings_count=wings,
        claws=ClawSize.NONE,
        teeth_sharpness=0,
        base_power=5,
        position=0,
        stamina=stamina,
        health=10,
    )


def test_crawl_available_with_zero_stamina() -> None:
    c = make_creature(0, 0, stamina=1)
    moves = allowed_movements(c)
    assert MovementKind.CRAWL in moves


def test_hop_requires_one_leg_and_stamina() -> None:
    c = make_creature(1, 0, stamina=20)
    assert MovementKind.HOP in allowed_movements(c)
    c2 = make_creature(0, 0, stamina=100)
    assert MovementKind.HOP not in allowed_movements(c2)


def test_walk_and_run_require_two_legs() -> None:
    c = make_creature(2, 0, stamina=60)
    moves = allowed_movements(c)
    assert MovementKind.WALK in moves
    assert MovementKind.RUN in moves
    c2 = make_creature(1, 0, stamina=100)
    moves2 = allowed_movements(c2)
    assert MovementKind.WALK not in moves2
    assert MovementKind.RUN not in moves2


def test_fly_requires_two_wings_and_stamina() -> None:
    c = make_creature(0, 2, stamina=80)
    assert MovementKind.FLY in allowed_movements(c)
    c2 = make_creature(0, 1, stamina=200)
    assert MovementKind.FLY not in allowed_movements(c2)
