"""
Tests for GET /activities.

AAA pattern: Arrange → Act → Assert
"""

EXPECTED_ACTIVITIES = [
    "Chess Club",
    "Programming Class",
    "Gym Class",
    "Basketball Team",
    "Soccer Club",
    "Art Club",
    "Drama Society",
    "Math Olympiad",
    "Science Club",
]


def test_get_activities_returns_200(client):
    # Arrange: default in-memory store (restored by reset_activities fixture)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200


def test_get_activities_returns_all_activities(client):
    # Arrange: default in-memory store
    # Act
    response = client.get("/activities")
    data = response.json()
    # Assert: all nine activities must be present
    for name in EXPECTED_ACTIVITIES:
        assert name in data, f"Activity '{name}' missing from /activities response"


def test_get_activities_response_has_expected_fields(client):
    # Arrange: check structure for a known activity
    # Act
    response = client.get("/activities")
    data = response.json()
    chess = data["Chess Club"]
    # Assert: each activity has the expected fields
    assert "description" in chess
    assert "schedule" in chess
    assert "max_participants" in chess
    assert "participants" in chess
    assert isinstance(chess["participants"], list)


def test_get_activities_no_cache_headers(client):
    # Arrange: no special state required
    # Act
    response = client.get("/activities")
    # Assert: the API must opt-out of browser caching
    assert response.headers.get("cache-control") == "no-store"
    assert response.headers.get("pragma") == "no-cache"
