import uuid

import pytest

from habit_tracker.core.habits import Habit, HabitType, Log, Routine
from habit_tracker.infra.in_memory.repository import InMemoryHabitRepository


@pytest.fixture
def repository() -> InMemoryHabitRepository:
    return InMemoryHabitRepository()


@pytest.fixture
def sample_habit() -> Habit:
    return Habit(
        id=uuid.uuid4(),
        name="Drink Water",
        description="8 glasses",
        category="Health",
        type=HabitType.NUMERIC,
        goal=8.0,
    )


@pytest.fixture
def sample_routine() -> Routine:
    return Routine(
        id=uuid.uuid4(),
        name="Morning",
        description="Start day",
        category="Daily",
    )


def test_should_save_and_retrieve_habit(
    repository: InMemoryHabitRepository, sample_habit: Habit
) -> None:
    repository.save(sample_habit)
    retrieved = repository.get(sample_habit.id)
    assert retrieved == sample_habit


def test_should_return_none_for_unknown_habit(
    repository: InMemoryHabitRepository,
) -> None:
    unknown_id = uuid.uuid4()
    assert repository.get(unknown_id) is None


def test_should_list_all_habits(
    repository: InMemoryHabitRepository, sample_habit: Habit, sample_routine: Routine
) -> None:
    repository.save(sample_habit)
    repository.save(sample_routine)
    all_habits = repository.list_all()
    assert len(all_habits) == 2
    assert sample_habit in all_habits
    assert sample_routine in all_habits


def test_should_list_empty_when_no_habits(
    repository: InMemoryHabitRepository,
) -> None:
    assert repository.list_all() == []


def test_should_delete_habit(
    repository: InMemoryHabitRepository, sample_habit: Habit
) -> None:
    repository.save(sample_habit)
    repository.delete(sample_habit.id)
    assert repository.get(sample_habit.id) is None


def test_should_delete_unknown_habit_silently(
    repository: InMemoryHabitRepository,
) -> None:
    unknown_id = uuid.uuid4()
    repository.delete(unknown_id)
    assert repository.get(unknown_id) is None


def test_should_update_habit(
    repository: InMemoryHabitRepository, sample_habit: Habit
) -> None:
    repository.save(sample_habit)
    sample_habit.name = "Updated Name"
    repository.save(sample_habit)
    retrieved = repository.get(sample_habit.id)
    assert retrieved is not None
    assert retrieved.name == "Updated Name"


def test_should_save_log(repository: InMemoryHabitRepository) -> None:
    from datetime import date

    habit_id = uuid.uuid4()
    log = Log(habit_id=habit_id, date=date.today(), value=5.0)
    repository.save_log(log)
    logs = repository.get_logs(habit_id)
    assert len(logs) == 1
    assert logs[0] == log


def test_should_return_empty_logs_for_unknown_habit(
    repository: InMemoryHabitRepository,
) -> None:
    unknown_id = uuid.uuid4()
    assert repository.get_logs(unknown_id) == []


