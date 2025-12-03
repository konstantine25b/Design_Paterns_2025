from __future__ import annotations

import uuid
from datetime import date
from typing import Any

from .habits import Habit, HabitComponent, HabitType, Log, Routine
from .repository import HabitRepository
from .stats import (
    CompletionRateStrategy,
    CurrentStreakStrategy,
    StatContext,
    StatStrategy,
    TotalProgressStrategy,
)


class HabitService:
    def __init__(self, repository: HabitRepository):
        self.repo = repository

    def create_habit(
        self,
        name: str,
        description: str,
        category: str,
        habit_type: HabitType,
        goal: float,
    ) -> Habit:
        habit = Habit(
            id=uuid.uuid4(),
            name=name,
            description=description,
            created_at=date.today(),
            category=category,
            type=habit_type,
            goal=goal,
        )
        self.repo.save(habit)
        return habit

    def create_routine(self, name: str, description: str, category: str) -> Routine:
        routine = Routine(
            id=uuid.uuid4(),
            name=name,
            description=description,
            created_at=date.today(),
            category=category,
        )
        self.repo.save(routine)
        return routine

    def get_habit(self, habit_id: uuid.UUID) -> HabitComponent | None:
        return self.repo.get(habit_id)

    def list_habits(self) -> list[HabitComponent]:
        return self.repo.list_all()

    def delete_habit(self, habit_id: uuid.UUID) -> None:
        self.repo.delete(habit_id)

    def update_habit(
        self,
        habit_id: uuid.UUID,
        name: str | None = None,
        description: str | None = None,
        category: str | None = None,
        goal: float | None = None,
    ) -> HabitComponent | None:
        habit = self.repo.get(habit_id)
        if not habit:
            return None

        if name is not None:
            habit.name = name
        if description is not None:
            habit.description = description
        if category is not None and hasattr(habit, "category"):
            habit.category = category

        if goal is not None and isinstance(habit, Habit):
            habit.goal = goal

        self.repo.save(habit)
        return habit

    def add_subhabit(self, parent_id: uuid.UUID, child_id: uuid.UUID) -> None:
        parent = self.repo.get(parent_id)
        child = self.repo.get(child_id)
        if not parent or not child:
            raise ValueError("Parent or child not found")

        try:
            parent.add(child)
            self.repo.save(parent)
        except NotImplementedError as e:
            raise ValueError("Cannot add sub-habit to this habit type") from e

    def log_progress(
        self, habit_id: uuid.UUID, value: float, log_date: date | None = None
    ) -> Log:
        if log_date is None:
            log_date = date.today()

        log = Log(habit_id=habit_id, date=log_date, value=value)
        self.repo.save_log(log)
        return log

    def get_logs(self, habit_id: uuid.UUID) -> list[Log]:
        return self.repo.get_logs(habit_id)

    def get_stats(self, habit_id: uuid.UUID, strategy_type: str) -> Any:
        habit = self.repo.get(habit_id)
        if not habit:
            raise ValueError("Habit not found")

        if isinstance(habit, Routine):
            return 0

        logs = self.repo.get_logs(habit_id)

        strategy: StatStrategy
        if strategy_type == "streak":
            strategy = CurrentStreakStrategy()
        elif strategy_type == "completion_rate":
            strategy = CompletionRateStrategy()
        else:
            strategy = TotalProgressStrategy()

        context = StatContext(strategy)
        goal = getattr(habit, "goal", 0.0)
        return context.analyze(logs, goal)
