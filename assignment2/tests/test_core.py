import uuid
from datetime import date, timedelta

from habit_tracker.core.habits import Habit, HabitType, Log, Routine
from habit_tracker.core.stats import CurrentStreakStrategy, TotalProgressStrategy


def test_streak_strategy() -> None:
    strategy = CurrentStreakStrategy()
    goal = 5.0
    today = date.today()

    logs = [
        Log(uuid.uuid4(), today, 5.0),
        Log(uuid.uuid4(), today - timedelta(days=1), 6.0),
        Log(uuid.uuid4(), today - timedelta(days=2), 5.0),
        Log(uuid.uuid4(), today - timedelta(days=3), 2.0),
    ]

    streak = strategy.calculate(logs, goal)
    assert streak == 3


def test_total_progress_strategy() -> None:
    strategy = TotalProgressStrategy()
    logs = [
        Log(uuid.uuid4(), date.today(), 10.0),
        Log(uuid.uuid4(), date.today(), 5.0),
    ]
    total = strategy.calculate(logs, 0.0)
    assert total == 15.0


def test_routine_composite() -> None:
    routine = Routine(
        id=uuid.uuid4(), name="Routine", description="Desc", category="Cat"
    )
    habit = Habit(
        id=uuid.uuid4(),
        name="Habit",
        description="Desc",
        category="Cat",
        type=HabitType.BOOLEAN,
        goal=1.0,
    )

    routine.add(habit)
    assert len(routine.get_children()) == 1

    routine.remove(habit)
    assert len(routine.get_children()) == 0
