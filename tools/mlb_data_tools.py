"""
Custom MLB Data Tools for Agno Agent Team

These tools provide direct access to MLB data sources for the agents.
"""

import os
import json
import subprocess
from typing import Optional, Dict, Any, List
from datetime import datetime, date
import requests

from agno.tools import Toolkit
from agno.tools.tool import tool


class MLBDataTools(Toolkit):
    """
    Custom toolkit for accessing MLB data sources.
    
    Sources:
    - pybaseball library (Statcast, FanGraphs, Baseball Reference)
    - MLB Stats API
    - Custom CSV/parquet files
    """
    
    def __init__(self):
        super().__init__(name="mlb_data")
        
        # MLB data paths
        self.data_path = os.path.expanduser("~/mlb-baseball/data")
        self.raw_path = os.path.join(self.data_path, "raw")
        self.processed_path = os.path.join(self.data_path, "processed")
    
    @tool(name="get_player_stats", description="Get batting/pitching statistics for a player")
    def get_player_stats(
        self, 
        player_name: str, 
        season: Optional[int] = None,
        stat_type: str = "batting"
    ) -> str:
        """
        Get player statistics using pybaseball.
        
        Args:
            player_name: Player's full name (e.g., "Mike Trout")
            season: Year (defaults to most recent)
            stat_type: "batting" or "pitching"
        """
        try:
            from pybaseball import player_lookup, batting_stats, pitching_stats
            
            # Find player ID
            player_id = player_lookup(player_name)
            if player_id.empty:
                return f"Player '{player_name}' not found"
            
            pid = player_id['key_mlbam'].iloc[0]
            
            # Get stats
            if stat_type == "batting":
                stats = batting_stats(season if season else date.today().year)
            else:
                stats = pitching_stats(season if season else date.today().year)
            
            player_stats = stats[stats['IDfg'] == pid]
            
            if player_stats.empty:
                return f"No {stat_type} stats found for {player_name}"
            
            return player_stats.to_string()
            
        except ImportError:
            return "pybaseball not installed. Run: pip install pybaseball"
        except Exception as e:
            return f"Error fetching player stats: {str(e)}"
    
    @tool(name="get_statcast_data", description="Get Statcast data (exit velocity, launch angle, etc.)")
    def get_statcast_data(
        self,
        start_date: str,
        end_date: str,
        player_id: Optional[int] = None
    ) -> str:
        """
        Get Statcast data for a date range.
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            player_id: Optional MLB player ID
        """
        try:
            from pybaseball import statcast
            
            data = statcast(start_date, end_date)
            
            if player_id:
                data = data[data['batter'] == player_id]
            
            return f"Retrieved {len(data)} Statcast records from {start_date} to {end_date}"
            
        except ImportError:
            return "pybaseball not installed"
        except Exception as e:
            return f"Error fetching Statcast data: {str(e)}"
    
    @tool(name="search_player", description="Search for a player by name")
    def search_player(self, query: str) -> str:
        """
        Search for players by name.
        
        Args:
            query: Player name (partial match works)
        """
        try:
            from pybaseball import player_lookup
            
            results = player_lookup(query)
            
            if results.empty:
                return f"No players found matching '{query}'"
            
            # Return top 10 results
            return results.head(10)[['namefirst', 'namelast', 'key_mlbam', 'key_bbref']].to_string()
            
        except ImportError:
            return "pybaseball not installed"
        except Exception as e:
            return f"Error searching player: {str(e)}"
    
    @tool(name="get_team_standings", description="Get current MLB standings")
    def get_team_standings(self, league: str = "all") -> str:
        """
        Get current team standings.
        
        Args:
            league: "al", "nl", or "all"
        """
        try:
            from pybaseball import standings
            
            stand = standings()
            
            if league != "all":
                stand = stand[stand['League'] == league]
            
            return stand.to_string()
            
        except ImportError:
            return "pybaseball not installed"
        except Exception as e:
            return f"Error fetching standings: {str(e)}"
    
    @tool(name="get_schedule", description="Get MLB schedule for a date range")
    def get_schedule(
        self,
        start_date: str,
        end_date: str,
        team: Optional[str] = None
    ) -> str:
        """
        Get MLB schedule.
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            team: Optional team abbreviation (e.g., "NYY")
        """
        try:
            from pybaseball import schedule_data
            
            schedule = schedule_data(start_date, end_date)
            
            if team:
                schedule = schedule[schedule['Home'] == team | schedule['Away'] == team]
            
            return schedule.to_string()
            
        except ImportError:
            return "pybaseball not installed"
        except Exception as e:
            return f"Error fetching schedule: {str(e)}"
    
    @tool(name="calculate_sabermetrics", description="Calculate advanced baseball statistics")
    def calculate_sabermetrics(
        self,
        hits: int,
        at_bats: int,
        doubles: int = 0,
        triples: int = 0,
        home_runs: int = 0,
        walks: int = 0,
        hbp: int = 0,
        sacrifice_flies: int = 0
    ) -> str:
        """
        Calculate sabermetrics from basic stats.
        
        Args:
            hits: Total hits (H)
            at_bats: At bats (AB)
            doubles: Doubles (2B)
            triples: Triples (3B)
            home_runs: Home runs (HR)
            walks: Walks (BB)
            hbp: Hit by pitch (HBP)
            sacrifice_flies: Sacrifice flies (SF)
        """
        # Prevent division by zero
        if at_bats == 0:
            return "Error: At bats cannot be zero"
        
        # Basic stats
        singles = hits - doubles - triples - home_runs
        total_bases = singles + (2 * doubles) + (3 * triples) + (4 * home_runs)
        
        # Batting average
        ba = hits / at_bats
        
        # On-base percentage
        plate_appearances = at_bats + walks + hbp + sacrifice_flies
        on_base = (hits + walks + hbp) / plate_appearances if plate_appearances > 0 else 0
        
        # Slugging percentage
        slg = total_bases / at_bats
        
        # OPS
        ops = on_base + slg
        
        # ISO (Isolated Power)
        iso = slg - ba
        
        return f"""
Advanced Statistics:
- Batting Average (BA): {ba:.3f}
- On-Base Percentage (OBP): {on_base:.3f}
- Slugging Percentage (SLG): {slg:.3f}
- OPS: {ops:.3f}
- ISO (Isolated Power): {iso:.3f}
- Total Bases: {total_bases}
"""
    
    @tool(name="get_local_data", description="List available local MLB data files")
    def list_local_data(self) -> str:
        """
        List available local MLB data files.
        """
        import os
        
        paths_to_check = [
            (self.raw_path, "raw"),
            (self.processed_path, "processed"),
            ("~/mlb-baseball/baseball/sources", "sources"),
        ]
        
        result = []
        for path, label in paths_to_check:
            expanded = os.path.expanduser(path)
            if os.path.exists(expanded):
                files = os.listdir(expanded)
                result.append(f"\n{label.upper()} ({expanded}):")
                for f in files[:20]:  # Limit to 20 files
                    result.append(f"  - {f}")
                if len(files) > 20:
                    result.append(f"  ... and {len(files) - 20} more files")
            else:
                result.append(f"\n{label.upper()}: Directory not found")
        
        return "\n".join(result)
    
    @tool(name="read_csv_data", description="Read a CSV data file")
    def read_csv_data(self, filename: str, limit: int = 100) -> str:
        """
        Read a CSV file from local MLB data.
        
        Args:
            filename: Name of the CSV file
            limit: Number of rows to read
        """
        import os
        import pandas as pd
        
        # Search for file
        search_paths = [
            os.path.join(self.raw_path, filename),
            os.path.join(self.processed_path, filename),
            os.path.expanduser(f"~/mlb-baseball/{filename}"),
        ]
        
        file_path = None
        for path in search_paths:
            if os.path.exists(path):
                file_path = path
                break
        
        if not file_path:
            return f"File '{filename}' not found in expected locations"
        
        try:
            df = pd.read_csv(file_path)
            return f"File: {file_path}\nShape: {df.shape}\n\n{df.head(limit).to_string()}"
        except Exception as e:
            return f"Error reading file: {str(e)}"


# =============================================================================
# TOOLKIT FACTORY
# =============================================================================

def get_mlb_data_tools() -> MLBDataTools:
    """Get an instance of MLB data tools."""
    return MLBDataTools()
