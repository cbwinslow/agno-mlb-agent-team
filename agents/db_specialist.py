"""
Database Specialist Agent - PostgreSQL, pgvector, Schema Design

This agent handles all database-related tasks including schema design,
query optimization, embeddings, and vector search.
"""

from typing import Optional, List, Dict
from pathlib import Path

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.file_system import FileSystemTools
from agno.tools.shell import ShellTools

from config import DEFAULT_INSTRUCTIONS


def create_db_specialist_agent(
    repo_path: str = "/home/cbwinslow/mlb-baseball",
    model_id: str = "gpt-4o",
) -> Agent:
    """Create a database specialist agent."""
    
    system_prompt = """You are the **Database Specialist** for the MLB Agent Team. You are the authority on PostgreSQL, pgvector, and data persistence for the mlb-baseball project.

## Your Role

You ensure optimal database design and data management by:
1. Designing PostgreSQL schemas and tables
2. Implementing pgvector embeddings for semantic search
3. Writing optimized SQL queries
4. Creating database migrations
5. Ensuring data integrity and consistency
6. Optimizing query performance
7. Setting up indexes and partitions

## PostgreSQL Expertise

### Schema Design
```sql
-- Example: Player statistics table
CREATE TABLE player_stats (
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(id),
    stat_type VARCHAR(50) NOT NULL,
    value DECIMAL(10,3),
    season INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index for common queries
CREATE INDEX idx_player_stats_season ON player_stats(season);
CREATE INDEX idx_player_stats_player ON player_stats(player_id);
```

### pgvector Embeddings
```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create embeddings table
CREATE TABLE player_embeddings (
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(id),
    embedding vector(768),  -- nomic-embed-text dimensions
    content TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Semantic search query
SELECT p.name, p.id,
    1 - (pe.embedding <=> $1::vector) AS similarity
FROM player_embeddings pe
JOIN players p ON p.id = pe.player_id
WHERE pe.embedding <=> $1::vector < 0.5
ORDER BY pe.embedding <=> $1::vector
LIMIT 10;
```

### Query Optimization
- Use EXPLAIN ANALYZE to understand query plans
- Create appropriate indexes
- Use partitions for time-series data
- Optimize JOINs and subqueries
- Use connection pooling (pgbouncer)

## MLB Project Context

This project uses:
- PostgreSQL 16 with pgvector 0.8
- SQLAlchemy ORM for Python
- Existing tables: players, games, box_scores, stats
- Data from MLB Stats API and FanGraphs

## Your Tools

- **FileSystemTools**: Read/write schema files, migration scripts
- **ShellTools**: Run psql commands, check database status

## Tasks You Handle

1. **Schema Design**: Create new tables, modify existing
2. **Migrations**: Generate Alembic migration files
3. **Embedding Setup**: Configure pgvector for semantic search
4. **Query Optimization**: Improve slow queries
5. **Data Modeling**: Translate requirements to DB schema
6. **Documentation**: Document schema and relationships

## Output Format

When designing a schema, provide:
```markdown
## Database Design

### Tables
- Table name, columns, types, constraints
- Indexes
- Relationships

### Migrations
- Alembic migration steps

### Query Examples
- Common queries with examples

### Performance Considerations
- Indexes needed
- Partitioning strategy
```

## Repository

- URL: https://github.com/cbwinslow/mlb-baseball
- Local Path: /home/cbwinslow/mlb-baseball

## Working with the Team

- Receive DB tasks from the Coordinator
- Work with Architect on data models
- Provide query optimization to Coder
- Ensure Tester understands DB constraints
"""
    
    agent = Agent(
        name="DBSpecialist",
        model=OpenAIChat(id=model_id),
        system_message=system_prompt,
        instructions=[
            f"Repository: {repo_path}",
            DEFAULT_INSTRUCTIONS,
            "Always use parameterized queries to prevent SQL injection.",
            "Document all schema changes.",
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


class DBSpecialistAgent:
    """Wrapper class for the database specialist agent."""
    
    def __init__(
        self,
        repo_path: str = "/home/cbwinslow/mlb-baseball",
        model_id: str = "gpt-4o",
    ):
        self.repo_path = repo_path
        self.model_id = model_id
        self.agent = create_db_specialist_agent(repo_path, model_id)
    
    def design_schema(self, entity_spec: str) -> str:
        """Design database schema for an entity."""
        task = f"""
Design a PostgreSQL schema for the following entity:

{entity_spec}

Please provide:
1. Table definition(s) with columns and types
2. Indexes for common queries
3. Constraints and relationships
4. Alembic migration file content
5. SQLAlchemy model code
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def setup_embeddings(self, use_case: str) -> str:
        """Set up pgvector for semantic search."""
        task = f"""
Set up pgvector embeddings for: {use_case}

Consider:
1. Embedding model (nomic-embed-text, 768 dimensions)
2. Table structure for storing vectors
3. Index type (IVFFlat or HNSW)
4. Query approach for similarity search
5. Integration with existing schema
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def optimize_query(self, query: str, context: str = "") -> str:
        """Optimize a slow SQL query."""
        task = f"""
Optimize the following SQL query:

Query:
```sql
{query}
```

Context: {context or 'No additional context'}

Please:
1. Analyze the query plan
2. Identify bottlenecks
3. Suggest indexes
4. Rewrite for better performance
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def create_migration(self, changes: str) -> str:
        """Generate an Alembic migration."""
        task = f"""
Generate an Alembic migration for:

{changes}

Follow the project's migration patterns.
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def analyze_schema(self, focus_area: str = "all") -> str:
        """Analyze the current database schema."""
        task = f"""
Analyze the database schema in the mlb-baseball project.

Focus area: {focus_area}

Provide:
1. Current table structure
2. Relationships
3. Indexes
4. Potential improvements
5. Missing indexes or optimizations
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def print_schema_design(self, entity: str):
        """Print schema design interactively."""
        self.agent.print_response(f"Design schema for: {entity}")


# Default instance
_default_db_specialist: Optional[DBSpecialistAgent] = None


def get_db_specialist() -> DBSpecialistAgent:
    """Get the default DB specialist instance."""
    global _default_db_specialist
    if _default_db_specialist is None:
        _default_db_specialist = DBSpecialistAgent()
    return _default_db_specialist


if __name__ == "__main__":
    specialist = DBSpecialistAgent()
    print("Database Specialist Agent")
    print("=" * 50)
    print("Expertise: PostgreSQL, pgvector, Schema Design")
    
    while True:
        task = input("\nTask (or 'exit'): ")
        if task.lower() in ("exit", "quit"):
            break
        if task.strip():
            specialist.print_schema_design(task)
