import pytest
from fastapi.testclient import TestClient

from habit_tracker.core.services import HabitService
from habit_tracker.infra.fastapi.dependencies import get_habit_service
from habit_tracker.infra.in_memory.repository import InMemoryHabitRepository
from habit_tracker.runner.app import app


@pytest.fixture
def service() -> HabitService:
    repo = InMemoryHabitRepository()
    return HabitService(repo)


@pytest.fixture
def client(service: HabitService) -> TestClient:
    app.dependency_overrides[get_habit_service] = lambda: service
    return TestClient(app)
