"""
Coordinator Agent - Team Leader for MLB Agent Team

This agent orchestrates the work of the specialist agents.
"""

from typing import Optional
from pathlib import Path

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.db.sqlite import SqliteDb

from config import get_model, REPO_CONFIG, DEFAULT_INSTRUCTIONS
from prompts.coordinator import COORDINATOR_PROMPT


class CoordinatorAgent:
    """Team coordinator that manages the agent workflow."""
    
    def __init__(
        self,
        repo_path: str = REPO_CONFIG["local_path"],
        model_id: str = "gpt-4o",
        storage_path: str = "./data/coordinator.db",
    ):
        self.repo_path = Path(repo_path)
        self.model_id = model_id
        
        # Load the system prompt
        prompt_path = Path(__file__).parent.parent / "prompts" / "coordinator.md"
        if prompt_path.exists():
            self.system_prompt = prompt_path.read_text()
        else:
            self.system_prompt = COORDINATOR_PROMPT
        
        # Create the agent
        self.agent = Agent(
            name="Coordinator",
            model=OpenAIChat(id=self.model_id),
            system_message=self.system_prompt,
            instructions=[
                f"You are coordinating work on: {REPO_CONFIG['url']}",
                f"Repository path: {repo_path}",
                DEFAULT_INSTRUCTIONS,
            ],
            storage=SqliteDb(table_name="coordinator", db_file=storage_path),
            markdown=True,
            debug_mode=False,
        )
    
    def run(self, task: str, context: Optional[dict] = None) -> str:
        """Execute a task through the coordinator."""
        full_task = f"""
Repository: {REPO_CONFIG['url']}
Local Path: {self.repo_path}

Task: {task}

Context: {context or 'No additional context'}

Please analyze this task and coordinate with your team to complete it.
"""
        response = self.agent.run(full_task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def print_response(self, task: str, context: Optional[dict] = None):
        """Print the coordinator's response interactively."""
        full_task = f"""
Repository: {REPO_CONFIG['url']}
Local Path: {self.repo_path}

Task: {task}

Context: {context or 'No additional context'}
"""
        self.agent.print_response(full_task)


def create_coordinator_team() -> Team:
    """Create a team with all agents for coordinated work."""
    from agents.architect import create_architect_agent
    from agents.coder import create_coder_agent
    from agents.tester import create_tester_agent
    from agents.docs_writer import create_docs_writer_agent
    from agents.db_specialist import create_db_specialist_agent
    from agents.stats_agent import create_stats_agent
    from agents.app_architect import create_app_architect_agent
    
    # Create individual agents
    architect = create_architect_agent()
    coder = create_coder_agent()
    tester = create_tester_agent()
    docs_writer = create_docs_writer_agent()
    db_specialist = create_db_specialist_agent()
    stats_agent = create_stats_agent()
    app_architect = create_app_architect_agent()
    
    # Create the team
    team = Team(
        name="mlb-agent-team",
        mode="coordinate",  # Coordinator assigns tasks to agents
        agents=[
            architect, coder, tester, docs_writer,
            db_specialist, stats_agent, app_architect
        ],
        storage=SqliteDb(table_name="team", db_file="./data/team.db"),
        enable_session_history=True,
        share_member_info=True,
        system_message=f"""
You are the Team Coordinator for the MLB Baseball Analytics project.

Your team includes:
- Architect: Designs data models and system architecture
- Coder: Implements features and fixes bugs
- Tester: Writes tests and validates code
- DocsWriter: Maintains documentation
- DBSpecialist: PostgreSQL, pgvector, database design
- StatsAgent: Sabermetrics, statistical modeling, data analysis
- AppArchitect: Full-stack design, industry best practices, system architecture

Workflow:
1. Receive a task from the user
2. Determine which agents are needed
3. Assign tasks with clear instructions
4. Track progress and dependencies
5. Report results back to the user

Task Routing:
- Feature request → AppArchitect (design) → DBSpecialist (schema) → Coder (implement) → Tester (verify) → DocsWriter (document)
- Database work → DBSpecialist
- Statistics/analytics → StatsAgent
- Architecture/review → AppArchitect
- Bug fix → Coder → Tester
- Documentation → DocsWriter

Repository: {REPO_CONFIG['url']}
Local Path: {REPO_CONFIG['local_path']}
""",
    )
    
    return team


# Default instance for convenience
_default_coordinator: Optional[CoordinatorAgent] = None


def get_coordinator() -> CoordinatorAgent:
    """Get the default coordinator instance."""
    global _default_coordinator
    if _default_coordinator is None:
        _default_coordinator = CoordinatorAgent()
    return _default_coordinator


if __name__ == "__main__":
    # Interactive mode
    coordinator = CoordinatorAgent()
    print("MLB Agent Team Coordinator")
    print("=" * 50)
    print(f"Repository: {REPO_CONFIG['url']}")
    print("Type 'exit' to quit\n")
    
    while True:
        task = input("\nTask: ")
        if task.lower() in ("exit", "quit"):
            break
        if task.strip():
            coordinator.print_response(task)
