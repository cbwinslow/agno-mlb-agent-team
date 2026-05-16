"""Pytest configuration and shared fixtures for agno-mlb-agent-team tests."""
import os
import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Set safe dummy env vars so agents can be instantiated without real credentials."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-dummy")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test-dummy")
    monkeypatch.setenv("GITHUB_TOKEN", "ghp_test_dummy")
    monkeypatch.setenv("MLB_REPO_PATH", "/tmp/mlb-test")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./test.db")
    monkeypatch.setenv("AGNO_PORT", "7778")


@pytest.fixture
def mock_openai_client():
    """Return a mock OpenAI client to prevent live API calls."""
    with patch("openai.OpenAI") as mock:
        mock.return_value = MagicMock()
        yield mock


@pytest.fixture
def mock_requests_get():
    """Mock requests.get for MLB data tool tests."""
    with patch("requests.get") as mock:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock.return_value = mock_response
        yield mock
