"""
AgentOS Runtime Configuration

Configures the full Agno AgentOS runtime with:
- Agent persistence (PostgreSQL)
- Vector embeddings (pgvector)
- Memory management
- MCP servers
- Tracing
"""

import os
from typing import List, Optional
from agno.agent import Agent
from agno.os import AgentOS
from agno.team import Team
from agno.db.postgres import PostgresDb
from agno.vector_db.pgvector import PgVector
from agno.knowledge import Knowledge

# Import configuration
from config import (
    AGENT_MODELS,
    TEAM_CONFIG,
    REPO_CONFIG,
    AGNO_DATABASE,
    RAG_DATABASE,
    VECTOR_DB_CONFIG,
    get_agno_persistence_config,
    get_vector_db_config,
    get_all_tools,
)


# =============================================================================
# DATABASE SETUP
# =============================================================================

def get_postgres_db():
    """Get Agno PostgreSQL database connection."""
    return PostgresDb(
        db_url=AGNO_DATABASE.url,
        session_table_name="agent_sessions",
    )


def get_vector_db():
    """Get pgvector database for embeddings."""
    return PgVector(
        table_name=VECTOR_DB_CONFIG["table_name"],
        dimension=VECTOR_DB_CONFIG["dimension"],
        db_url=RAG_DATABASE.url,
    )


# =============================================================================
# KNOWLEDGE BASE SETUP
# =============================================================================

def get_agent_knowledge():
    """Get knowledge base for RAG."""
    return Knowledge(
        vector_db=get_vector_db(),
        num_documents=10,
    )


# =============================================================================
# AGENT FACTORY
# =============================================================================

def create_agent(
    name: str,
    role: str,
    instructions: str,
    tools: Optional[List] = None,
    knowledge: bool = True,
    memory: bool = True,
    enable_agentic_memory: bool = True,
) -> Agent:
    """
    Create a configured agent with all infrastructure.
    
    Args:
        name: Agent name
        role: Agent role description
        instructions: System prompt/instructions
        tools: List of tools to enable
        knowledge: Enable RAG knowledge base
        memory: Enable conversation history
        enable_agentic_memory: Enable automatic memory
    """
    model = AGENT_MODELS.get(name)
    
    agent_config = {
        "name": name,
        "role": role,
        "model": model,
        "instructions": instructions,
        "add_history_to_messages": memory,
        "num_history_messages": 5,
        "enable_agentic_memory": enable_agentic_memory,
    }
    
    # Add tools
    if tools:
        agent_config["tools"] = tools
    
    # Add knowledge base
    if knowledge:
        agent_config["knowledge"] = get_agent_knowledge()
    
    return Agent(**agent_config)


# =============================================================================
# TEAM SETUP
# =============================================================================

def create_team(agents: List[Agent]) -> Team:
    """
    Create a team of agents with shared context.
    """
    return Team(
        name=TEAM_CONFIG["name"],
        agents=agents,
        mode="coordinate",
        enable_agentic_memory=True,
        share_knowledge=True,
    )


# =============================================================================
# AGENTOS RUNTIME
# =============================================================================

def create_agentos_runtime(
    agents: List[Agent],
    app_name: str = "mlb-agent-team",
) -> AgentOS:
    """
    Create the full AgentOS runtime.
    
    This provides:
    - REST API endpoints
    - WebSocket support
    - Session persistence
    - Memory management
    - Tracing
    """
    return AgentOS(
        name=app_name,
        agents=agents,
        db=get_postgres_db(),
        user_id="cbwinslow",
        # Enable features
        enable_agentic_memory=True,
        enable_session_persistence=True,
        enable_trace_storage=True,
        # Knowledge base
        knowledge_base=get_agent_knowledge(),
        # Storage paths
        storage_path="./data",
    )


# =============================================================================
# RUNTIME CONFIGURATION
# =============================================================================

RUNTIME_CONFIG = {
    # Server settings
    "host": os.getenv("AGNO_HOST", "0.0.0.0"),
    "port": int(os.getenv("AGNO_PORT", "8000")),
    
    # Database
    "database_url": AGNO_DATABASE.url,
    "vector_db_url": RAG_DATABASE.url,
    
    # Agent defaults
    "default_tools": get_all_tools(),
    "enable_memory": True,
    "enable_knowledge": True,
    
    # Tracing
    "enable_tracing": os.getenv("TRACING_ENABLED", "true").lower() == "true",
    
    # MCP
    "mcp_servers_enabled": os.getenv("ENABLE_MCP_SERVERS", "true").lower() == "true",
}


def get_runtime_config() -> dict:
    """Get runtime configuration."""
    return RUNTIME_CONFIG.copy()
