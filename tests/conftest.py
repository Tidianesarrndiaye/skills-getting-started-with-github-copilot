"""
Shared fixtures for FastAPI backend tests.

- `client`: a TestClient instance connected to the FastAPI app.
- `reset_activities`: autouse fixture that deep-copies the original
  `activities` dict state before each test and restores it after,
  guaranteeing full test isolation on the in-memory store.
"""
import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module
from src.app import app

# ---------------------------------------------------------------------------
# Snapshot of the initial in-memory activity store captured at import time.
# Used by reset_activities to restore state before each test.
# ---------------------------------------------------------------------------
_INITIAL_ACTIVITIES: dict = copy.deepcopy(app_module.activities)


@pytest.fixture
def client() -> TestClient:
    """Return a synchronous TestClient for the FastAPI application."""
    return TestClient(app, raise_server_exceptions=True)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Restore the global `activities` dict to its initial state
    before every test so mutations made in one test cannot leak
    into another, regardless of execution order.
    """
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_INITIAL_ACTIVITIES))
    yield
    # Post-test cleanup (defensive: mirror the setup)
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_INITIAL_ACTIVITIES))
