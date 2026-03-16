"""
Tests for GET / (root redirect).

AAA pattern: Arrange → Act → Assert
"""


def test_root_redirects_to_static_index(client):
    # Arrange: no specific state required – route has no dependencies
    # Act
    response = client.get("/", follow_redirects=False)
    # Assert: FastAPI should issue a redirect to the static frontend
    assert response.status_code in (301, 302, 307, 308)
    assert response.headers["location"] == "/static/index.html"
