"""
Docs Writer Agent - Documentation Maintenance

This agent maintains and updates project documentation.
"""

from typing import Optional, List
from pathlib import Path

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.file_system import FileSystemTools

from config import DEFAULT_INSTRUCTIONS
from prompts.docs_writer import DOCS_WRITER_PROMPT


def create_docs_writer_agent(
    repo_path: str = "/home/cbwinslow/mlb-baseball",
    model_id: str = "gpt-4o-mini",
) -> Agent:
    """Create a docs writer agent."""
    
    # Load the system prompt
    prompt_path = Path(__file__).parent.parent / "prompts" / "docs_writer.md"
    if prompt_path.exists():
        system_prompt = prompt_path.read_text()
    else:
        system_prompt = DOCS_WRITER_PROMPT
    
    agent = Agent(
        name="DocsWriter",
        model=OpenAIChat(id=model_id),
        system_message=system_prompt,
        instructions=[
            f"Repository: {repo_path}",
            DEFAULT_INSTRUCTIONS,
            "Always verify documentation examples work.",
            "Keep changelog up to date.",
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


class DocsWriterAgent:
    """Wrapper class for the docs writer agent."""
    
    def __init__(
        self,
        repo_path: str = "/home/cbwinslow/mlb-baseball",
        model_id: str = "gpt-4o-mini",
    ):
        self.repo_path = repo_path
        self.model_id = model_id
        self.agent = create_docs_writer_agent(repo_path, model_id)
    
    def document_feature(self, feature_description: str, implementation_path: str) -> str:
        """Document a new feature."""
        task = f"""
Document the following feature:

Feature: {feature_description}
Implementation: {implementation_path}

Please:
1. Read the implementation
2. Update README.md if needed
3. Add API documentation to docs/api.md
4. Update CHANGELOG.md
5. Add code examples
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def update_api_docs(self, endpoint: str, new_implementation: str) -> str:
        """Update API documentation for an endpoint."""
        task = f"""
Update API documentation for:

Endpoint: {endpoint}
Implementation: {new_implementation}

Please:
1. Read the new implementation
2. Document request/response schemas
3. Add or update examples
4. Update docs/api.md
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def update_readme(self, changes: str) -> str:
        """Update the README with new information."""
        task = f"""
Update the README with the following changes:

{changes}

Please:
1. Read current README
2. Make appropriate updates
3. Maintain formatting and style
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def add_changelog_entry(
        self,
        version: str = "Unreleased",
        changes: dict = None,
    ) -> str:
        """Add an entry to the changelog."""
        changes = changes or {}
        task = f"""
Add changelog entry for version: {version}

Changes:
{chr(10).join(f"- {k}: {v}" for k, v in changes.items())}

Please update CHANGELOG.md following existing format.
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def create_tutorial(self, topic: str) -> str:
        """Create a tutorial document."""
        task = f"""
Create a tutorial for: {topic}

Please:
1. Identify key tasks a user would want to accomplish
2. Write step-by-step instructions
3. Include working code examples
4. Add a troubleshooting section
5. Save to docs/tutorials/{topic.lower().replace(' ', '_')}.md
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def audit_docs(self) -> str:
        """Audit all documentation for completeness and accuracy."""
        task = f"""
Audit the documentation in the mlb-baseball project.

Check:
1. README is complete and accurate
2. API docs match implementations
3. All examples work
4. No broken links
5. CHANGELOG is up to date

Report any issues found.
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def print_docs_update(self, feature: str):
        """Print documentation update process interactively."""
        self.agent.print_response(f"Document feature: {feature}")


# Default instance
_default_docs_writer: Optional[DocsWriterAgent] = None


def get_docs_writer() -> DocsWriterAgent:
    """Get the default docs writer instance."""
    global _default_docs_writer
    if _default_docs_writer is None:
        _default_docs_writer = DocsWriterAgent()
    return _default_docs_writer


if __name__ == "__main__":
    docs = DocsWriterAgent()
    print("MLB Docs Writer Agent")
    print("=" * 50)
    
    while True:
        task = input("\nFeature to document (or 'exit'): ")
        if task.lower() in ("exit", "quit"):
            break
        if task.strip():
            docs.print_docs_update(task)
