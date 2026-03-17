import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

@pytest.mark.parametrize("activity,email", [
    ("Chess Club", "newstudent@mergington.edu"),
    ("Programming Class", "coder@mergington.edu")
])
def test_signup_for_activity(activity, email):
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]


def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup", params={"email": "ghost@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant():
    # First, sign up a participant
    activity = "Art Club"
    email = "remove@mergington.edu"
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Now, unregister
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]


def test_unregister_activity_not_found():
    response = client.delete("/activities/Nonexistent/unregister", params={"email": "ghost@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_not_found():
    response = client.delete("/activities/Chess Club/unregister", params={"email": "ghost@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
