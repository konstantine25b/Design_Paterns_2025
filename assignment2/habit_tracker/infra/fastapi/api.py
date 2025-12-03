from __future__ import annotations

import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from ...core.habits import Habit, HabitComponent, Routine
from ...core.services import HabitService
from .dependencies import get_habit_service
from .schemas import (
    CreateHabitRequest,
    CreateRoutineRequest,
    HabitResponse,
    LogRequest,
    LogResponse,
    StatResponse,
)

router = APIRouter()


def to_response(component: HabitComponent) -> HabitResponse:
    # Helper to convert Domain entity to Pydantic model
    # Handle polymorphism manually or via fields

    # Basic fields
    data: dict[str, Any] = {
        "id": component.id,
        "name": component.name,
        "description": component.description,
        "category": getattr(component, "category", ""),
        "created_at": component.created_at,
        "children": [],
        "type": None,
        "goal": None,
    }

    if isinstance(component, Habit):
        data["type"] = component.type
        data["goal"] = component.goal

    if isinstance(component, Routine):
        data["children"] = [to_response(child) for child in component.children]

    return HabitResponse(**data)


@router.post(
    "/habits", response_model=HabitResponse, status_code=status.HTTP_201_CREATED
)
def create_habit(
    request: CreateHabitRequest,
    service: HabitService = Depends(get_habit_service),
) -> HabitResponse:
    habit = service.create_habit(
        name=request.name,
        description=request.description,
        category=request.category,
        habit_type=request.type,
        goal=request.goal,
    )
    return to_response(habit)


@router.post(
    "/routines", response_model=HabitResponse, status_code=status.HTTP_201_CREATED
)
def create_routine(
    request: CreateRoutineRequest,
    service: HabitService = Depends(get_habit_service),
) -> HabitResponse:
    routine = service.create_routine(
        name=request.name,
        description=request.description,
        category=request.category,
    )
    return to_response(routine)


@router.get("/habits", response_model=list[HabitResponse])
def list_habits(
    service: HabitService = Depends(get_habit_service),
) -> list[HabitResponse]:
    habits = service.list_habits()
    return [to_response(h) for h in habits]


@router.get("/habits/{habit_id}", response_model=HabitResponse)
def get_habit(
    habit_id: uuid.UUID,
    service: HabitService = Depends(get_habit_service),
) -> HabitResponse:
    habit = service.get_habit(habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return to_response(habit)


@router.put("/habits/{habit_id}", response_model=HabitResponse)
def update_habit(
    habit_id: uuid.UUID,
    request: CreateHabitRequest,
    # Reuse create request for update fields
    # For simplicity, we assume full update or partial.
    # For "student-like", reusing CreateSchema implies full update.
    # I'll make a separate UpdateHabitRequest or just use params.
    # Let's assume we pass fields we want to update.
    # I'll use Body with optional fields? Or simpler: just expect full payload.
    service: HabitService = Depends(get_habit_service),
) -> HabitResponse:
    # Using CreateHabitRequest means we must send all fields.
    updated = service.update_habit(
        habit_id,
        name=request.name,
        description=request.description,
        category=request.category,
        goal=request.goal,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Habit not found")
    return to_response(updated)


@router.delete("/habits/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(
    habit_id: uuid.UUID,
    service: HabitService = Depends(get_habit_service),
) -> None:
    service.delete_habit(habit_id)


@router.post("/habits/{habit_id}/subhabits", status_code=status.HTTP_200_OK)
def add_subhabit(
    habit_id: uuid.UUID,
    child_id: uuid.UUID,  # Query or Body? Usually body {"child_id": "..."}
    # I'll take it as query param for simplicity or body. Body is cleaner.
    service: HabitService = Depends(get_habit_service),
) -> None:
    try:
        service.add_subhabit(habit_id, child_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post(
    "/habits/{habit_id}/logs",
    response_model=LogResponse,
    status_code=status.HTTP_201_CREATED,
)
def log_progress(
    habit_id: uuid.UUID,
    request: LogRequest,
    service: HabitService = Depends(get_habit_service),
) -> LogResponse:
    from datetime import date as date_cls

    log_date = None
    if request.date:
        log_date = date_cls.fromisoformat(request.date)

    log = service.log_progress(habit_id, request.value, log_date)
    return LogResponse(habit_id=log.habit_id, date=log.date, value=log.value)


@router.get("/habits/{habit_id}/logs", response_model=list[LogResponse])
def list_logs(
    habit_id: uuid.UUID,
    service: HabitService = Depends(get_habit_service),
) -> list[LogResponse]:
    logs = service.get_logs(habit_id)
    return [
        LogResponse(
            habit_id=log_entry.habit_id, date=log_entry.date, value=log_entry.value
        )
        for log_entry in logs
    ]


@router.get("/habits/{habit_id}/stats", response_model=StatResponse)
def get_stats(
    habit_id: uuid.UUID,
    stat_type: str = "total",
    service: HabitService = Depends(get_habit_service),
) -> StatResponse:
    try:
        value = service.get_stats(habit_id, stat_type)
        return StatResponse(stat_type=stat_type, value=value)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
