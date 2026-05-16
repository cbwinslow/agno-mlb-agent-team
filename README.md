# Agno MLB Agent Team

A multi-agent AI team using [Agno](https://agno.com) that autonomously analyzes, completes, and maintains the [mlb-baseball](https://github.com/cbwinslow/mlb-baseball) project using **100% FREE tier models**.

## Overview

This agent team operates like a software development squad with distinct roles, working collaboratively in a democratic open-source style:

| Agent | Role | Model | Cost |
|-------|------|-------|------|
| **Coordinator** | Task orchestration | Gemini 3.1 Flash | FREE |
| **AppArchitect** | System design, docs generation | Nemotron 120B | FREE |
| **DBSpecialist** | PostgreSQL, pgvector, embeddings | MiniMax M2.5 | FREE |
| **StatsAgent** | Sabermetrics, statistical modeling | Gemini 3.1 Flash | FREE |
| **APISpecialist** | REST/GraphQL API design | Nemotron 120B | FREE |
| **CodeReviewer** | Peer code review | Gemini 3.1 Flash | FREE |
| **PerformanceOptimizer** | Query optimization, profiling | Nemotron 120B | FREE |
| **DocsWriter** | SRS, README, documentation | Gemini 3.1 Flash | FREE |
| **Coder-1** | Feature implementation | Ring Reasoning | FREE |
| **Coder-2** | Feature implementation | GLM 4.5 | FREE |
| **Coder-3** | Feature implementation | GPT-OSS 120B | FREE |
| **Coder-4** | Feature implementation | Kilo Gateway | BYOK |

## Architecture

```
                         ┌─────────────────────────────────────────┐
                         │              Coordinator                │
                         │         (Gemini 3.1 Flash - FREE)     │
                         └──────────────────────┬────────────────┘
                                              │
          ┌───────────────────────────────────┼───────────────────────────────────┐
          │                                   │                                   │
          ▼                                   ▼                                   ▼
┌─────────────────────┐          ┌─────────────────────┐          ┌─────────────────────┐
│   AppArchitect      │          │       Coder-1        │          │   CodeReviewer      │
│ (Nemotron 120B FREE)│          │ (Ring Reasoning FREE)│          │(Gemini 3.1 Flash)  │
└──────────┬──────────┘          └──────────┬───────────┘          └─────────────────────┘
           │                                 │
           │                    ┌─────────────┼─────────────┐
           │                    │             │             │
           ▼                    ▼             ▼             ▼
┌─────────────────────┐  ┌────────────┐ ┌────────────┐ ┌────────────┐
│    DBSpecialist     │  │  Coder-2   │ │  Coder-3   │ │  Coder-4   │
│(MiniMax M2.5 FREE) │  │(GLM FREE)  │ │(GPT-OSS)   │ │(Kilo GW)   │
└──────────┬──────────┘  └────────────┘ └────────────┘ └────────────┘
           │
┌──────────┴──────────┐
│    StatsAgent       │
│(Gemini 3.1 Flash)  │
└─────────────────────┘
```

## Quick Start

### 1. Create Virtual Environment & Install

```bash
cd ~/infra/agno-mlb-team
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit with your API keys (all FREE tier!)
# - GOOGLE_API_KEY: Get at https://aistudio.google.com/app/apikey
# - OPENROUTER_API_KEY: Get at https://openrouter.ai/keys
# - KILO_API_KEY: Get at https://app.kilo.ai/settings/api-keys
```

### 3. Verify Setup

```bash
source .venv/bin/activate
python -c "from config import ALL_AGENTS; print(f'Agents: {len(ALL_AGENTS)}')"
```

### 4. Run the Workbench

```bash
# Interactive mode
source .venv/bin/activate
python workbench.py

# Or with uv
uv run python workbench.py
```

## External CLI Tools

The team can also leverage these terminal coding tools:

| Tool | Description | Command |
|------|-------------|---------|
| **Cline CLI** | AI coding with MCP | `cline <task>` |
| **KiloCode CLI** | 500+ models via gateway | `kilocode` |
| **OpenCode CLI** | AI coding assistant | `opencode` |

## Task Routing

| Task Type | Agents Invoked |
|-----------|----------------|
| `feature` | AppArchitect → DBSpecialist → Coder → CodeReviewer → Docs |
| `bug` | Coder → CodeReviewer |
| `database` | DBSpecialist |
| `statistics` | StatsAgent |
| `architecture` | AppArchitect |
| `code_review` | CodeReviewer → AppArchitect → Coder |

## Monthly Cost

**$0** - All agents use free tier models only!

- Gemini Direct: Unlimited free usage
- OpenRouter FREE models: No cost
- Kilo Gateway: Bring your own API key (zero markup)

## Project Structure

```
agno-mlb-team/
├── agents/           # Agent implementations (12 agents)
├── config/          # Model & team configuration
├── runtime/         # AgentOS runtime setup
├── prompts/         # Agent system prompts
├── tools/           # Custom tools (GitHub, MCP)
├── workbench.py     # Development entry point
├── production.py    # Production deployment
└── requirements.txt # Dependencies
├── tests/              # Pytest suite (conftest.py + smoke tests)
├── .env.example        # Environment variable template
├── pyproject.toml      # Project metadata & dependencies (uv/pip)
## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/cbwinslow/agno-mlb-agent-team.git
cd agno-mlb-agent-team

# Recommended: use uv
uv sync --extra dev

# Or with pip
pip install -e ".[dev]"
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and fill in your API keys and MLB_REPO_PATH
```

### 3. Run the workbench (local dev)

```bash
python workbench.py
```

### 4. Run in production mode

```bash
python production.py
# AgentOS API will be available at http://localhost:7777
```

### 5. Run tests

```bash
pytest tests/ -v
```

## Environment Variables

See [`.env.example`](.env.example) for a full annotated reference. Key variables:

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | Yes | OpenAI API key for GPT-4o agents |
| `ANTHROPIC_API_KEY` | No | Anthropic key (for Claude-backed agents) |
| `MLB_REPO_PATH` | Yes | Path to local Retrosheet/Statcast data directory |
| `GITHUB_TOKEN` | Yes | GitHub PAT for repo tools |
| `DATABASE_URL` | No | PostgreSQL connection string (defaults to DuckDB) |
| `QDRANT_URL` | No | Qdrant vector store URL for agent memory |

└── CHANGELOG.md        # Version history
```

## Documentation

- `PLAN.md` - Full implementation plan
- `config/models.py` - Model configurations
- `config/team_config.py` - Team topology

## License

MIT
