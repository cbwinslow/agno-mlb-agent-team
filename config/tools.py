"""
Agno Tools Configuration for MLB Agent Team

This module configures all tools available to the agent team.
"""

from typing import List, Optional
from agno.tools import Toolkit

# =============================================================================
# TOOL CATEGORIES
# =============================================================================

# Core tools that all agents should have access to
CORE_TOOLS = [
    "bash",      # Shell commands
    "python",    # Python interpreter
    "calculator", # Math calculations
]

# GitHub tools for repository operations
GITHUB_TOOLS = [
    "github",
]

# Database tools
DATABASE_TOOLS = [
    "postgres",  # PostgreSQL operations
    "sqlite",    # SQLite operations
]

# Web tools
WEB_TOOLS = [
    "duckduckgo",  # Search
    "wikipedia",   # Wikipedia
    "arxiv",       # Research papers
]

# File system tools
FILESYSTEM_TOOLS = [
    "filesystem",
]

# MCP tools - for MLB data servers
MCP_TOOLS = [
    "mcp_client",
]

# =============================================================================
# MLB-SPECIFIC TOOLS
# =============================================================================

# Data fetching tools for MLB sources
MLB_DATA_TOOLS = [
    "yfinance",    # Can be adapted for sports data
    "requests",    # Generic HTTP requests for APIs
]

# =============================================================================
# TOOL CONFIGURATIONS
# =============================================================================

def get_core_tools() -> List[str]:
    """Get list of core tools for all agents."""
    return CORE_TOOLS.copy()

def get_github_tools() -> List[str]:
    """Get GitHub-specific tools."""
    return GITHUB_TOOLS.copy()

def get_database_tools() -> List[str]:
    """Get database tools."""
    return DATABASE_TOOLS.copy()

def get_web_tools() -> List[str]:
    """Get web search tools."""
    return WEB_TOOLS.copy()

def get_mcp_tools() -> List[str]:
    """Get MCP client tools."""
    return MCP_TOOLS.copy()

def get_all_tools() -> List[str]:
    """Get all available tools."""
    tools = set()
    tools.update(CORE_TOOLS)
    tools.update(GITHUB_TOOLS)
    tools.update(DATABASE_TOOLS)
    tools.update(WEB_TOOLS)
    tools.update(FILESYSTEM_TOOLS)
    tools.update(MCP_TOOLS)
    tools.update(MLB_DATA_TOOLS)
    return sorted(list(tools))

# =============================================================================
# TOOL PERMISSIONS
# =============================================================================

# Tools that require confirmation before execution
CONFIRMATION_REQUIRED = [
    "bash",
    "filesystem_write",
    "github_create_pr",
    "database_write",
]

# Tools that are read-only (safer)
READ_ONLY_TOOLS = [
    "calculator",
    "duckduckgo",
    "wikipedia",
    "arxiv",
    "github_read",
    "database_read",
]

# =============================================================================
# MCP SERVER CONFIGURATION
# =============================================================================

# MLB Data MCP servers
MCP_SERVERS = {
    "mlb_stats": {
        "command": "npx",
        "args": ["-y", "@etweiler/mlb-mcp"],
        "description": "MLB Stats API data",
    },
    "pybaseball": {
        "command": "python",
        "args": ["-m", "pybaseball"],
        "description": "pybaseball library wrapper",
    },
}

# =============================================================================
# TOOL DESCRIPTIONS
# =============================================================================

TOOL_DESCRIPTIONS = {
    "bash": "Execute shell commands",
    "python": "Run Python code in a sandboxed environment",
    "calculator": "Perform mathematical calculations",
    "github": "Interact with GitHub API (repos, issues, PRs)",
    "postgres": "Query and manage PostgreSQL databases",
    "sqlite": "Query and manage SQLite databases",
    "duckduckgo": "Search the web using DuckDuckGo",
    "wikipedia": "Search and read Wikipedia articles",
    "arxiv": "Search academic papers on arXiv",
    "filesystem": "Read, write, and manage local files",
    "mcp_client": "Connect to MCP servers for specialized data",
    "yfinance": "Fetch financial/sports data (adaptable)",
    "requests": "Make HTTP requests to APIs",
}
