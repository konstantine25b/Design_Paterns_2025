from datetime import date
from typing import Any

import pytest
from starlette.testclient import TestClient


@pytest.fixture
def water_habit() -> dict[str, Any]:
    return {
        "name": "Drink Water",
        "description": "8 glasses daily",
        "category": "Health",
        "type": "numeric",
        "goal": 8.0,
    }


@pytest.fixture
def exercise_habit() -> dict[str, Any]:
    return {
        "name": "Exercise",
        "description": "30 min workout",
        "category": "Fitness",
        "type": "boolean",
        "goal": 1.0,
    }


@pytest.fixture
def morning_routine() -> dict[str, Any]:
    return {
        "name": "Morning Routine",
        "description": "Start day right",
        "category": "Daily",
    }


def test_should_create_habit_with_id(
    client: TestClient, water_habit: dict[str, Any]
) -> None:
    response = client.post("/habits", json=water_habit)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == water_habit["name"]


def test_should_persist_habit(client: TestClient, water_habit: dict[str, Any]) -> None:
    response = client.post("/habits", json=water_habit)
    habit_id = response.json()["id"]
    response = client.get(f"/habits/{habit_id}")
    assert response.status_code == 200
    assert response.json()["id"] == habit_id


def test_should_return_404_for_unknown_habit(client: TestClient) -> None:
    response = client.get("/habits/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_should_list_multiple_habits(
    client: TestClient, water_habit: dict[str, Any], exercise_habit: dict[str, Any]
) -> None:
    client.post("/habits", json=water_habit)
    client.post("/habits", json=exercise_habit)
    response = client.get("/habits")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_should_list_empty_habits(client: TestClient) -> None:
    response = client.get("/habits")
    assert response.status_code == 200
    assert response.json() == []


def test_should_update_habit(client: TestClient, water_habit: dict[str, Any]) -> None:
    response = client.post("/habits", json=water_habit)
    habit_id = response.json()["id"]
    updated_data = {**water_habit, "name": "Updated Water"}
    response = client.put(f"/habits/{habit_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Water"


def test_should_return_404_when_updating_unknown_habit(
    client: TestClient, water_habit: dict[str, Any]
) -> None:
    response = client.put(
        "/habits/00000000-0000-0000-0000-000000000000", json=water_habit
    )
    assert response.status_code == 404


def test_should_delete_habit(client: TestClient, water_habit: dict[str, Any]) -> None:
    response = client.post("/habits", json=water_habit)
    habit_id = response.json()["id"]
    response = client.delete(f"/habits/{habit_id}")
    assert response.status_code == 204


def test_should_not_find_deleted_habit(
    client: TestClient, water_habit: dict[str, Any]
) -> None:
    response = client.post("/habits", json=water_habit)
    habit_id = response.json()["id"]
    client.delete(f"/habits/{habit_id}")
    response = client.get(f"/habits/{habit_id}")
    assert response.status_code == 404


def test_should_create_routine(
    client: TestClient, morning_routine: dict[str, Any]
) -> None:
    response = client.post("/routines", json=morning_routine)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["children"] == []


def test_should_add_multiple_subhabits(
    client: TestClient, water_habit: dict[str, Any], exercise_habit: dict[str, Any]
) -> None:
    routine_resp = client.post(
        "/routines", json={"name": "R", "description": "D", "category": "C"}
    )
    routine_id = routine_resp.json()["id"]

    habit1_resp = client.post("/habits", json=water_habit)
    habit1_id = habit1_resp.json()["id"]

    habit2_resp = client.post("/habits", json=exercise_habit)
    habit2_id = habit2_resp.json()["id"]

    client.post(f"/habits/{routine_id}/subhabits", params={"child_id": habit1_id})
    client.post(f"/habits/{routine_id}/subhabits", params={"child_id": habit2_id})

    response = client.get(f"/habits/{routine_id}")
    data = response.json()
    assert len(data["children"]) == 2


def test_should_return_400_when_adding_to_leaf_habit(
    client: TestClient, water_habit: dict[str, Any], exercise_habit: dict[str, Any]
) -> None:
    habit1_resp = client.post("/habits", json=water_habit)
    habit1_id = habit1_resp.json()["id"]

    habit2_resp = client.post("/habits", json=exercise_habit)
    habit2_id = habit2_resp.json()["id"]

    response = client.post(
        f"/habits/{habit1_id}/subhabits", params={"child_id": habit2_id}
    )
    assert response.status_code == 400


def test_should_log_single_progress(
    client: TestClient, water_habit: dict[str, Any]
) -> None:
    habit_resp = client.post("/habits", json=water_habit)
    habit_id = habit_resp.json()["id"]

    response = client.post(
        f"/habits/{habit_id}/logs", json={"value": 6.0, "date": str(date.today())}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["value"] == 6.0


def test_should_retrieve_logs(client: TestClient, water_habit: dict[str, Any]) -> None:
    habit_resp = client.post("/habits", json=water_habit)
    habit_id = habit_resp.json()["id"]

    client.post(f"/habits/{habit_id}/logs", json={"value": 6.0})
    client.post(f"/habits/{habit_id}/logs", json={"value": 7.0})

    response = client.get(f"/habits/{habit_id}/logs")
    assert response.status_code == 200
    logs = response.json()
    assert len(logs) == 2


def test_should_return_empty_logs(
    client: TestClient, water_habit: dict[str, Any]
) -> None:
    habit_resp = client.post("/habits", json=water_habit)
    habit_id = habit_resp.json()["id"]

    response = client.get(f"/habits/{habit_id}/logs")
    assert response.status_code == 200
    assert response.json() == []


def test_should_calculate_zero_total_without_logs(
    client: TestClient, water_habit: dict[str, Any]
) -> None:
    habit_resp = client.post("/habits", json=water_habit)
    habit_id = habit_resp.json()["id"]

    response = client.get(f"/habits/{habit_id}/stats?stat_type=total")
    assert response.status_code == 200
    assert response.json()["value"] == 0.0


def test_should_calculate_zero_streak_without_logs(
    client: TestClient, water_habit: dict[str, Any]
) -> None:
    habit_resp = client.post("/habits", json=water_habit)
    habit_id = habit_resp.json()["id"]

    response = client.get(f"/habits/{habit_id}/stats?stat_type=streak")
    assert response.status_code == 200
    assert response.json()["value"] == 0


def test_should_return_404_for_unknown_habit_stats(client: TestClient) -> None:
    response = client.get(
        "/habits/00000000-0000-0000-0000-000000000000/stats?stat_type=total"
    )
    assert response.status_code == 404


def test_should_default_to_total_stats(
    client: TestClient, water_habit: dict[str, Any]
) -> None:
    habit_resp = client.post("/habits", json=water_habit)
    habit_id = habit_resp.json()["id"]
    client.post(f"/habits/{habit_id}/logs", json={"value": 5.0})

    response = client.get(f"/habits/{habit_id}/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["stat_type"] == "total"
    assert data["value"] == 5.0


def test_should_include_created_date(
    client: TestClient, water_habit: dict[str, Any]
) -> None:
    response = client.post("/habits", json=water_habit)
    data = response.json()
    assert "created_at" in data
    assert data["created_at"] == str(date.today())


def test_should_handle_boolean_habit(client: TestClient) -> None:
    habit = {
        "name": "Meditate",
        "description": "10 min",
        "category": "Wellness",
        "type": "boolean",
        "goal": 1.0,
    }
    response = client.post("/habits", json=habit)
    assert response.status_code == 201
    data = response.json()
    assert data["type"] == "boolean"
    assert data["goal"] == 1.0


def test_should_handle_numeric_habit(client: TestClient) -> None:
    habit = {
        "name": "Read",
        "description": "Pages",
        "category": "Learning",
        "type": "numeric",
        "goal": 30.0,
    }
    response = client.post("/habits", json=habit)
    assert response.status_code == 201
    data = response.json()
    assert data["type"] == "numeric"
    assert data["goal"] == 30.0

