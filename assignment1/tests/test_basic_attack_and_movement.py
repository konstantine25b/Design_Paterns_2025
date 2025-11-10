from pvspgame.core.creature import (
    Creature,
    allowed_movements,
    apply_movement,
)
from pvspgame.core.types import ClawSize, MovementKind


def test_attack_power_small_claws_and_teeth() -> None:
    c = Creature(
        legs_count=2,
        wings_count=0,
        claws=ClawSize.SMALL,
        teeth_sharpness=3,
        base_power=5,
        position=0,
        stamina=100,
        health=10,
    )
    assert c.attack_power() == 16


def test_allowed_movements_respects_stamina_and_abilities() -> None:
    c = Creature(
        legs_count=2,
        wings_count=0,
        claws=ClawSize.NONE,
        teeth_sharpness=0,
        base_power=1,
        position=0,
        stamina=60,
        health=10,
    )
    moves = set(allowed_movements(c))
    assert MovementKind.RUN in moves
    assert MovementKind.FLY not in moves


def test_apply_movement_updates_position_and_stamina() -> None:
    c = Creature(
        legs_count=2,
        wings_count=0,
        claws=ClawSize.NONE,
        teeth_sharpness=0,
        base_power=1,
        position=0,
        stamina=60,
        health=10,
    )
    apply_movement(c, MovementKind.RUN)
    assert c.position == 6
    assert c.stamina == 56


