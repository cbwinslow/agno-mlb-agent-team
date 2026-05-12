#!/usr/bin/env python3
"""
Workbench - Development Entry Point for MLB Agent Team

This is the interactive development environment for the agent team.
Use this for testing, exploration, and prototyping.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration
REPO_PATH = os.getenv("MLB_REPO_PATH", "/home/cbwinslow/mlb-baseball")
MODEL_ID = os.getenv("AGNO_MODEL", "gpt-4o")


def print_banner():
    """Print the workbench banner."""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║                    MLB AGENT TEAM WORKBENCH                     ║
║                                                                ║
║  Multi-agent AI team for mlb-baseball project development      ║
║                                                                ║
║  Agents: Coordinator | Architect | Coder | Tester | DocsWriter | DBSpecialist | StatsAgent | AppArchitect ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def interactive_mode():
    """Run the interactive workbench mode."""
    from agents import (
        CoordinatorAgent,
        ArchitectAgent,
        CoderAgent,
        TesterAgent,
        DocsWriterAgent,
        DBSpecialistAgent,
        StatsAgent,
        AppArchitectAgent,
    )
    
    # Create agents
    coordinator = CoordinatorAgent(repo_path=REPO_PATH, model_id=MODEL_ID)
    architect = ArchitectAgent(repo_path=REPO_PATH, model_id=MODEL_ID)
    coder = CoderAgent(repo_path=REPO_PATH, model_id=MODEL_ID)
    tester = TesterAgent(repo_path=REPO_PATH, model_id=MODEL_ID)
    docs = DocsWriterAgent(repo_path=REPO_PATH, model_id=MODEL_ID)
    db_specialist = DBSpecialistAgent(repo_path=REPO_PATH, model_id=MODEL_ID)
    stats = StatsAgent(repo_path=REPO_PATH, model_id=MODEL_ID)
    app_architect = AppArchitectAgent(repo_path=REPO_PATH, model_id=MODEL_ID)
    
    agents = {
        "coordinator": coordinator,
        "architect": architect,
        "coder": coder,
        "tester": tester,
        "docs": docs,
        "docs_writer": docs,
        "db_specialist": db_specialist,
        "stats": stats,
        "stats_agent": stats,
        "app_architect": app_architect,
    }
    
    print(f"Repository: {REPO_PATH}")
    print(f"Model: {MODEL_ID}")
    print("\nCommands:")
    print("  agent <name> <task>  - Run task with specific agent")
    print("  list                 - List available agents")
    print("  exit                 - Exit workbench")
    print()
    
    while True:
        try:
            user_input = input("workbench> ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ("exit", "quit", "q"):
                print("Goodbye!")
                break
            
            if user_input.lower() == "list":
                print("\nAvailable Agents:")
                for name in agents.keys():
                    print(f"  - {name}")
                print()
                continue
            
            # Parse agent command
            parts = user_input.split(" ", 1)
            agent_name = parts[0].lower()
            task = parts[1] if len(parts) > 1 else ""
            
            if agent_name in agents:
                if not task:
                    print(f"Usage: agent {agent_name} <task>")
                    continue
                
                print(f"\n[Running with {agent_name}]")
                print("-" * 50)
                
                if agent_name == "coordinator":
                    coordinator.print_response(task)
                elif agent_name == "architect":
                    architect.print_design(task)
                elif agent_name == "coder":
                    coder.print_implementation(task)
                elif agent_name in ("tester", "docs", "docs_writer"):
                    tester.print_tests(task) if agent_name == "tester" else docs.print_docs_update(task)
                
                print("-" * 50)
            else:
                print(f"Unknown agent: {agent_name}")
                print("Use 'list' to see available agents")
        
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit")
        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")


def team_mode():
    """Run with the full agent team coordination."""
    from agents import create_coordinator_team
    
    print("Starting Team Mode...")
    print("The coordinator will manage the team automatically.\n")
    
    team = create_coordinator_team()
    
    while True:
        try:
            task = input("Task (or 'exit'): ").strip()
            
            if task.lower() in ("exit", "quit"):
                break
            
            if task:
                print("\n[Team processing task...]\n")
                team.print_response(task)
        
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit")
        except EOFError:
            break


def analyze_mode():
    """Analyze the codebase with the architect agent."""
    from agents import get_architect
    
    print("Codebase Analysis Mode")
    print("=" * 50)
    
    architect = get_architect()
    
    areas = [
        "overall structure",
        "data models",
        "API endpoints",
        "data pipelines",
        "tests",
    ]
    
    print("\nAnalysis areas:")
    for i, area in enumerate(areas, 1):
        print(f"  {i}. {area}")
    
    while True:
        try:
            choice = input("\nAnalyze area (number or 'exit'): ").strip()
            
            if choice.lower() in ("exit", "quit"):
                break
            
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(areas):
                    print(f"\nAnalyzing: {areas[idx]}")
                    print("-" * 50)
                    architect.agent.print_response(
                        f"Analyze the {areas[idx]} of the mlb-baseball project. "
                        "Provide a detailed report."
                    )
                    print("-" * 50)
            else:
                # Treat as custom query
                if choice:
                    architect.agent.print_response(f"Analyze: {choice}")
        
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit")
        except EOFError:
            break


def main():
    """Main entry point."""
    print_banner()
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == "team":
            team_mode()
        elif mode == "analyze":
            analyze_mode()
        else:
            print(f"Unknown mode: {mode}")
            print("Usage: python workbench.py [interactive|team|analyze]")
    else:
        print("Select mode:")
        print("  1. Interactive - Work with individual agents")
        print("  2. Team        - Let coordinator manage the team")
        print("  3. Analyze     - Analyze the codebase")
        print()
        
        choice = input("Choice (1/2/3): ").strip()
        
        if choice == "1":
            interactive_mode()
        elif choice == "2":
            team_mode()
        elif choice == "3":
            analyze_mode()
        else:
            print("Invalid choice, starting interactive mode")
            interactive_mode()


if __name__ == "__main__":
    main()
