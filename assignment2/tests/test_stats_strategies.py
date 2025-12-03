import uuid
from datetime import date, timedelta

from habit_tracker.core.habits import Log
from habit_tracker.core.stats import (
    CompletionRateStrategy,
    CurrentStreakStrategy,
    StatContext,
    TotalProgressStrategy,
)


def test_should_calculate_zero_total_for_empty_logs() -> None:
    strategy = TotalProgressStrategy()
    assert strategy.calculate([], 10.0) == 0.0


def test_should_sum_all_log_values() -> None:
    logs = [
        Log(uuid.uuid4(), date.today(), 5.0),
        Log(uuid.uuid4(), date.today(), 7.0),
        Log(uuid.uuid4(), date.today(), 3.0),
    ]
    strategy = TotalProgressStrategy()
    assert strategy.calculate(logs, 10.0) == 15.0


def test_should_ignore_goal_for_total() -> None:
    logs = [Log(uuid.uuid4(), date.today(), 5.0)]
    strategy = TotalProgressStrategy()
    assert strategy.calculate(logs, 100.0) == 5.0


def test_should_calculate_zero_streak_for_empty_logs() -> None:
    strategy = CurrentStreakStrategy()
    assert strategy.calculate([], 5.0) == 0


def test_should_calculate_single_day_streak() -> None:
    logs = [Log(uuid.uuid4(), date.today(), 6.0)]
    strategy = CurrentStreakStrategy()
    assert strategy.calculate(logs, 5.0) == 1


def test_should_calculate_multi_day_streak() -> None:
    today = date.today()
    logs = [
        Log(uuid.uuid4(), today, 6.0),
        Log(uuid.uuid4(), today - timedelta(days=1), 7.0),
        Log(uuid.uuid4(), today - timedelta(days=2), 8.0),
    ]
    strategy = CurrentStreakStrategy()
    assert strategy.calculate(logs, 5.0) == 3


def test_should_break_streak_on_failure() -> None:
    today = date.today()
    logs = [
        Log(uuid.uuid4(), today, 6.0),
        Log(uuid.uuid4(), today - timedelta(days=1), 7.0),
        Log(uuid.uuid4(), today - timedelta(days=2), 3.0),
        Log(uuid.uuid4(), today - timedelta(days=3), 8.0),
    ]
    strategy = CurrentStreakStrategy()
    assert strategy.calculate(logs, 5.0) == 2


def test_should_count_streak_from_most_recent() -> None:
    today = date.today()
    logs = [
        Log(uuid.uuid4(), today - timedelta(days=3), 8.0),
        Log(uuid.uuid4(), today - timedelta(days=2), 3.0),
        Log(uuid.uuid4(), today - timedelta(days=1), 7.0),
        Log(uuid.uuid4(), today, 6.0),
    ]
    strategy = CurrentStreakStrategy()
    assert strategy.calculate(logs, 5.0) == 2


def test_should_calculate_zero_completion_for_empty_logs() -> None:
    strategy = CompletionRateStrategy()
    assert strategy.calculate([], 5.0) == 0.0


def test_should_calculate_full_completion() -> None:
    logs = [
        Log(uuid.uuid4(), date.today(), 6.0),
        Log(uuid.uuid4(), date.today(), 7.0),
        Log(uuid.uuid4(), date.today(), 8.0),
    ]
    strategy = CompletionRateStrategy()
    assert strategy.calculate(logs, 5.0) == 100.0


def test_should_calculate_partial_completion() -> None:
    logs = [
        Log(uuid.uuid4(), date.today(), 6.0),
        Log(uuid.uuid4(), date.today(), 3.0),
    ]
    strategy = CompletionRateStrategy()
    assert strategy.calculate(logs, 5.0) == 50.0


def test_should_calculate_zero_completion() -> None:
    logs = [
        Log(uuid.uuid4(), date.today(), 2.0),
        Log(uuid.uuid4(), date.today(), 3.0),
    ]
    strategy = CompletionRateStrategy()
    assert strategy.calculate(logs, 5.0) == 0.0


def test_should_use_strategy_with_context() -> None:
    logs = [Log(uuid.uuid4(), date.today(), 5.0)]
    strategy = TotalProgressStrategy()
    context = StatContext(strategy)
    assert context.analyze(logs, 10.0) == 5.0


def test_should_switch_strategies_in_context() -> None:
    logs = [
        Log(uuid.uuid4(), date.today(), 6.0),
        Log(uuid.uuid4(), date.today(), 3.0),
    ]
    context = StatContext(TotalProgressStrategy())
    assert context.analyze(logs, 5.0) == 9.0
    context = StatContext(CompletionRateStrategy())
    assert context.analyze(logs, 5.0) == 50.0


def test_should_handle_exact_goal_match() -> None:
    logs = [Log(uuid.uuid4(), date.today(), 5.0)]
    strategy = CurrentStreakStrategy()
    assert strategy.calculate(logs, 5.0) == 1


def test_should_handle_above_goal() -> None:
    logs = [Log(uuid.uuid4(), date.today(), 10.0)]
    strategy = CurrentStreakStrategy()
    assert strategy.calculate(logs, 5.0) == 1


def test_should_handle_below_goal() -> None:
    logs = [Log(uuid.uuid4(), date.today(), 4.99)]
    strategy = CurrentStreakStrategy()
    assert strategy.calculate(logs, 5.0) == 0


def test_should_round_completion_rate_correctly() -> None:
    logs = [
        Log(uuid.uuid4(), date.today(), 6.0),
        Log(uuid.uuid4(), date.today(), 3.0),
        Log(uuid.uuid4(), date.today(), 7.0),
    ]
    strategy = CompletionRateStrategy()
    result = strategy.calculate(logs, 5.0)
    assert 66.0 < result < 67.0

