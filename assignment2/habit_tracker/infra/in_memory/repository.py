from __future__ import annotations

import uuid

from ...core.habits import HabitComponent, Log
from ...core.repository import HabitRepository


class InMemoryHabitRepository(HabitRepository):
    def __init__(self) -> None:
        self._habits: dict[uuid.UUID, HabitComponent] = {}
        self._logs: dict[uuid.UUID, list[Log]] = {}

    def save(self, habit: HabitComponent) -> None:
        self._habits[habit.id] = habit

    def get(self, habit_id: uuid.UUID) -> HabitComponent | None:
        return self._habits.get(habit_id)

    def list_all(self) -> list[HabitComponent]:
        return list(self._habits.values())

    def delete(self, habit_id: uuid.UUID) -> None:
        if habit_id in self._habits:
            del self._habits[habit_id]

    def save_log(self, log: Log) -> None:
        if log.habit_id not in self._logs:
            self._logs[log.habit_id] = []
        self._logs[log.habit_id].append(log)

    def get_logs(self, habit_id: uuid.UUID) -> list[Log]:
        return self._logs.get(habit_id, [])
