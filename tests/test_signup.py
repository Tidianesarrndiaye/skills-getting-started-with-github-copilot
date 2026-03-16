"""
Tests for POST /activities/{activity_name}/signup.

AAA pattern: Arrange → Act → Assert
"""

import src.app as app_module


def test_signup_new_participant_returns_200(client):
    # Arrange: Basketball Team starts with no participants
    activity_name = "Basketball Team"
    email = "alice@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 200


def test_signup_new_participant_returns_success_message(client):
    # Arrange
    activity_name = "Art Club"
    email = "bob@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    data = response.json()
    # Assert: confirmation message mentions the email and activity
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_adds_participant_to_activity(client):
    # Arrange
    activity_name = "Soccer Club"
    email = "carol@mergington.edu"
    # Act
    client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert: participant appears in the in-memory store
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_unknown_activity_returns_404(client):
    # Arrange: activity does not exist
    activity_name = "Unknown Activity"
    email = "dave@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_already_enrolled_returns_400(client):
    # Arrange: michael is already enrolled in Chess Club (initial data)
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
