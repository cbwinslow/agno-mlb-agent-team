"""
AgentOS Runtime Configuration

This module sets up the production runtime for the MLB agent team.
"""

from pathlib import Path
from typing import Optional, List

from agno.os import AgentOS
from agno.db.sqlite import SqliteDb
from agno.db.postgres import PostgresDb

from config import REPO_CONFIG, TEAM_CONFIG
from agents import (
    create_architect_agent,
    create_coder_agent,
    create_tester_agent,
    create_docs_writer_agent,
)


def create_agentos_runtime(
    db_url: Optional[str] = None,
    db_file: str = "./data/agno.db",
    tracing: bool = True,
) -> AgentOS:
    """
    Create the AgentOS runtime with all agents configured.
    
    Args:
        db_url: PostgreSQL connection URL (optional, uses SQLite if not provided)
        db_file: SQLite database file path
        tracing: Enable OpenTelemetry tracing
        
    Returns:
        Configured AgentOS instance
    """
    # Create agents
    agents = [
        create_architect_agent(repo_path=REPO_CONFIG["local_path"]),
        create_coder_agent(repo_path=REPO_CONFIG["local_path"]),
        create_tester_agent(repo_path=REPO_CONFIG["local_path"]),
        create_docs_writer_agent(repo_path=REPO_CONFIG["local_path"]),
    ]
    
    # Configure database
    if db_url:
        db = PostgresDb(
            connection_string=db_url,
            table_name="agent_sessions",
        )
    else:
        db = SqliteDb(
            table_name="agent_sessions",
            db_file=db_file,
        )
    
    # Create AgentOS instance
    agent_os = AgentOS(
        name=TEAM_CONFIG["name"],
        agents=agents,
        db=db,
        tracing=tracing,
        enable_session_history=True,
        enable_agentic_context=True,
    )
    
    return agent_os


def create_workflow_runtime(
    db_file: str = "./data/workflows.db",
) -> AgentOS:
    """
    Create a runtime optimized for workflow execution.
    """
    from agents.coordinator import create_coordinator_team
    
    team = create_coordinator_team()
    
    return AgentOS(
        name=f"{TEAM_CONFIG['name']}-workflow",
        team=team,
        db=SqliteDb(table_name="workflows", db_file=db_file),
        tracing=True,
        enable_session_history=True,
    )


# Default runtime instance
_default_runtime: Optional[AgentOS] = None


def get_runtime(
    db_url: Optional[str] = None,
    db_file: str = "./data/agno.db",
) -> AgentOS:
    """Get the default runtime instance."""
    global _default_runtime
    if _default_runtime is None:
        _default_runtime = create_agentos_runtime(db_url, db_file)
    return _default_runtime


def get_workflow_runtime(db_file: str = "./data/workflows.db") -> AgentOS:
    """Get the workflow runtime instance."""
    return create_workflow_runtime(db_file)


if __name__ == "__main__":
    # Test runtime creation
    runtime = create_agentos_runtime()
    print(f"Created AgentOS runtime: {runtime.name}")
    print(f"Agents: {[a.name for a in runtime.agents]}")
