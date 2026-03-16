"""
Tests for POST /activities/{activity_name}/unregister.

AAA pattern: Arrange → Act → Assert
"""

import src.app as app_module


def test_unregister_enrolled_participant_returns_200(client):
    # Arrange: michael is enrolled in Chess Club (initial data)
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    # Assert
    assert response.status_code == 200


def test_unregister_enrolled_participant_returns_success_message(client):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    data = response.json()
    # Assert: confirmation message mentions the email and activity
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_unregister_removes_participant_from_activity(client):
    # Arrange
    activity_name = "Gym Class"
    email = "john@mergington.edu"
    # Act
    client.post(f"/activities/{activity_name}/unregister?email={email}")
    # Assert: participant no longer in the in-memory store
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    # Arrange: activity does not exist
    activity_name = "Nonexistent Activity"
    email = "eve@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_not_enrolled_participant_returns_404(client):
    # Arrange: email not enrolled in the activity
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
