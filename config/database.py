"""
Database Configuration for Agno MLB Agent Team

Configures PostgreSQL + pgvector for:
- Agno session/memory persistence
- MLB data storage
- Vector embeddings for RAG
"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Database configuration for Agno."""
    host: str
    port: int
    database: str
    user: str
    password: str
    
    @property
    def url(self) -> str:
        """Get connection URL."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    @property
    def async_url(self) -> str:
        """Get async connection URL."""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


# =============================================================================
# DATABASE INSTANCES
# =============================================================================

# Agno's own database (sessions, memories, traces)
AGNO_DATABASE = DatabaseConfig(
    host=os.getenv("AGNO_DB_HOST", "localhost"),
    port=int(os.getenv("AGNO_DB_PORT", "5432")),
    database=os.getenv("AGNO_DB_NAME", "agno"),
    user=os.getenv("AGNO_DB_USER", "cbwinslow"),
    password=os.getenv("AGNO_DB_PASSWORD", ""),
)

# MLB data database
MLB_DATABASE = DatabaseConfig(
    host=os.getenv("MLB_DB_HOST", "localhost"),
    port=int(os.getenv("MLB_DB_PORT", "5432")),
    database=os.getenv("MLB_DB_NAME", "mlb_baseball"),
    user=os.getenv("MLB_DB_USER", "cbwinslow"),
    password=os.getenv("MLB_DB_PASSWORD", ""),
)

# CBW RAG database (existing pgvector setup)
RAG_DATABASE = DatabaseConfig(
    host=os.getenv("RAG_DB_HOST", "localhost"),
    port=int(os.getenv("RAG_DB_PORT", "5432")),
    database=os.getenv("RAG_DB_NAME", "cbw_rag"),
    user=os.getenv("RAG_DB_USER", "cbwinslow"),
    password=os.getenv("RAG_DB_PASSWORD", ""),
)


# =============================================================================
# VECTOR DB CONFIGURATION
# =============================================================================

# pgvector configuration for embeddings
VECTOR_DB_CONFIG = {
    "provider": "pgvector",
    "dimension": 768,  # nomic-embed-text embedding size
    "table_name": "agent_knowledge",
    "index_type": "HNSW",  # or "IVFFlat"
    "metric": "COSINE",  # or "L2", "IP"
}


# =============================================================================
# TABLE SCHEMAS
# =============================================================================

# Schema for MLB player stats
MLB_STATS_SCHEMA = """
CREATE TABLE IF NOT EXISTS mlb_player_stats (
    id SERIAL PRIMARY KEY,
    player_id INTEGER UNIQUE NOT NULL,
    player_name VARCHAR(100) NOT NULL,
    season INTEGER NOT NULL,
    team VARCHAR(10),
    -- Batting stats
    games INTEGER DEFAULT 0,
    at_bats INTEGER DEFAULT 0,
    hits INTEGER DEFAULT 0,
    doubles INTEGER DEFAULT 0,
    triples INTEGER DEFAULT 0,
    home_runs INTEGER DEFAULT 0,
    runs_batted_in INTEGER DEFAULT 0,
    walks INTEGER DEFAULT 0,
    strikeouts INTEGER DEFAULT 0,
    batting_average DECIMAL(4,3),
    on_base_percentage DECIMAL(4,3),
    slugging_percentage DECIMAL(4,3),
    ops DECIMAL(4,3),
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_mlb_stats_player ON mlb_player_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_mlb_stats_season ON mlb_player_stats(season);
"""

# Schema for agent knowledge base (RAG)
KNOWLEDGE_SCHEMA = """
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS agent_knowledge (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(768),
    metadata JSONB,
    source VARCHAR(100),
    agent_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_knowledge_embedding ON agent_knowledge 
    USING HNSW (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS idx_knowledge_source ON agent_knowledge(source);
"""

# =============================================================================
# DATABASE HELPERS
# =============================================================================

def get_agno_db_url() -> str:
    """Get Agno database URL."""
    return AGNO_DATABASE.url


def get_mlb_db_url() -> str:
    """Get MLB database URL."""
    return MLB_DATABASE.url


def get_rag_db_url() -> str:
    """Get RAG database URL."""
    return RAG_DATABASE.url


def test_connection(config: DatabaseConfig) -> bool:
    """Test database connection."""
    try:
        import psycopg2
        conn = psycopg2.connect(config.url)
        conn.close()
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False


# =============================================================================
# AGNO INTEGRATION
# =============================================================================

def get_agno_persistence_config() -> dict:
    """
    Get Agno persistence configuration for database storage.
    """
    return {
        "session_db_url": AGNO_DATABASE.url,
        "memory_db_url": AGNO_DATABASE.url,
        "traces_db_url": AGNO_DATABASE.url,
    }


def get_vector_db_config() -> dict:
    """
    Get vector database configuration for embeddings.
    """
    return {
        "provider": "pgvector",
        "table_name": VECTOR_DB_CONFIG["table_name"],
        "dimension": VECTOR_DB_CONFIG["dimension"],
        "db_url": RAG_DATABASE.url,
    }
