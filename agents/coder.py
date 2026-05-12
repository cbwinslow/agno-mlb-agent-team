"""
Coder Agent - Feature Implementation

This agent implements features, fixes bugs, and writes production code.
"""

from typing import Optional, List
from pathlib import Path

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.file_system import FileSystemTools
from agno.tools.shell import ShellTools

from config import DEFAULT_INSTRUCTIONS
from prompts.coder import CODER_PROMPT


def create_coder_agent(
    repo_path: str = "/home/cbwinslow/mlb-baseball",
    model_id: str = "gpt-4o",
) -> Agent:
    """Create a coder agent for implementation."""
    
    # Load the system prompt
    prompt_path = Path(__file__).parent.parent / "prompts" / "coder.md"
    if prompt_path.exists():
        system_prompt = prompt_path.read_text()
    else:
        system_prompt = CODER_PROMPT
    
    agent = Agent(
        name="Coder",
        model=OpenAIChat(id=model_id),
        system_message=system_prompt,
        instructions=[
            f"Repository: {repo_path}",
            DEFAULT_INSTRUCTIONS,
        ],
        tools=[
            FileSystemTools(
                base_dir=repo_path,
                read_files=True,
                write_files=True,
                list_files=True,
                search_files=True,
            ),
            ShellTools(),
        ],
        markdown=True,
        debug_mode=False,
    )
    
    return agent


class CoderAgent:
    """Wrapper class for the coder agent."""
    
    def __init__(
        self,
        repo_path: str = "/home/cbwinslow/mlb-baseball",
        model_id: str = "gpt-4o",
    ):
        self.repo_path = repo_path
        self.model_id = model_id
        self.agent = create_coder_agent(repo_path, model_id)
    
    def implement_feature(self, design: str, file_path: Optional[str] = None) -> str:
        """Implement a feature based on a design specification."""
        task = f"""
Implement the following feature design:

{design}

{"Target file: " + file_path if file_path else ""}

Please:
1. First explore the existing codebase to understand patterns
2. Implement the code following project conventions
3. Add type hints and docstrings
4. Write unit tests for the new functionality
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def fix_bug(self, bug_description: str, file_path: Optional[str] = None) -> str:
        """Fix a bug based on description."""
        task = f"""
Fix the following bug:

{bug_description}

{"Location: " + file_path if file_path else ""}

Please:
1. Locate the relevant code
2. Understand the issue
3. Write a test that reproduces the bug (should fail)
4. Fix the bug
5. Verify the fix works
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def create_endpoint(
        self,
        endpoint_spec: str,
        route_file: str = "routes/api.py",
    ) -> str:
        """Create an API endpoint."""
        task = f"""
Create an API endpoint based on this specification:

{endpoint_spec}

Target file: {route_file}

Follow the existing patterns in the codebase for:
- Route definitions
- Request/Response models
- Error handling
- Type hints
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def create_model(self, model_spec: str, model_file: str = "models/") -> str:
        """Create a database model."""
        task = f"""
Create a database model based on this specification:

{model_spec}

Target directory: {model_file}

Follow existing SQLAlchemy patterns in the project.
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def explore_and_modify(self, instruction: str) -> str:
        """General exploration and modification."""
        response = self.agent.run(f"""
{instruction}

Repository path: {self.repo_path}
""")
        return response.content if hasattr(response, 'content') else str(response)
    
    def print_implementation(self, design: str):
        """Print implementation interactively."""
        self.agent.print_response(f"Implement: {design}")


# Default instance
_default_coder: Optional[CoderAgent] = None


def get_coder() -> CoderAgent:
    """Get the default coder instance."""
    global _default_coder
    if _default_coder is None:
        _default_coder = CoderAgent()
    return _default_coder


if __name__ == "__main__":
    coder = CoderAgent()
    print("MLB Coder Agent")
    print("=" * 50)
    
    while True:
        task = input("\nTask (or 'exit'): ")
        if task.lower() in ("exit", "quit"):
            break
        if task.strip():
            coder.print_implementation(task)
