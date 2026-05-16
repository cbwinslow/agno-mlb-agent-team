"""Smoke tests — verify agents can be imported and key env vars are present."""
import os
import importlib
import pytest


class TestEnvironment:
    """Verify required environment variables are accessible."""

    def test_mlb_repo_path_env_var(self):
        """MLB_REPO_PATH must be set and not use the hardcoded default."""
        val = os.getenv("MLB_REPO_PATH", "")
        assert val != "", "MLB_REPO_PATH must be set in .env"
        assert val != "/home/cbwinslow/mlb-baseball", (
            "MLB_REPO_PATH still uses hardcoded path — set it via .env"
        )

    def test_openai_api_key_present(self):
        assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY must be set"

    def test_github_token_present(self):
        assert os.getenv("GITHUB_TOKEN"), "GITHUB_TOKEN must be set"


class TestAgentImports:
    """Verify each agent module can be imported without crashing."""

    AGENT_MODULES = [
        "agents.coordinator",
        "agents.stats_agent",
        "agents.db_specialist",
        "agents.code_reviewer",
        "agents.docs_writer",
        "agents.api_specialist",
        "agents.app_architect",
        "agents.performance_optimizer",
    ]

    @pytest.mark.parametrize("module_path", AGENT_MODULES)
    def test_agent_module_importable(self, module_path):
        """Each agent file should be importable without raising at module level."""
        try:
            importlib.import_module(module_path)
        except ModuleNotFoundError as e:
            # If the module itself doesn't exist yet, fail clearly
            pytest.fail(f"Could not import {module_path}: {e}")
        except Exception:
            # Other errors (e.g. missing env, API call at import) are also failures
            pytest.fail(f"{module_path} raised an unexpected error during import")


class TestToolWrappers:
    """Unit tests for MLB data tool wrapper functions."""

    def test_mlb_data_tools_importable(self):
        try:
            from tools import mlb_data_tools  # noqa: F401
        except ImportError as e:
            pytest.fail(f"tools.mlb_data_tools not importable: {e}")

    def test_get_player_stats_returns_dict(self, mock_requests_get):
        """get_player_stats should return a dict (mocked API response)."""
        try:
            from tools.mlb_data_tools import get_player_stats
            result = get_player_stats(player_id=660271)  # Juan Soto
            assert isinstance(result, dict)
        except ImportError:
            pytest.skip("mlb_data_tools.get_player_stats not yet implemented")
