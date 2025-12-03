from datetime import date, timedelta

from starlette.testclient import TestClient


def test_create_and_list_habit(client: TestClient) -> None:
    response = client.post(
        "/habits",
        json={
            "name": "Drink Water",
            "description": "8 glasses",
            "category": "Health",
            "type": "numeric",
            "goal": 8.0,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Drink Water"
    habit_id = data["id"]

    response = client.get("/habits")
    assert response.status_code == 200
    habits = response.json()
    assert len(habits) == 1
    assert habits[0]["id"] == habit_id


def test_routine_and_subhabit(client: TestClient) -> None:
    h_resp = client.post(
        "/habits",
        json={
            "name": "Meditate",
            "description": "10 mins",
            "category": "Health",
            "type": "boolean",
            "goal": 1.0,
        },
    )
    habit_id = h_resp.json()["id"]

    r_resp = client.post(
        "/routines",
        json={
            "name": "Morning Routine",
            "description": "Start day well",
            "category": "Health",
        },
    )
    routine_id = r_resp.json()["id"]

    response = client.post(
        f"/habits/{routine_id}/subhabits", params={"child_id": habit_id}
    )
    assert response.status_code == 200

    response = client.get(f"/habits/{routine_id}")
    data = response.json()
    assert len(data["children"]) == 1
    assert data["children"][0]["id"] == habit_id


def test_log_and_stats(client: TestClient) -> None:
    response = client.post(
        "/habits",
        json={
            "name": "Read",
            "description": "Pages",
            "category": "Learning",
            "type": "numeric",
            "goal": 10.0,
        },
    )
    habit_id = response.json()["id"]

    resp = client.post(
        f"/habits/{habit_id}/logs",
        json={"value": 12.0, "date": str(date.today())},
    )
    assert resp.status_code == 201, resp.text

    yesterday = date.today() - timedelta(days=1)
    resp = client.post(
        f"/habits/{habit_id}/logs",
        json={"value": 15.0, "date": str(yesterday)},
    )
    assert resp.status_code == 201

    response = client.get(f"/habits/{habit_id}/stats?stat_type=total")
    assert response.status_code == 200
    assert response.json()["value"] == 27.0

    response = client.get(f"/habits/{habit_id}/stats?stat_type=streak")
    assert response.status_code == 200
    assert response.json()["value"] == 2
