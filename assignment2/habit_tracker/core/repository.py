from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from .habits import HabitComponent, Log


class HabitRepository(ABC):
    @abstractmethod
    def save(self, habit: HabitComponent) -> None:
        pass

    @abstractmethod
    def get(self, habit_id: uuid.UUID) -> HabitComponent | None:
        pass

    @abstractmethod
    def list_all(self) -> list[HabitComponent]:
        pass

    @abstractmethod
    def delete(self, habit_id: uuid.UUID) -> None:
        pass

    @abstractmethod
    def save_log(self, log: Log) -> None:
        pass

    @abstractmethod
    def get_logs(self, habit_id: uuid.UUID) -> list[Log]:
        pass
