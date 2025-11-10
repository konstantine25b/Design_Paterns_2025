from pvspgame.core.creature import Creature
from pvspgame.core.strategies.movement import GreedyMovementStrategy
from pvspgame.core.types import ClawSize, MovementKind


def test_greedy_strategy_prefers_fastest_available() -> None:
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
    strat = GreedyMovementStrategy()
    choice = strat.choose(c)
    assert choice == MovementKind.RUN


def test_greedy_strategy_prefers_fly_when_possible() -> None:
    c = Creature(
        legs_count=0,
        wings_count=2,
        claws=ClawSize.NONE,
        teeth_sharpness=0,
        base_power=1,
        position=0,
        stamina=100,
        health=10,
    )
    strat = GreedyMovementStrategy()
    choice = strat.choose(c)
    assert choice == MovementKind.FLY
