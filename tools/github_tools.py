"""
GitHub Tools for Agno Agent Team

Provides GitHub API integration for repository operations.
"""

import os
from typing import Optional, List, Dict
from pathlib import Path

try:
    from github import Github
    from github.GithubException import GithubException
    HAS_PYTHON_GITHUB = True
except ImportError:
    HAS_PYTHON_GITHUB = False


class GitHubTools:
    """Tools for interacting with GitHub repositories."""
    
    def __init__(
        self,
        token: Optional[str] = None,
        repo_url: str = "https://github.com/cbwinslow/mlb-baseball",
    ):
        """
        Initialize GitHub tools.
        
        Args:
            token: GitHub personal access token
            repo_url: Repository URL
        """
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.repo_url = repo_url
        
        # Parse owner and repo from URL
        parts = repo_url.rstrip("/").split("/")
        self.owner = parts[-2]
        self.repo_name = parts[-1]
        
        if HAS_PYTHON_GITHUB and self.token:
            self.client = Github(self.token)
            self.repo = self.client.get_repo(f"{self.owner}/{self.repo_name}")
        else:
            self.client = None
            self.repo = None
    
    def get_file(self, path: str, ref: str = "main") -> Optional[str]:
        """Get file contents from repository."""
        if not self.repo:
            return None
        
        try:
            contents = self.repo.get_contents(path, ref=ref)
            if hasattr(contents, 'decoded_content'):
                return contents.decoded_content.decode('utf-8')
            return None
        except GithubException:
            return None
    
    def list_files(self, path: str = "", ref: str = "main") -> List[Dict]:
        """List files in a directory."""
        if not self.repo:
            return []
        
        try:
            contents = self.repo.get_contents(path, ref=ref)
            return [
                {
                    "name": c.name,
                    "path": c.path,
                    "type": c.type,
                    "sha": c.sha,
                }
                for c in contents
            ]
        except GithubException:
            return []
    
    def create_or_update_file(
        self,
        path: str,
        content: str,
        message: str,
        branch: Optional[str] = None,
    ) -> bool:
        """Create or update a file in the repository."""
        if not self.repo:
            return False
        
        try:
            # Check if file exists
            try:
                existing = self.repo.get_contents(path, ref=branch or "main")
                # Update existing file
                self.repo.update_file(
                    path=path,
                    message=message,
                    content=content,
                    sha=existing.sha,
                    branch=branch,
                )
            except GithubException:
                # Create new file
                self.repo.create_file(
                    path=path,
                    message=message,
                    content=content,
                    branch=branch,
                )
            return True
        except GithubException as e:
            print(f"Error updating file: {e}")
            return False
    
    def create_branch(self, branch_name: str, from_branch: str = "main") -> bool:
        """Create a new branch."""
        if not self.repo:
            return False
        
        try:
            # Get the source reference
            source = self.repo.get_branch(from_branch)
            
            # Create new branch
            self.repo.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=source.commit.sha,
            )
            return True
        except GithubException as e:
            print(f"Error creating branch: {e}")
            return False
    
    def create_pull_request(
        self,
        title: str,
        body: str,
        head: str,
        base: str = "main",
    ) -> Optional[Dict]:
        """Create a pull request."""
        if not self.repo:
            return None
        
        try:
            pr = self.repo.create_pull(
                title=title,
                body=body,
                head=head,
                base=base,
            )
            return {
                "number": pr.number,
                "url": pr.html_url,
                "state": pr.state,
            }
        except GithubException as e:
            print(f"Error creating PR: {e}")
            return None
    
    def get_issues(self, state: str = "open") -> List[Dict]:
        """Get repository issues."""
        if not self.repo:
            return []
        
        try:
            issues = self.repo.get_issues(state=state)
            return [
                {
                    "number": i.number,
                    "title": i.title,
                    "body": i.body,
                    "state": i.state,
                    "labels": [l.name for l in i.labels],
                }
                for i in issues
            ]
        except GithubException:
            return []
    
    def get_pull_requests(self, state: str = "open") -> List[Dict]:
        """Get repository pull requests."""
        if not self.repo:
            return []
        
        try:
            prs = self.repo.get_pulls(state=state)
            return [
                {
                    "number": pr.number,
                    "title": pr.title,
                    "body": pr.body,
                    "state": pr.state,
                    "url": pr.html_url,
                }
                for pr in prs
            ]
        except GithubException:
            return []


# Default instance
_github_tools: Optional[GitHubTools] = None


def get_github_tools() -> GitHubTools:
    """Get the default GitHub tools instance."""
    global _github_tools
    if _github_tools is None:
        _github_tools = GitHubTools()
    return _github_tools


if __name__ == "__main__":
    # Test GitHub connection
    tools = GitHubTools()
    print(f"Repository: {tools.owner}/{tools.repo_name}")
    
    if tools.repo:
        print("Connected to GitHub")
        files = tools.list_files()
        print(f"Root files: {len(files)}")
    else:
        print("GitHub connection not available (no token?)")
