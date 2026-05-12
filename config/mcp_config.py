"""
MCP Server Configuration for MLB Agent Team

This module configures MCP (Model Context Protocol) servers for accessing
specialized data sources like MLB statistics.
"""

import os
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field


@dataclass
class MCPServer:
    """Configuration for an MCP server."""
    name: str
    command: str
    args: List[str] = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)
    description: str = ""
    enabled: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "command": self.command,
            "args": self.args,
            "env": self.env,
            "description": self.description,
            "enabled": self.enabled,
        }


# =============================================================================
# MLB MCP SERVERS
# =============================================================================

# Community MCP servers for MLB data
MLB_MCP_SERVERS = [
    MCPServer(
        name="mlb-stats",
        command="npx",
        args=["-y", "@etweiler/mlb-mcp"],
        description="MLB Stats API via MCP protocol",
    ),
    MCPServer(
        name="mlb-api",
        command="uvx",
        args=["mlb-api-mcp"],
        description="MLB API MCP server",
    ),
]

# Baseball data MCP servers
BASEBALL_MCP_SERVERS = [
    MCPServer(
        name="pybaseball",
        command="python",
        args=["-m", "pybaseball"],
        description="pybaseball library wrapper",
    ),
]

# =============================================================================
# MCP CLIENT CONFIGURATION
# =============================================================================

def get_mcp_servers_config() -> List[Dict[str, Any]]:
    """Get configuration for MCP servers."""
    servers = []
    
    for server in MLB_MCP_SERVERS + BASEBALL_MCP_SERVERS:
        if server.enabled:
            servers.append(server.to_dict())
    
    return servers


# =============================================================================
# MCP TOOLS MAPPING
# =============================================================================

# Map MCP servers to available tools
MCP_TOOLS = {
    "mlb-stats": [
        "get_player_stats",
        "get_team_standings", 
        "get_game_schedule",
        "get_season_stats",
    ],
    "mlb-api": [
        "get_live_scores",
        "get_player_info",
        "get_boxscore",
    ],
    "pybaseball": [
        "statcast",
        "player_lookup",
        "batting_stats",
        "pitching_stats",
        "standings",
        "schedule",
    ],
}


# =============================================================================
# AGENT MCP CONFIGURATIONS
# =============================================================================

# Which agents get which MCP tools
AGENT_MCP_CONFIG = {
    "stats_agent": ["mlb-stats", "pybaseball"],
    "db_specialist": ["pybaseball"],
    "coordinator": ["mlb-api"],
}


# =============================================================================
# MCP SERVER MANAGEMENT
# =============================================================================

def get_enabled_servers() -> List[MCPServer]:
    """Get list of enabled MCP servers."""
    all_servers = MLB_MCP_SERVERS + BASEBALL_MCP_SERVERS
    return [s for s in all_servers if s.enabled]


def get_servers_for_agent(agent_name: str) -> List[MCPServer]:
    """Get MCP servers configured for a specific agent."""
    server_names = AGENT_MCP_CONFIG.get(agent_name, [])
    all_servers = MLB_MCP_SERVERS + BASEBALL_MCP_SERVERS
    return [s for s in all_servers if s.name in server_names and s.enabled]


def enable_server(server_name: str) -> bool:
    """Enable an MCP server by name."""
    for server in MLB_MCP_SERVERS + BASEBALL_MCP_SERVERS:
        if server.name == server_name:
            server.enabled = True
            return True
    return False


def disable_server(server_name: str) -> bool:
    """Disable an MCP server by name."""
    for server in MLB_MCP_SERVERS + BASEBALL_MCP_SERVERS:
        if server.name == server_name:
            server.enabled = False
            return True
    return False


# =============================================================================
# MCP CLIENT SETUP
# =============================================================================

def get_mcp_client_config() -> Dict[str, Any]:
    """
    Get configuration for MCP client connection.
    
    This is used to connect agents to MCP servers.
    """
    return {
        "servers": get_mcp_servers_config(),
        "tools": MCP_TOOLS,
        "agent_config": AGENT_MCP_CONFIG,
    }
