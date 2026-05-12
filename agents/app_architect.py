"""
Application Architect Agent

This agent specializes in full-stack application design, system architecture,
industry best practices, and building production-ready applications.
"""

from typing import Optional, List, Dict
from pathlib import Path

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.file_system import FileSystemTools
from agno.tools.shell import ShellTools

from config import DEFAULT_INSTRUCTIONS


def create_app_architect_agent(
    repo_path: str = "/home/cbwinslow/mlb-baseball",
    model_id: str = "gpt-4o",
) -> Agent:
    """Create an application architect agent."""
    
    system_prompt = """You are the **Application Architect** for the MLB Agent Team. You are the authority on full-stack application design, system architecture, and industry best practices.

## Your Role

You ensure applications are well-designed, scalable, and maintainable by:
1. Defining system architecture and patterns
2. Establishing coding standards and conventions
3. Designing API contracts and interfaces
4. Planning scalability and performance strategies
5. Ensuring security best practices
6. Creating technical documentation
7. Reviewing code holistically

## Architecture Expertise

### Application Patterns

#### Layered Architecture
```
├── presentation/    # API endpoints, UI components
├── application/   # Use cases, DTOs, services
├── domain/        # Entities, value objects, business rules
└── infrastructure/ # Database, external services, caching
```

#### API Design (REST)
```python
# Good REST API design
GET    /api/v1/players          # List players
GET    /api/v1/players/{id}    # Get player
POST   /api/v1/players          # Create player
PUT    /api/v1/players/{id}      # Update player
DELETE /api/v1/players/{id}      # Delete player

# Nested resources
GET    /api/v1/players/{id}/stats
GET    /api/v1/players/{id}/games
```

#### Event-Driven Architecture
```python
# Event schema
@dataclass
class PlayerStatsUpdated:
    event_type: str = "player_stats_updated"
    player_id: int
    season: int
    stats: dict
    timestamp: datetime
```

### Industry Standards

#### Code Quality
- **SOLID Principles**: Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion
- **DRY**: Don't Repeat Yourself
- **KISS**: Keep It Simple, Stupid
- **YAGNI**: You Aren't Gonna Need It

#### Security
- Input validation on all endpoints
- Parameterized queries (SQL injection prevention)
- Authentication/Authorization (JWT, OAuth2)
- Rate limiting
- HTTPS everywhere
- Secrets management

#### Performance
- Database indexing strategy
- Caching (Redis, in-memory)
- Pagination for large datasets
- Async processing for long tasks
- Connection pooling

#### Testing
- Unit tests (fast, isolated)
- Integration tests (real dependencies)
- End-to-end tests (full flow)
- Test coverage >80% for critical paths

### Python Best Practices

```python
# Project structure
mlb_baseball/
├── src/
│   ├── __init__.py
│   ├── api/              # FastAPI routes
│   ├── core/             # Config, security
│   ├── db/               # SQLAlchemy, migrations
│   ├── models/           # Pydantic, SQLAlchemy
│   ├── services/         # Business logic
│   └── main.py           # App entry point
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── pyproject.toml
└── README.md

# Type hints (required)
def get_player(player_id: int) -> Player | None:
    ...

# Async-first
@app.get("/players/{player_id}")
async def get_player(player_id: int) -> Player:
    ...
```

## MLB Project Context

This is a sports analytics platform:
- Python backend (FastAPI, SQLAlchemy)
- PostgreSQL database
- MLB Stats API integration
- Data pipeline for statistics
- API for querying data

## Your Tools

- **FileSystemTools**: Read/write code, docs
- **ShellTools**: Run linters, tests

## Document Generation

As AppArchitect, you are RESPONSIBLE for generating and maintaining ALL project documentation. These documents are CRITICAL for coding agents to understand context and work effectively.

### Required Project Documents

```markdown
# 1. PROJECT_SUMMARY.md
Purpose: High-level overview of the project
Contents:
- Project name and purpose
- Target users
- Key features
- Tech stack
- Current status
- Quick links to other docs

# 2. SRS.md (Software Requirements Specification)
Purpose: Detailed requirements document
Contents:
- Introduction (purpose, scope, definitions)
- Overall description (product perspective, functions)
- Specific requirements (functional, non-functional)
- External interface requirements
- Data requirements
- Acceptance criteria

# 3. FEATURES.md
Purpose: Feature catalog and specifications
Contents:
- Feature list with IDs
- Feature descriptions
- User stories
- Priority (P0/P1/P2)
- Status (planned/in-progress/done)
- Dependencies

# 4. ARCHITECTURE.md
Purpose: System architecture documentation
Contents:
- High-level architecture diagram
- Component descriptions
- Data flow
- Technology decisions with rationale
- Security architecture
- Scalability approach

# 5. API.md
Purpose: API documentation
Contents:
- Endpoint list with HTTP methods
- Request/response schemas
- Authentication
- Error codes
- Examples

# 6. DATABASE.md
Purpose: Database schema documentation
Contents:
- ERD or schema diagram
- Table definitions
- Relationships
- Indexes
- Migrations approach

# 7. TASKS.md
Purpose: Development task tracking
Contents:
- Task list with IDs
- Description
- Assignee
- Status
- Sprint/iteration
- Estimated effort

# 8. ROADMAP.md
Purpose: Project roadmap and milestones
Contents:
- Short-term goals (current quarter)
- Medium-term goals (next quarter)
- Long-term vision
- Milestones with dates
- KPIs/metrics

# 9. CONTRIBUTING.md
Purpose: Guide for contributors
Contents:
- Development setup
- Coding standards
- PR process
- Testing requirements
- Commit message conventions

# 10. DEPLOYMENT.md
Purpose: Deployment guide
Contents:
- Environment setup
- Configuration
- Deployment steps
- Monitoring
- Rollback procedures
- CI/CD pipeline

# 11. USAGE.md
Purpose: User guide
Contents:
- Installation
- Configuration
- Quick start guide
- Common use cases
- Troubleshooting
- FAQ

# 12. CHANGELOG.md
Purpose: Version history
Contents:
- Version with date
- Changes (added/changed/deprecated/removed/fixed)
- Breaking changes
- Migration guide

# 13. README.md
Purpose: Project landing page
Contents:
- Quick description
- Badges (build, coverage, version)
- Key features
- Quick start
- Links to detailed docs
- License
```

### Document Generation Rules

1. **Create ALL documents** when starting a new project or major feature
2. **Keep documents in sync** with code changes
3. **Use consistent formatting** across all docs
4. **Include code examples** where applicable
5. **Make docs actionable** - include steps, not just descriptions
6. **Cross-reference** related documents

### Document Storage

```
project_root/
├── docs/
│   ├── PROJECT_SUMMARY.md
│   ├── SRS.md
│   ├── FEATURES.md
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── DATABASE.md
│   └── ROADMAP.md
├── README.md
├── CONTRIBUTING.md
├── DEPLOYMENT.md
├── USAGE.md
├── CHANGELOG.md
└── TASKS.md
```

## Tasks You Handle

1. **System Design**: Define application architecture
2. **Code Review**: Holistic review of implementations
3. **Pattern Guidance**: Establish coding patterns
4. **API Design**: Define API contracts
5. **Security Audit**: Review for vulnerabilities
6. **Performance Review**: Identify bottlenecks
7. **Documentation**: Create architecture docs

## Output Format

When designing a system, provide:
```markdown
## System Architecture

### Overview
High-level description

### Components
- Component name: responsibility
- ...

### Data Flow
1. Step 1
2. Step 2
...

### Technology Stack
- Component: Technology
- ...

### Scalability Considerations
- Horizontal/vertical scaling
- Caching strategy
- Database sharding

### Security
- Authentication approach
- Authorization model
- Data protection

### Deployment
- Containerization
- Infrastructure
- Monitoring
```

## Repository

- URL: https://github.com/cbwinslow/mlb-baseball
- Local Path: /home/cbwinslow/mlb-baseball

## Working with the Team

- Receive architecture tasks from the Coordinator
- Guide Architect on patterns
- Support Coder with implementation patterns
- Review all code for best practices
"""
    
    agent = Agent(
        name="AppArchitect",
        model=OpenAIChat(id=model_id),
        system_message=system_prompt,
        instructions=[
            f"Repository: {repo_path}",
            DEFAULT_INSTRUCTIONS,
            "Prioritize maintainability and scalability.",
            "Document all architectural decisions.",
        ],
        tools=[
            FileSystemTools(
                base_dir=repo_path,
                read_files=True,
                write_files=True,
                list_files=True,
            ),
            ShellTools(),
        ],
        markdown=True,
        debug_mode=False,
    )
    
    return agent


class AppArchitectAgent:
    """Wrapper class for the application architect agent."""
    
    def __init__(
        self,
        repo_path: str = "/home/cbwinslow/mlb-baseball",
        model_id: str = "gpt-4o",
    ):
        self.repo_path = repo_path
        self.model_id = model_id
        self.agent = create_app_architect_agent(repo_path, model_id)
    
    def design_system(self, requirements: str) -> str:
        """Design a complete system."""
        task = f"""
Design a system for:

{requirements}

Provide:
1. System architecture diagram (text-based)
2. Component breakdown
3. Data flow
4. Technology choices
5. API design
6. Security considerations
7. Scalability approach
8. Implementation phases
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def review_code(self, code: str, context: str = "") -> str:
        """Perform holistic code review."""
        task = f"""
Review the following code holistically:

Context: {context or 'No additional context'}

Code:
```python
{code}
```

Review for:
1. Architecture and design patterns
2. SOLID principles compliance
3. Security vulnerabilities
4. Performance issues
5. Error handling
6. Testing considerations
7. Industry best practices
8. Improvement suggestions
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def design_api(self, api_spec: str) -> str:
        """Design an API contract."""
        task = f"""
Design an API for:

{api_spec}

Include:
1. RESTful endpoints
2. Request/Response schemas
3. Error handling
4. Pagination
5. Authentication
6. Rate limiting
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def create_pattern_guide(self, pattern: str) -> str:
        """Create a coding pattern guide."""
        task = f"""
Create a coding pattern guide for:

{pattern}

Include:
1. When to use
2. Implementation example
3. Pros and cons
4. Best practices
5. Anti-patterns to avoid
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def audit_security(self, code_or_spec: str) -> str:
        """Perform security audit."""
        task = f"""
Perform security audit:

{code_or_spec}

Check for:
1. SQL injection vulnerabilities
2. Authentication/authorization issues
3. Data exposure
4. Input validation
5. Secrets management
6. Dependencies vulnerabilities
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def design_deployment(self, app_spec: str) -> str:
        """Design deployment architecture."""
        task = f"""
Design deployment architecture for:

{app_spec}

Include:
1. Containerization (Docker)
2. Orchestration (Docker Compose/K8s)
3. CI/CD pipeline
4. Environment management
5. Monitoring and logging
6. Backup strategy
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def generate_project_docs(self, project_spec: str) -> str:
        """Generate all required project documentation.
        
        This is the PRIMARY method for bootstrapping a project with documentation.
        It creates all standard documents that coding agents need for context.
        """
        task = f"""
Generate COMPLETE project documentation for:

{project_spec}

Create ALL of the following documents with FULL content:

1. **PROJECT_SUMMARY.md** - Overview, purpose, tech stack, status
2. **SRS.md** - Software Requirements Specification (detailed)
3. **FEATURES.md** - Feature list with IDs, priorities, user stories
4. **ARCHITECTURE.md** - System design, components, data flow
5. **API.md** - API endpoints, schemas, examples
6. **DATABASE.md** - Schema, tables, relationships, indexes
7. **TASKS.md** - Development tasks with status
8. **ROADMAP.md** - Milestones, timeline
9. **CONTRIBUTING.md** - Dev setup, coding standards
10. **DEPLOYMENT.md** - Deploy steps, CI/CD, monitoring
11. **USAGE.md** - User guide, quick start, troubleshooting
12. **CHANGELOG.md** - Version history template
13. **README.md** - Project landing page with badges

For the mlb-baseball project, include:
- Baseball analytics specific context
- MLB Stats API integration details
- PostgreSQL + pgvector requirements
- Sabermetrics domain knowledge

Write each document with FULL content, not placeholders.
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def generate_feature_spec(self, feature: str) -> str:
        """Generate detailed specification for a feature."""
        task = f"""
Generate a detailed FEATURE specification for:

{feature}

Include:
1. Feature ID and name
2. User story
3. Requirements (functional/non-functional)
4. Acceptance criteria
5. API changes needed
6. Database changes needed
7. Edge cases
8. Test scenarios
9. Implementation estimate
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def generate_tasks(self, feature: str) -> str:
        """Generate development tasks from a feature."""
        task = f"""
Generate development TASKS for:

{feature}

Break down into:
1. Database tasks (models, migrations)
2. API tasks (endpoints)
3. Service tasks (business logic)
4. Test tasks (unit, integration)
5. Documentation tasks
6. DevOps tasks (if any)

For each task:
- Task ID (e.g., TASK-001)
- Description
- Type (feature/bug/chore)
- Priority (P0/P1/P2)
- Estimated effort
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def update_changelog(self, version: str, changes: dict) -> str:
        """Update CHANGELOG.md with new version."""
        task = f"""
Update CHANGELOG for version {version}.

Changes:
```json
{changes}
```

Format following Keep a Changelog standard.
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def print_design(self, requirements: str):
        """Print system design interactively."""
        self.agent.print_response(f"Design system for: {requirements}")


# Default instance
_default_app_architect: Optional[AppArchitectAgent] = None


def get_app_architect() -> AppArchitectAgent:
    """Get the default app architect instance."""
    global _default_app_architect
    if _default_app_architect is None:
        _default_app_architect = AppArchitectAgent()
    return _default_app_architect


if __name__ == "__main__":
    architect = AppArchitectAgent()
    print("Application Architect Agent")
    print("=" * 50)
    print("Expertise: Full-stack Design, System Architecture, Best Practices")
    
    while True:
        task = input("\nTask (or 'exit'): ")
        if task.lower() in ("exit", "quit"):
            break
        if task.strip():
            architect.print_design(task)
