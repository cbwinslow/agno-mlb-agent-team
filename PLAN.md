# Agno MLB Agent Team - Implementation Plan

## Overview

Create a multi-agent team using **Agno** that autonomously analyzes, completes, and maintains the **mlb-baseball** GitHub project. The team operates like a software development squad with distinct roles working collaboratively.

---

## Project Structure

```
~/infra/agno-mlb-team/
├── README.md                    # Project overview
├── PLAN.md                      # This document
├── agents/
│   ├── __init__.py
│   ├── coordinator.py           # Orchestrates the team
│   ├── architect.py             # Technical design & patterns
│   ├── coder.py                 # Implements features
│   ├── tester.py               # Writes & validates tests
│   └── docs_writer.py           # Maintains documentation
├── config/
│   ├── __init__.py
│   ├── models.py                # Model configurations
│   └── team_config.py           # Team topology
├── runtime/
│   ├── __init__.py
│   ├── agentos_server.py        # AgentOS runtime setup
│   └── api_server.py            # FastAPI server config
├── prompts/
│   ├── coordinator.md           # Coordinator instructions
│   ├── architect.md            # Architect instructions
│   ├── coder.md                # Coder instructions
│   ├── tester.md               # Tester instructions
│   └── docs_writer.md          # Docs writer instructions
├── tools/
│   ├── __init__.py
│   ├── github_tools.py          # GitHub API integration
│   └── file_tools.py            # File system operations
├── workbench.py                  # Development entry point
├── production.py                 # Production entry point
└── requirements.txt             # Python dependencies
```

---

## Agent Team Topology

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
           │                    │             │             │
           ▼                    └─────────────┴─────────────┘
┌─────────────────────┐                      │
│    StatsAgent       │          ┌────────────┴────────────┐
│(Gemini 3.1 Flash)  │          │   APISpecialist         │
└─────────────────────┘          │ (Nemotron 120B FREE)   │
                                 └────────────┬────────────┘
                                              │
                    ┌─────────────────────────┴─────────────────────────┐
                    ▼                                                   ▼
         ┌─────────────────────┐                           ┌─────────────────────┐
         │    DocsWriter       │                           │PerformanceOptimizer │
         │(Gemini 3.1 Flash)  │                           │(Nemotron 120B FREE)│
         └─────────────────────┘                           └─────────────────────┘
```

---

## Free Model Providers

All agents use **FREE tier models** only - no cost!

### 1. Gemini Direct (UNLIMITED FREE)
- **Model**: `gemini-3.1-flash`
- **Provider**: Google AI (Direct API)
- **Context**: 1M tokens
- **Use for**: Coordinator, StatsAgent, CodeReviewer, DocsWriter

### 2. OpenRouter FREE Models
Only models with "free" in the name:

| Model | Context | Use For |
|-------|---------|---------|
| `nvidia/nemotron-3-super-120b-a12b:free` | 1M | AppArchitect, APISpecialist, PerformanceOptimizer |
| `inclusionai/ring-2.6-1t:free` | 262K | Coder-1 (reasoning) |
| `openai/gpt-oss-120b:free` | 32K | Coder-3 |
| `z-ai/glm-4.5-air:free` | 32K | Coder-2 |
| `minimax/minimax-m2.5:free` | 32K | DBSpecialist |

### 3. Kilo Gateway (BYOK - Bring Your Own Key)
- **Base URL**: `https://api.kilo.ai/api/gateway`
- **API**: OpenAI-compatible
- **Use for**: Coder-4 (flexible model selection)

---

## Agent Roles & Responsibilities

### 1. Coordinator Agent
**Purpose**: Team lead that receives tasks, decomposes work, and assigns to specialists.

**Capabilities**:
- Parse user requests into actionable tasks
- Route tasks to appropriate agents
- Track progress and dependencies
- Ask clarifying questions when requirements are ambiguous
- Report status and results to user

**Tools**: GitHub API, File System, Team Communication

---

### 2. AppArchitect Agent
**Purpose**: Full-stack application design, system architecture, industry best practices.

**Capabilities**:
- Design complete system architectures
- Establish coding standards (SOLID, DRY, KISS)
- Define API contracts and interfaces
- Plan scalability and performance strategies
- Security auditing
- Deployment architecture (Docker, CI/CD)
- Code review for best practices

**Tools**: FileSystem, Shell, Linting

---

### 3. DBSpecialist Agent
**Purpose**: PostgreSQL database expert, pgvector embeddings, schema design.

**Capabilities**:
- Design PostgreSQL schemas and tables
- Implement pgvector for semantic search
- Write optimized SQL queries
- Create Alembic migrations
- Set up and optimize indexes
- Query performance analysis
- Data modeling for complex relationships

**Tools**: FileSystem, Shell (psql), GitHub API

---

### 4. StatsAgent
**Purpose**: Statistical analysis, sabermetrics, data modeling for MLB.

**Capabilities**:
- Implement advanced baseball statistics (OPS, WAR, FIP, xwOBA)
- Build predictive models (player projections)
- Design data aggregation pipelines
- Data validation and quality checks
- Create statistical reports and insights
- Work with pandas, numpy, scipy

**Tools**: FileSystem, Shell, Python

---

### 5. Architect Agent
**Purpose**: Technical design authority - defines patterns, data models, and system structure.

**Capabilities**:
- Analyze existing codebase structure
- Design data models (SQLAlchemy, Pydantic)
- Define API schemas
- Establish coding patterns and conventions
- Review proposed changes for technical fit
- Identify technical debt and improvements

**Tools**: Code Analysis, GitHub API, File System

---

### 3. Coder Agent
**Purpose**: Implements features, fixes bugs, and writes code.

**Capabilities**:
- Write Python code (data pipelines, APIs, CLI tools)
- Create/modify database schemas
- Implement API endpoints
- Build data processing pipelines (ETL)
- Integrate with external APIs (MLB Stats API, FanGraphs)
- Follow project coding standards

**Tools**: Code Editor, GitHub API, Shell, File System

---

### 4. Tester Agent
**Purpose**: Ensures code quality through testing and validation.

**Capabilities**:
- Write unit tests (pytest)
- Write integration tests
- Verify code functionality
- Check type hints and linting
- Validate data pipeline outputs
- Ensure test coverage meets standards

**Tools**: pytest, mypy, ruff, Shell

---

### 5. Docs Writer Agent
**Purpose**: Maintains project documentation.

**Capabilities**:
- Update README files
- Write API documentation
- Document data models
- Create usage examples
- Maintain changelog
- Update deployment guides

**Tools**: File System, GitHub API

---

## Workflow Patterns

### Pattern 1: Feature Request (Full Pipeline)
```
User → Coordinator → AppArchitect (design) → DBSpecialist (schema) → Coder (implement) → Tester (verify) → DocsWriter (document) → Coordinator → User
```

### Pattern 2: Quick Feature (Database Focus)
```
User → Coordinator → DBSpecialist (schema) → Coder (implement) → Tester (verify) → Coordinator → User
```

### Pattern 3: Bug Fix
```
User → Coordinator → Coder (fix) → Tester (verify) → Coordinator → User
```

### Pattern 4: Statistical Analysis
```
User → Coordinator → StatsAgent (analyze) → Coder (implement) → Tester (verify) → Coordinator → User
```

### Pattern 5: Database/Embeddings Work
```
User → Coordinator → DBSpecialist (design/optimize) → Coordinator → User
```

### Pattern 6: Architecture Review
```
User → Coordinator → AppArchitect (review) → Coordinator → User
```

---

## Interaction Protocol

### Agent-to-Agent Communication

Each agent can invoke other agents through Agno's team primitives:

```python
# Example: Architect asks Coder to implement
self.coder_agent.run(
    f"Implement the following design: {design_spec}",
    context={"task_id": task_id}
)
```

### Asking Questions

When agents need clarification:

```python
# Agent pauses and asks coordinator
self.coordinator.ask_question(
    agent_id=self.id,
    question="What MLB statistics should we prioritize?",
    options=["Pitching", "Hitting", "Fielding", "All"]
)
```

---

## Implementation Phases

### Phase 1: Foundation
- [ ] Create directory structure
- [ ] Set up Python package (`__init__.py` files)
- [ ] Create requirements.txt
- [ ] Define base agent class structure
- [ ] Set up logging configuration

### Phase 2: Agent Implementation
- [ ] Implement Coordinator agent
- [ ] Implement Architect agent
- [ ] Implement Coder agent
- [ ] Implement Tester agent
- [ ] Implement Docs Writer agent

### Phase 3: Tools & Integrations
- [ ] Implement GitHub tools
- [ ] Implement file system tools
- [ ] Add MLB API tools
- [ ] Configure model providers

### Phase 4: Runtime & Testing
- [ ] Configure AgentOS runtime
- [ ] Set up FastAPI server
- [ ] Create workbench entry point
- [ ] Test agent interactions
- [ ] Verify team coordination

### Phase 5: Production Deployment
- [ ] Configure production settings
- [ ] Set up database persistence
- [ ] Add authentication (optional)
- [ ] Create deployment scripts

---

## Model Configuration

### Primary Models

| Agent | Model | Purpose |
|-------|-------|---------|
| Coordinator | `gpt-4o` | High-level reasoning, planning |
| Architect | `gpt-4o` | Code analysis, design |
| Coder | `gpt-4o` | Code generation |
| Tester | `gpt-4o-mini` | Validation, smaller tasks |
| Docs Writer | `gpt-4o-mini` | Writing, lower cost |

### Provider Setup

```python
# config/models.py
MODELS = {
    "coordinator": "openai/gpt-4o",
    "architect": "openai/gpt-4o",
    "coder": "openai/gpt-4o",
    "tester": "openai/gpt-4o-mini",
    "docs_writer": "openai/gpt-4o-mini",
}
```

---

## GitHub Integration

### Repository Operations

- Clone/fetch repository
- Read files and directories
- Create/update files
- Commit and push changes
- Create Pull Requests
- Manage branches

### Agent Behavior

1. **Coder** commits work to feature branches
2. **Coordinator** reviews and merges
3. **Docs Writer** updates CHANGELOG

---

## Memory & State

### Agent Memory

Each agent maintains:
- Task history
- Code context
- Conversation history
- User preferences

### Shared Knowledge

```python
# Shared context across team
SHARED_CONTEXT = {
    "repo_url": "https://github.com/cbwinslow/mlb-baseball",
    "repo_path": "/path/to/mlb-baseball",
    "current_branch": "main",
    "open_issues": [],
    "in_progress_tasks": [],
}
```

---

## Configuration Files

### team_config.py
```python
TEAM_CONFIG = {
    "name": "mlb-agent-team",
    "description": "AI agent team for mlb-baseball project",
    "agents": [...],
    "routing": {...},
    "permissions": {...},
}
```

### environment.py
```python
# Environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MLB_API_KEY = os.getenv("MLB_API_KEY")
```

---

## Usage Examples

### Development Mode (Workbench)

```bash
cd ~/infra/agno-mlb-team
uv pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
export GITHUB_TOKEN=ghp_...

# Interactive workbench
uv run python workbench.py
```

### Production Mode

```bash
uv run python production.py
# Starts FastAPI server with 50+ endpoints
```

### Programmatic Usage

```python
from agents.coordinator import CoordinatorAgent

coordinator = CoordinatorAgent(
    repo_url="https://github.com/cbwinslow/mlb-baseball"
)

# Ask the team to implement a feature
result = coordinator.run(
    "Add player career stats tracking"
)
```

---

## Dependencies

```
# requirements.txt
agno[os]>=1.0.0
openai>=1.0.0
github3.py>=3.2.0
pydantic>=2.0.0
sqlalchemy>=2.0.0
pytest>=7.0.0
ruff>=0.1.0
mypy>=1.0.0
python-dotenv>=1.0.0
```

---

## Success Criteria

1. **Team Autonomy**: Agents can complete features with minimal human input
2. **Code Quality**: Generated code passes linting and type checking
3. **Documentation**: All new features include docs
4. **Testing**: Critical paths have test coverage
5. **GitHub Integration**: Agents can push PRs and manage issues
6. **User Satisfaction**: User can request features in natural language

---

## Next Steps

1. Approve this plan
2. Proceed with Phase 1: Foundation
3. Set up repository access (GitHub token)
4. Configure API keys
5. Implement base agent structure

---

## Questions for User

1. **LLM Provider**: Should we use OpenAI exclusively, or include Anthropic/Google models?
2. **GitHub Access**: Do you want agents to auto-push branches and create PRs, or just generate code for review?
3. **Database**: Should agents create/modify the PostgreSQL schema directly?
4. **External APIs**: Should agents have access to MLB Stats API for live data testing?
5. **Deployment Target**: Local Docker, or cloud deployment (Vercel, Railway, etc.)?
