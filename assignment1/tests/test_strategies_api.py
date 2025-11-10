from pvspgame.core.creature import Creature
from pvspgame.core.strategies.chase import chase as chase_strategy
from pvspgame.core.strategies.fight import fight as fight_strategy
from pvspgame.core.strategies.movement import GreedyMovementStrategy
from pvspgame.core.types import ClawSize


def test_chase_strategy_returns_uncaught_when_no_move() -> None:
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
        position=5,
        stamina=100,
        health=10,
    )
    res = chase_strategy(predator, prey, GreedyMovementStrategy())
    assert res.caught is False


def test_fight_strategy_predator_wins_with_stronger_stats() -> None:
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
    res = fight_strategy(predator, prey)
    assert res.predator_won is True
