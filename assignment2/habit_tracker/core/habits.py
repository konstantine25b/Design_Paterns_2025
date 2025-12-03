from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class HabitType(str, Enum):
    BOOLEAN = "boolean"
    NUMERIC = "numeric"


@dataclass
class Log:
    habit_id: uuid.UUID
    date: date
    value: float  # 1.0 for boolean true, 0.0 for false, or actual number


@dataclass(kw_only=True)
class HabitComponent(ABC):
    id: uuid.UUID
    name: str
    description: str
    created_at: date

    @abstractmethod
    def is_composite(self) -> bool:
        pass

    @abstractmethod
    def add(self, component: HabitComponent) -> None:
        pass

    @abstractmethod
    def remove(self, component: HabitComponent) -> None:
        pass

    @abstractmethod
    def get_children(self) -> list[HabitComponent]:
        pass


@dataclass(kw_only=True)
class Habit(HabitComponent):
    category: str
    type: HabitType
    goal: float  # e.g. 1 for boolean, N for numeric
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: date = field(default_factory=date.today)

    def is_composite(self) -> bool:
        return False

    def add(self, component: HabitComponent) -> None:
        raise NotImplementedError("Cannot add child to a leaf habit")

    def remove(self, component: HabitComponent) -> None:
        raise NotImplementedError("Cannot remove child from a leaf habit")

    def get_children(self) -> list[HabitComponent]:
        return []


@dataclass(kw_only=True)
class Routine(HabitComponent):
    category: str
    children: list[HabitComponent] = field(default_factory=list)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: date = field(default_factory=date.today)

    def is_composite(self) -> bool:
        return True

    def add(self, component: HabitComponent) -> None:
        self.children.append(component)

    def remove(self, component: HabitComponent) -> None:
        self.children.remove(component)

    def get_children(self) -> list[HabitComponent]:
        return self.children
