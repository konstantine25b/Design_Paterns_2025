from __future__ import annotations

import uuid
from datetime import date

from pydantic import BaseModel, ConfigDict

from ...core.habits import HabitType


class CreateHabitRequest(BaseModel):
    name: str
    description: str
    category: str
    type: HabitType
    goal: float


class CreateRoutineRequest(BaseModel):
    name: str
    description: str
    category: str


class HabitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str
    category: str
    created_at: date
    type: HabitType | None = None
    goal: float | None = None
    children: list[HabitResponse] = []


class LogRequest(BaseModel):
    value: float
    date: str | None = None


class LogResponse(BaseModel):
    habit_id: uuid.UUID
    date: date
    value: float


class StatResponse(BaseModel):
    stat_type: str
    value: float | int
