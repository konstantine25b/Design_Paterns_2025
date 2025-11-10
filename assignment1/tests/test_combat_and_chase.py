from pvspgame.core.creature import Creature, GreedyMovementStrategy
from pvspgame.core.simulation import chase, fight
from pvspgame.core.types import ClawSize


def test_chase_stops_when_predator_cannot_move() -> None:
    predator = Creature(
        legs_count=0,
        wings_count=0,
        claws=ClawSize.NONE,
        teeth_sharpness=0,
        base_power=1,
        position=0,
        stamina=0,
        health=10,
    )
    prey = Creature(
        legs_count=2,
        wings_count=0,
        claws=ClawSize.NONE,
        teeth_sharpness=0,
        base_power=1,
        position=10,
        stamina=100,
        health=10,
    )
    result = chase(predator, prey, GreedyMovementStrategy())
    assert result.caught is False
    assert any(m == "Pray ran into infinity" for m in result.logs)


def test_fight_stops_when_one_health_zero_or_below() -> None:
    predator = Creature(
        legs_count=2,
        wings_count=0,
        claws=ClawSize.BIG,
        teeth_sharpness=9,
        base_power=10,
        position=0,
        stamina=100,
        health=30,
    )
    prey = Creature(
        legs_count=2,
        wings_count=0,
        claws=ClawSize.NONE,
        teeth_sharpness=0,
        base_power=1,
        position=0,
        stamina=100,
        health=10,
    )
    result = fight(predator, prey)
    assert result.caught is True
    assert result.predator_won is True
    assert any(m == "Some R-rated things have happened" for m in result.logs)
