"""
Architect Agent - Technical Design Authority

This agent designs data models, API schemas, and system architecture.
"""

from typing import Optional
from pathlib import Path

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.file_system import FileSystemTools

from config import DEFAULT_INSTRUCTIONS
from prompts.architect import ARCHITECT_PROMPT


def create_architect_agent(
    repo_path: str = "/home/cbwinslow/mlb-baseball",
    model_id: str = "gpt-4o",
) -> Agent:
    """Create an architect agent for technical design."""
    
    # Load the system prompt
    prompt_path = Path(__file__).parent.parent / "prompts" / "architect.md"
    if prompt_path.exists():
        system_prompt = prompt_path.read_text()
    else:
        system_prompt = ARCHITECT_PROMPT
    
    agent = Agent(
        name="Architect",
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
            ),
        ],
        markdown=True,
        debug_mode=False,
    )
    
    return agent


class ArchitectAgent:
    """Wrapper class for the architect agent."""
    
    def __init__(
        self,
        repo_path: str = "/home/cbwinslow/mlb-baseball",
        model_id: str = "gpt-4o",
    ):
        self.repo_path = repo_path
        self.model_id = model_id
        self.agent = create_architect_agent(repo_path, model_id)
    
    def design_feature(self, feature_request: str) -> str:
        """Create a design specification for a feature."""
        task = f"""
Analyze the mlb-baseball codebase and create a technical design for:

{feature_request}

Please provide:
1. Overview of the feature
2. Data model design (if applicable)
3. API endpoint specifications
4. Implementation steps
5. Technical considerations
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def analyze_codebase(self, focus_area: Optional[str] = None) -> str:
        """Analyze the existing codebase structure."""
        task = f"""
Analyze the mlb-baseball codebase structure.

{"Focus area: " + focus_area if focus_area else "Provide a general overview."}

Include:
1. Current architecture
2. Key modules and their responsibilities
3. Data models
4. API structure
5. Areas that could be improved
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def review_implementation(self, code: str, context: str = "") -> str:
        """Review proposed implementation for technical fit."""
        task = f"""
Review the following implementation:

Context: {context}

Code:
```python
{code}
```

Provide feedback on:
1. Design patterns used
2. Type safety
3. Performance considerations
4. Potential improvements
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def print_design(self, feature_request: str):
        """Print the design interactively."""
        self.agent.print_response(f"Design a feature for: {feature_request}")


# Default instance
_default_architect: Optional[ArchitectAgent] = None


def get_architect() -> ArchitectAgent:
    """Get the default architect instance."""
    global _default_architect
    if _default_architect is None:
        _default_architect = ArchitectAgent()
    return _default_architect


if __name__ == "__main__":
    architect = ArchitectAgent()
    print("MLB Architect Agent")
    print("=" * 50)
    
    while True:
        feature = input("\nFeature to design (or 'exit'): ")
        if feature.lower() in ("exit", "quit"):
            break
        if feature.strip():
            architect.print_design(feature)
