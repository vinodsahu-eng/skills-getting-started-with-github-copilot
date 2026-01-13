from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "test_student@example.com"

    # Ensure clean state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should fail
    dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert dup.status_code == 400

    # Unregister
    resp_un = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp_un.status_code == 200
    assert email not in activities[activity]["participants"]

    # Unregistering again should return 404
    resp_un2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp_un2.status_code == 404


def test_signup_nonexistent_activity():
    resp = client.post("/activities/NoSuchActivity/signup?email=a@b.com")
    assert resp.status_code == 404


def test_unregister_nonexistent_activity():
    resp = client.post("/activities/NoSuchActivity/unregister?email=a@b.com")
    assert resp.status_code == 404
