import uuid
from datetime import date, timedelta

import pytest

from habit_tracker.core.habits import Habit, HabitType, Routine
from habit_tracker.core.services import HabitService
from habit_tracker.infra.in_memory.repository import InMemoryHabitRepository


@pytest.fixture
def service() -> HabitService:
    return HabitService(InMemoryHabitRepository())


def test_should_create_habit(service: HabitService) -> None:
    habit = service.create_habit(
        name="Exercise",
        description="Daily workout",
        category="Health",
        habit_type=HabitType.BOOLEAN,
        goal=1.0,
    )
    assert habit.name == "Exercise"
    assert habit.type == HabitType.BOOLEAN
    assert habit.goal == 1.0


def test_should_create_routine(service: HabitService) -> None:
    routine = service.create_routine(
        name="Morning", description="Start day", category="Daily"
    )
    assert routine.name == "Morning"
    assert routine.is_composite()


def test_should_retrieve_created_habit(service: HabitService) -> None:
    habit = service.create_habit(
        "Read", "Books", "Learning", HabitType.NUMERIC, 30.0
    )
    retrieved = service.get_habit(habit.id)
    assert retrieved is not None
    assert retrieved.id == habit.id


def test_should_return_none_for_unknown_habit(service: HabitService) -> None:
    unknown_id = uuid.uuid4()
    assert service.get_habit(unknown_id) is None


def test_should_list_all_habits(service: HabitService) -> None:
    service.create_habit("Habit1", "D1", "C1", HabitType.BOOLEAN, 1.0)
    service.create_habit("Habit2", "D2", "C2", HabitType.NUMERIC, 5.0)
    habits = service.list_habits()
    assert len(habits) == 2


def test_should_list_empty_initially(service: HabitService) -> None:
    assert service.list_habits() == []


def test_should_delete_habit(service: HabitService) -> None:
    habit = service.create_habit("Delete Me", "Temp", "Test", HabitType.BOOLEAN, 1.0)
    service.delete_habit(habit.id)
    assert service.get_habit(habit.id) is None


def test_should_update_habit_name(service: HabitService) -> None:
    habit = service.create_habit("Old", "Desc", "Cat", HabitType.BOOLEAN, 1.0)
    updated = service.update_habit(habit.id, name="New")
    assert updated is not None
    assert updated.name == "New"


def test_should_update_habit_description(service: HabitService) -> None:
    habit = service.create_habit("Name", "Old", "Cat", HabitType.BOOLEAN, 1.0)
    updated = service.update_habit(habit.id, description="New Description")
    assert updated is not None
    assert updated.description == "New Description"


def test_should_update_habit_goal(service: HabitService) -> None:
    habit = service.create_habit("Name", "Desc", "Cat", HabitType.NUMERIC, 5.0)
    updated = service.update_habit(habit.id, goal=10.0)
    assert updated is not None
    assert isinstance(updated, Habit)
    assert updated.goal == 10.0


def test_should_return_none_when_updating_unknown_habit(
    service: HabitService,
) -> None:
    unknown_id = uuid.uuid4()
    result = service.update_habit(unknown_id, name="New")
    assert result is None


def test_should_add_habit_to_routine(service: HabitService) -> None:
    routine = service.create_routine("Routine", "Desc", "Cat")
    habit = service.create_habit("Habit", "Desc", "Cat", HabitType.BOOLEAN, 1.0)
    service.add_subhabit(routine.id, habit.id)
    retrieved = service.get_habit(routine.id)
    assert retrieved is not None
    assert isinstance(retrieved, Routine)
    assert len(retrieved.get_children()) == 1


def test_should_raise_error_when_adding_to_leaf_habit(service: HabitService) -> None:
    habit = service.create_habit("Habit", "Desc", "Cat", HabitType.BOOLEAN, 1.0)
    child = service.create_habit("Child", "Desc", "Cat", HabitType.BOOLEAN, 1.0)
    with pytest.raises(ValueError):
        service.add_subhabit(habit.id, child.id)


def test_should_raise_error_when_parent_not_found(service: HabitService) -> None:
    habit = service.create_habit("Habit", "Desc", "Cat", HabitType.BOOLEAN, 1.0)
    with pytest.raises(ValueError):
        service.add_subhabit(uuid.uuid4(), habit.id)


def test_should_raise_error_when_child_not_found(service: HabitService) -> None:
    routine = service.create_routine("Routine", "Desc", "Cat")
    with pytest.raises(ValueError):
        service.add_subhabit(routine.id, uuid.uuid4())


def test_should_log_progress(service: HabitService) -> None:
    habit = service.create_habit("Habit", "Desc", "Cat", HabitType.NUMERIC, 8.0)
    log = service.log_progress(habit.id, 5.0)
    assert log.habit_id == habit.id
    assert log.value == 5.0


def test_should_log_progress_with_date(service: HabitService) -> None:
    habit = service.create_habit("Habit", "Desc", "Cat", HabitType.NUMERIC, 8.0)
    custom_date = date(2025, 1, 1)
    log = service.log_progress(habit.id, 5.0, custom_date)
    assert log.date == custom_date


def test_should_default_log_date_to_today(service: HabitService) -> None:
    habit = service.create_habit("Habit", "Desc", "Cat", HabitType.NUMERIC, 8.0)
    log = service.log_progress(habit.id, 5.0)
    assert log.date == date.today()


def test_should_retrieve_logs(service: HabitService) -> None:
    habit = service.create_habit("Habit", "Desc", "Cat", HabitType.NUMERIC, 8.0)
    service.log_progress(habit.id, 5.0)
    service.log_progress(habit.id, 7.0)
    logs = service.get_logs(habit.id)
    assert len(logs) == 2


def test_should_return_empty_logs_for_habit_without_logs(
    service: HabitService,
) -> None:
    habit = service.create_habit("Habit", "Desc", "Cat", HabitType.NUMERIC, 8.0)
    assert service.get_logs(habit.id) == []


def test_should_calculate_total_progress(service: HabitService) -> None:
    habit = service.create_habit("Habit", "Desc", "Cat", HabitType.NUMERIC, 10.0)
    service.log_progress(habit.id, 5.0)
    service.log_progress(habit.id, 7.0)
    total = service.get_stats(habit.id, "total")
    assert total == 12.0


def test_should_calculate_streak(service: HabitService) -> None:
    habit = service.create_habit("Habit", "Desc", "Cat", HabitType.NUMERIC, 5.0)
    today = date.today()
    service.log_progress(habit.id, 6.0, today)
    service.log_progress(habit.id, 7.0, today - timedelta(days=1))
    service.log_progress(habit.id, 5.0, today - timedelta(days=2))
    streak = service.get_stats(habit.id, "streak")
    assert streak == 3


def test_should_calculate_completion_rate(service: HabitService) -> None:
    habit = service.create_habit("Habit", "Desc", "Cat", HabitType.NUMERIC, 5.0)
    service.log_progress(habit.id, 6.0)
    service.log_progress(habit.id, 7.0)
    service.log_progress(habit.id, 3.0)
    rate = service.get_stats(habit.id, "completion_rate")
    assert rate == pytest.approx(66.666, rel=0.01)


def test_should_return_zero_stats_for_routine(service: HabitService) -> None:
    routine = service.create_routine("Routine", "Desc", "Cat")
    assert service.get_stats(routine.id, "total") == 0


def test_should_raise_error_for_unknown_habit_stats(service: HabitService) -> None:
    unknown_id = uuid.uuid4()
    with pytest.raises(ValueError):
        service.get_stats(unknown_id, "total")

