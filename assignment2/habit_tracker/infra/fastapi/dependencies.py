from __future__ import annotations

from ...core.services import HabitService
from ...infra.in_memory.repository import InMemoryHabitRepository

# Singleton repository instance
_repo = InMemoryHabitRepository()


def get_habit_service() -> HabitService:
    return HabitService(_repo)
