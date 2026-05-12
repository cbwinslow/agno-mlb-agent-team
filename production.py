#!/usr/bin/env python3
"""
Production Entry Point for MLB Agent Team

This module provides the production deployment configuration
for the agent team using AgentOS and FastAPI.
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

# Configuration from environment
PORT = int(os.getenv("AGNO_PORT", "8000"))
HOST = os.getenv("AGNO_HOST", "0.0.0.0")
DATABASE_URL = os.getenv("DATABASE_URL")  # PostgreSQL URL if using Postgres
DB_FILE = os.getenv("AGNO_DB_FILE", "./data/agno.db")
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
ENABLE_TRACING = os.getenv("ENABLE_TRACING", "true").lower() == "true"


def create_production_runtime():
    """Create the production runtime with all configurations."""
    from runtime.agentos import create_agentos_runtime
    
    runtime = create_agentos_runtime(
        db_url=DATABASE_URL,
        db_file=DB_FILE,
        tracing=ENABLE_TRACING,
    )
    
    return runtime


def create_production_app():
    """Create the production FastAPI application."""
    from runtime.api_server import create_app
    
    runtime = create_production_runtime()
    app = create_app(runtime)
    
    return app


def run_server():
    """Run the production server."""
    import uvicorn
    
    app = create_production_app()
    
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                  MLB AGENT TEAM - PRODUCTION                      ║
╠══════════════════════════════════════════════════════════════════╣
║  Server: http://{HOST}:{PORT}                                     ║
║  API Docs: http://{HOST}:{PORT}/docs                               ║
║  Health: http://{HOST}:{PORT}/health                              ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level=LOG_LEVEL,
        workers=1,  # AgentOS is not thread-safe
    )


def run_scheduler():
    """Run scheduled tasks using the agent team."""
    from apscheduler.schedulers.background import BackgroundScheduler
    from runtime.agentos import get_runtime
    
    scheduler = BackgroundScheduler()
    runtime = get_runtime()
    
    # Example: Daily codebase analysis
    def daily_analysis():
        print("Running daily analysis...")
        # Add scheduled task logic here
        pass
    
    # Schedule daily analysis at 2 AM
    scheduler.add_job(
        daily_analysis,
        "cron",
        hour=2,
        minute=0,
        id="daily_analysis",
    )
    
    scheduler.start()
    print("Scheduler started. Press Ctrl+C to exit.")
    
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.shutdown()


def run_worker():
    """Run as a background worker processing tasks from a queue."""
    print("Starting worker mode...")
    print("Worker will process tasks from the configured queue.")
    
    # Placeholder for queue-based worker implementation
    # This would integrate with Redis, RabbitMQ, etc.
    print("Worker mode not yet implemented.")
    print("Use 'python production.py serve' to run the API server.")


def main():
    """Main entry point with command routing."""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "serve":
            run_server()
        elif command == "scheduler":
            run_scheduler()
        elif command == "worker":
            run_worker()
        elif command == "shell":
            # Interactive shell with runtime available
            from runtime.agentos import get_runtime
            runtime = get_runtime()
            print(f"Runtime ready: {runtime.name}")
            print(f"Agents: {[a.name for a in runtime.agents]}")
            
            # Drop into Python REPL
            import code
            code.interact(local=globals())
        else:
            print(f"Unknown command: {command}")
            print_help()
    else:
        run_server()


def print_help():
    """Print help message."""
    print("""
MLB Agent Team - Production Commands

Usage: python production.py <command>

Commands:
  serve      - Run the FastAPI server (default)
  scheduler  - Run scheduled background tasks
  worker     - Run as a background worker
  shell      - Start Python shell with runtime

Environment Variables:
  AGNO_PORT       - Server port (default: 8000)
  AGNO_HOST       - Server host (default: 0.0.0.0)
  DATABASE_URL     - PostgreSQL connection URL (optional)
  AGNO_DB_FILE    - SQLite database file (default: ./data/agno.db)
  LOG_LEVEL       - Log level (default: info)
  ENABLE_TRACING   - Enable OpenTelemetry tracing (default: true)
""")


if __name__ == "__main__":
    main()
