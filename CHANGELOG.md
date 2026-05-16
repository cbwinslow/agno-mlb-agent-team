# Changelog

All notable changes to this project will be documented in this file.
This project adheres to [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.

## [Unreleased]

### Added
- `pyproject.toml` with full dependency specification, dev extras, and tool configuration (ruff, mypy, pytest)
- `.env.example` documenting all required and optional environment variables
- `tests/` directory with `conftest.py` and initial smoke tests for agent instantiation and tool wrappers
- `CHANGELOG.md` to track project history

### Changed
- Cleaned up 22 AI-generated completion artifact files from repo root (e.g. `DONE.md`, `FINAL_ANSWER.md`, `TASK_COMPLETED.md`, etc.)

### Fixed
- `MLB_REPO_PATH` hardcoded to `/home/cbwinslow/mlb-baseball` — now driven by env var

## [0.1.0] - 2026-05-12

### Added
- Initial commit: 12-agent AI team implementation on Agno framework
- Agent roster: Coordinator, AppArchitect, DBSpecialist, StatsAgent, APISpecialist, CodeReviewer, DocsWriter, Coder-1/2/3/4, PerformanceOptimizer
- Tool integrations: GitHub, database (PostgreSQL + pgvector), local filesystem, MCP server config
- AgentOS runtime with 50+ API endpoints
- `production.py` with OpenTelemetry tracing bootstrap
- `workbench.py` for local development
- `requirements.txt` with initial dependency list
