"""
Tester Agent - Quality Assurance

This agent writes tests, validates code, and ensures quality.
"""

from typing import Optional, List, Dict
from pathlib import Path

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.file_system import FileSystemTools
from agno.tools.shell import ShellTools

from config import DEFAULT_INSTRUCTIONS
from prompts.tester import TESTER_PROMPT


def create_tester_agent(
    repo_path: str = "/home/cbwinslow/mlb-baseball",
    model_id: str = "gpt-4o-mini",
) -> Agent:
    """Create a tester agent for quality assurance."""
    
    # Load the system prompt
    prompt_path = Path(__file__).parent.parent / "prompts" / "tester.md"
    if prompt_path.exists():
        system_prompt = prompt_path.read_text()
    else:
        system_prompt = TESTER_PROMPT
    
    agent = Agent(
        name="Tester",
        model=OpenAIChat(id=model_id),
        system_message=system_prompt,
        instructions=[
            f"Repository: {repo_path}",
            DEFAULT_INSTRUCTIONS,
            "Always run tests after writing them.",
            "Report coverage metrics.",
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


class TesterAgent:
    """Wrapper class for the tester agent."""
    
    def __init__(
        self,
        repo_path: str = "/home/cbwinslow/mlb-baseball",
        model_id: str = "gpt-4o-mini",
    ):
        self.repo_path = repo_path
        self.model_id = model_id
        self.agent = create_tester_agent(repo_path, model_id)
    
    def write_tests(
        self,
        module_path: str,
        test_type: str = "unit",
    ) -> str:
        """Write tests for a module."""
        task = f"""
Write tests for: {module_path}

Test type: {test_type}

Please:
1. Explore the module to understand its interface
2. Create tests in the appropriate tests/ directory
3. Cover happy path, edge cases, and error conditions
4. Use pytest fixtures where appropriate
5. Run the tests and verify they pass
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def validate_feature(self, feature_description: str, implementation_path: str) -> str:
        """Validate that a feature implementation works correctly."""
        task = f"""
Validate the following feature implementation:

Feature: {feature_description}
Implementation: {implementation_path}

Please:
1. Read the implementation
2. Write comprehensive tests
3. Run the tests
4. Check linting (ruff) and types (mypy)
5. Report any issues found
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def run_test_suite(
        self,
        test_path: Optional[str] = None,
        verbose: bool = True,
    ) -> Dict[str, any]:
        """Run the test suite and report results."""
        task = f"""
Run the test suite.

{"Test path: " + test_path if test_path else "Run all tests in tests/ directory"}

Report:
- Number of tests passed/failed
- Coverage percentage
- Any linting errors
"""
        response = self.agent.run(task)
        return {
            "content": response.content if hasattr(response, 'content') else str(response),
            "success": True,  # Parse actual results from response
        }
    
    def check_code_quality(self, file_path: str) -> str:
        """Check code quality (linting, types)."""
        task = f"""
Check code quality for: {file_path}

Run:
1. ruff check {file_path}
2. ruff format --check {file_path}
3. mypy {file_path}

Report any issues.
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def verify_bug_fix(
        self,
        bug_description: str,
        fix_path: str,
    ) -> str:
        """Verify that a bug has been fixed."""
        task = f"""
Verify the bug fix:

Bug: {bug_description}
Fix location: {fix_path}

Please:
1. Write a test that reproduces the original bug
2. Run the test (should fail on original code)
3. Verify the fix is applied
4. Run the test again (should pass now)
5. Run full test suite to ensure no regressions
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def print_tests(self, module: str):
        """Print test writing process interactively."""
        self.agent.print_response(f"Write tests for: {module}")


# Default instance
_default_tester: Optional[TesterAgent] = None


def get_tester() -> TesterAgent:
    """Get the default tester instance."""
    global _default_tester
    if _default_tester is None:
        _default_tester = TesterAgent()
    return _default_tester


if __name__ == "__main__":
    tester = TesterAgent()
    print("MLB Tester Agent")
    print("=" * 50)
    
    while True:
        task = input("\nModule to test (or 'exit'): ")
        if task.lower() in ("exit", "quit"):
            break
        if task.strip():
            tester.print_tests(task)
