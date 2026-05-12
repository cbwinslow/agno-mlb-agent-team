"""
FastAPI Server Configuration

Production API server for the MLB agent team.
"""

from typing import Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agno.os import AgentOS

from config import REPO_CONFIG, TEAM_CONFIG
from runtime.agentos import get_runtime


# Request/Response models
class TaskRequest(BaseModel):
    """Request model for task execution."""
    task: str
    task_type: str = "feature"  # feature, bug, improvement, docs
    context: Optional[dict] = None


class TaskResponse(BaseModel):
    """Response model for task execution."""
    task_id: str
    status: str
    result: str
    agents_involved: list[str]


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    team_name: str
    repository: str
    version: str


def create_app(runtime: Optional[AgentOS] = None) -> FastAPI:
    """
    Create the FastAPI application.
    
    Args:
        runtime: Optional pre-configured AgentOS runtime
        
    Returns:
        Configured FastAPI app
    """
    # Get or create runtime
    agent_os = runtime or get_runtime()
    
    # Create FastAPI app
    app = FastAPI(
        title="MLB Agent Team API",
        description="Multi-agent AI team for MLB Baseball Analytics project",
        version="1.0.0",
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Store runtime reference
    app.state.runtime = agent_os
    app.state.team_config = TEAM_CONFIG
    app.state.repo_config = REPO_CONFIG
    
    # Health check endpoint
    @app.get("/health", response_model=HealthResponse)
    async def health():
        """Check API health."""
        return HealthResponse(
            status="healthy",
            team_name=TEAM_CONFIG["name"],
            repository=REPO_CONFIG["url"],
            version=TEAM_CONFIG["version"],
        )
    
    # Task execution endpoints
    @app.post("/tasks", response_model=TaskResponse)
    async def execute_task(request: TaskRequest):
        """Execute a task through the agent team."""
        try:
            # Route to appropriate agents based on task type
            result = await execute_with_team(
                agent_os,
                request.task,
                request.task_type,
                request.context,
            )
            
            return TaskResponse(
                task_id=result.get("task_id", "unknown"),
                status="completed",
                result=result.get("output", ""),
                agents_involved=result.get("agents", []),
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # Agent-specific endpoints
    @app.get("/agents")
    async def list_agents():
        """List all available agents."""
        return {
            "agents": [
                {
                    "name": agent.name,
                    "role": get_agent_role(agent.name),
                }
                for agent in agent_os.agents
            ]
        }
    
    @app.post("/agents/{agent_name}/task")
    async def agent_task(agent_name: str, task: str):
        """Execute a task with a specific agent."""
        agent = get_agent_by_name(agent_os, agent_name)
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
        
        result = agent.run(task)
        return {
            "agent": agent_name,
            "result": result.content if hasattr(result, 'content') else str(result),
        }
    
    # Repository endpoints
    @app.get("/repo/info")
    async def repo_info():
        """Get repository information."""
        return {
            "url": REPO_CONFIG["url"],
            "local_path": REPO_CONFIG["local_path"],
            "branch": REPO_CONFIG["branch"],
        }
    
    return app


async def execute_with_team(
    agent_os: AgentOS,
    task: str,
    task_type: str,
    context: Optional[dict],
) -> dict:
    """Execute a task with the agent team."""
    # This would integrate with AgentOS's team execution
    # For now, return a placeholder
    return {
        "task_id": "task_001",
        "output": f"Task '{task}' executed as type '{task_type}'",
        "agents": get_agents_for_task_type(task_type),
    }


def get_agent_role(agent_name: str) -> str:
    """Get the role description for an agent."""
    roles = {
        "Coordinator": "Team leader, task orchestration",
        "Architect": "Technical design, data models",
        "Coder": "Implementation, bug fixes",
        "Tester": "Testing, validation",
        "DocsWriter": "Documentation, changelog",
    }
    return roles.get(agent_name, "Unknown role")


def get_agent_by_name(agent_os: AgentOS, name: str):
    """Get an agent by name from the runtime."""
    for agent in agent_os.agents:
        if agent.name.lower() == name.lower():
            return agent
    return None


def get_agents_for_task_type(task_type: str) -> list[str]:
    """Get the agents needed for a task type."""
    routing = {
        "feature": ["architect", "coder", "tester", "docs_writer"],
        "bug": ["coder", "tester"],
        "improvement": ["architect", "coder", "tester"],
        "docs": ["docs_writer"],
        "testing": ["tester"],
        "analysis": ["architect", "coder"],
    }
    return routing.get(task_type, ["coordinator"])


# Application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
