"""
Team Configuration for Agno MLB Agent Team

This file defines the agent team topology, routing rules, and external tool integration.
"""

from typing import Dict, Any, List

# =============================================================================
# REPOSITORY CONFIGURATION
# =============================================================================

REPO_CONFIG = {
    "url": "https://github.com/cbwinslow/mlb-baseball",
    "local_path": "/home/cbwinslow/mlb-baseball",
    "branch": "main",
    "feature_branch_prefix": "agent/",
}

# =============================================================================
# TEAM CONFIGURATION
# =============================================================================

TEAM_CONFIG = {
    "name": "mlb-agent-team",
    "description": "AI agent team for mlb-baseball project development",
    "version": "1.0.0",
}

# =============================================================================
# EXTERNAL CLI TOOLS (Cline, KiloCode, OpenCode)
# =============================================================================

EXTERNAL_TOOLS = {
    # Cline CLI - Terminal coding tool
    "cline": {
        "enabled": True,
        "command": "cline",
        "description": "AI coding assistant with MCP support",
        "mode": "interactive",  # interactive, batch, auto-approve
    },
    
    # KiloCode CLI - Terminal coding tool with TUI/Kanban
    "kilocode": {
        "enabled": True,
        "command": "kilocode",
        "description": "AI coding assistant with 500+ models via Kilo Gateway",
        "mode": "auto",  # auto, kanban, cli
        "api_key_env": "KILO_API_KEY",
    },
    
    # OpenCode CLI - Terminal coding tool
    "opencode": {
        "enabled": True,
        "command": "opencode",
        "description": "AI coding assistant (Zen models available)",
        "mode": "interactive",
    },
}

# =============================================================================
# AGENT ROUTING RULES
# =============================================================================

# All available agents
ALL_AGENTS = [
    "coordinator",
    "app_architect",
    "db_specialist",
    "stats_agent",
    "api_specialist",
    "code_reviewer",
    "performance_optimizer",
    "docs_writer",
    "coder_1",
    "coder_2",
    "coder_3",
    "coder_4",
]

# Agent routing rules by task type
ROUTING_RULES = {
    # Full feature pipeline
    "feature_request": [
        "app_architect",
        "db_specialist",
        "api_specialist",
        "coder_1",
        "code_reviewer",
        "docs_writer",
    ],
    
    # Quick feature (minimal design)
    "quick_feature": [
        "db_specialist",
        "coder_2",
        "code_reviewer",
    ],
    
    # Bug fixes
    "bug_fix": [
        "coder_3",
        "code_reviewer",
    ],
    
    # Database work
    "database": ["db_specialist"],
    "embeddings": ["db_specialist"],
    "schema": ["db_specialist"],
    "sql": ["db_specialist"],
    
    # Statistics & Analysis
    "statistics": ["stats_agent"],
    "analytics": ["stats_agent"],
    "sabermetrics": ["stats_agent"],
    "modeling": ["stats_agent"],
    
    # Architecture & Design
    "architecture": ["app_architect"],
    "design_review": ["app_architect"],
    "security": ["app_architect"],
    "docs_generation": ["app_architect", "docs_writer"],
    
    # API Design
    "api_design": ["api_specialist"],
    "rest_api": ["api_specialist"],
    "graphql": ["api_specialist"],
    
    # Refactoring
    "refactoring": ["app_architect", "coder_1", "code_reviewer"],
    
    # Documentation
    "documentation": ["docs_writer"],
    "readme": ["docs_writer"],
    "srs": ["docs_writer"],
    
    # Testing
    "testing": ["code_reviewer"],
    "test_coverage": ["code_reviewer"],
    
    # Performance
    "performance": ["performance_optimizer"],
    "optimization": ["performance_optimizer"],
    
    # Code review (democratic approach - multiple eyes)
    "code_review": ["code_reviewer", "app_architect"],
    "peer_review": ["code_reviewer", "coder_1", "coder_2"],
    
    # Analysis
    "analysis": ["app_architect", "coder_1"],
    
    # Default
    "default": ["coordinator"],
}

# =============================================================================
# TASK DEFINITIONS
# =============================================================================

TASK_TYPES = {
    "feature": {
        "description": "New feature implementation (full pipeline)",
        "agents": ["app_architect", "db_specialist", "api_specialist", "coder_1", "code_reviewer", "docs_writer"],
        "requires_design": True,
    },
    "quick_feature": {
        "description": "Quick feature (minimal design)",
        "agents": ["db_specialist", "coder_2", "code_reviewer"],
        "requires_design": False,
    },
    "bug": {
        "description": "Bug fix",
        "agents": ["coder_3", "code_reviewer"],
        "requires_design": False,
    },
    "improvement": {
        "description": "Code improvement/refactoring",
        "agents": ["app_architect", "coder_1", "code_reviewer"],
        "requires_design": True,
    },
    "database": {
        "description": "Database schema or query work",
        "agents": ["db_specialist"],
        "requires_design": True,
    },
    "embeddings": {
        "description": "Vector embeddings or semantic search",
        "agents": ["db_specialist"],
        "requires_design": True,
    },
    "statistics": {
        "description": "Statistical analysis or modeling",
        "agents": ["stats_agent"],
        "requires_design": False,
    },
    "architecture": {
        "description": "System architecture or design review",
        "agents": ["app_architect"],
        "requires_design": True,
    },
    "api_design": {
        "description": "API design and specification",
        "agents": ["api_specialist"],
        "requires_design": True,
    },
    "docs": {
        "description": "Documentation update",
        "agents": ["docs_writer"],
        "requires_design": False,
    },
    "code_review": {
        "description": "Code review (democratic - multiple agents)",
        "agents": ["code_reviewer", "app_architect", "coder_1"],
        "requires_design": False,
    },
    "performance": {
        "description": "Performance optimization",
        "agents": ["performance_optimizer"],
        "requires_design": False,
    },
}

# =============================================================================
# SHARED CONTEXT KEYS
# =============================================================================

SHARED_CONTEXT_KEYS = [
    "repo_url",
    "repo_path",
    "current_branch",
    "open_issues",
    "in_progress_tasks",
    "completed_tasks",
    "last_task_result",
    "srs_document",
    "feature_specs",
    "api_schemas",
]

# =============================================================================
# DEFAULT AGENT INSTRUCTIONS
# =============================================================================

DEFAULT_INSTRUCTIONS = """
You are part of the MLB Agent Team working on the mlb-baseball project.
- Repository: https://github.com/cbwinslow/mlb-baseball
- Always follow the project's coding standards and conventions
- Use type hints and docstrings in all Python code
- Write tests for all new functionality
- Update documentation when making changes
- Communicate clearly with the team coordinator
- Work collaboratively with other agents (democratic approach)
"""

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_task_route(task_type: str) -> List[str]:
    """Get the agent routing for a task type."""
    return ROUTING_RULES.get(task_type, ROUTING_RULES["default"])

def get_available_agents() -> List[str]:
    """Get list of all available agents."""
    return ALL_AGENTS.copy()

def is_external_tool_enabled(tool_name: str) -> bool:
    """Check if an external CLI tool is enabled."""
    return EXTERNAL_TOOLS.get(tool_name, {}).get("enabled", False)
