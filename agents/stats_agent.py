"""
Statistical Modelling Specialist Agent

This agent handles statistical analysis, sabermetrics, data modeling,
and predictive analytics for the MLB project.
"""

from typing import Optional, List, Dict
from pathlib import Path

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.file_system import FileSystemTools
from agno.tools.shell import ShellTools

from config import DEFAULT_INSTRUCTIONS


def create_stats_agent(
    repo_path: str = "/home/cbwinslow/mlb-baseball",
    model_id: str = "gpt-4o",
) -> Agent:
    """Create a statistical modelling specialist agent."""
    
    system_prompt = """You are the **Statistical Modelling Specialist** for the MLB Agent Team. You are the authority on sabermetrics, statistical analysis, and data modeling for baseball analytics.

## Your Role

You enable data-driven insights by:
1. Implementing advanced baseball statistics (sabermetrics)
2. Creating statistical models for predictions
3. Designing data aggregation pipelines
4. Building reporting and analytics systems
5. Validating data quality and accuracy
6. Creating visualizations and dashboards

## Sabermetrics Expertise

### Core Statistics
- **BA (Batting Average)**: H / AB
- **OBP (On-Base Percentage)**: (H + BB + HBP) / (AB + BB + HBP + SF)
- **SLG (Slugging)**: TB / AB
- **OPS**: OBP + SLG
- **WAR (Wins Above Replacement)**: Complex metric combining offense/defense

### Advanced Metrics
```python
# Expected Weighted On-Base Average (xwOBA)
def calculate_xwoba(launch_speed, launch_angle, barrel_rate):
    # xwOBA combines exit velocity and launch angle
    # to predict expected outcomes
    pass

# Fielding Independent Pitching
def calculate_fip(hrs, bbs, hbps, ks, ips):
    # FIP = ((13*HR) + (3*(BB+HBP)) - (2*K)) / IP + constant
    constant = 3.10  # League average
    return ((13*hrs) + (3*(bbs+hbps)) - (2*ks)) / ips + constant

# Win Probability Added
def calculate_wpa(result, base_out, win_expectancy):
    # WPA measures impact on team's win probability
    pass
```

### Statistical Models
- Poisson regression for run scoring
- Logistic regression for binary outcomes (hit/no hit)
- Random forest for player projection
- Bayesian models for career trajectory

## MLB Project Context

This project aggregates:
- MLB Stats API: Box scores, play-by-play, player stats
- FanGraphs: Advanced metrics, projections
- Historical data from retrosheet

Data includes:
- Player statistics (hitting, pitching, fielding)
- Game events and outcomes
- Career trajectories

## Your Tools

- **FileSystemTools**: Read/write analysis scripts, notebooks
- **ShellTools**: Run Python/pandas scripts

## Tasks You Handle

1. **Metric Implementation**: Calculate advanced statistics
2. **Data Analysis**: Explore and validate data
3. **Model Development**: Build predictive models
4. **Pipeline Design**: Create ETL for statistics
5. **Reporting**: Generate analytics and insights
6. **Visualization**: Create charts and dashboards

## Output Format

When implementing statistics, provide:
```markdown
## Statistical Analysis

### Metric Definition
- Formula and components
- Expected values and ranges
- Interpretation

### Implementation
- Python code with docstrings
- Test cases with expected inputs/outputs

### Data Requirements
- Input fields needed
- Data quality checks

### Performance Considerations
- Computational complexity
- Optimization opportunities
```

## Repository

- URL: https://github.com/cbwinslow/mlb-baseball
- Local Path: /home/cbwinslow/mlb-baseball

## Working with the Team

- Receive stats tasks from the Coordinator
- Work with Coder on data pipelines
- Collaborate with DBSpecialist on data storage
- Provide validation to Tester
"""
    
    agent = Agent(
        name="StatsAgent",
        model=OpenAIChat(id=model_id),
        system_message=system_prompt,
        instructions=[
            f"Repository: {repo_path}",
            DEFAULT_INSTRUCTIONS,
            "Always validate statistical calculations.",
            "Document assumptions and data quality.",
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


class StatsAgent:
    """Wrapper class for the stats agent."""
    
    def __init__(
        self,
        repo_path: str = "/home/cbwinslow/mlb-baseball",
        model_id: str = "gpt-4o",
    ):
        self.repo_path = repo_path
        self.model_id = model_id
        self.agent = create_stats_agent(repo_path, model_id)
    
    def implement_metric(self, metric_spec: str) -> str:
        """Implement a statistical metric."""
        task = f"""
Implement the following baseball metric:

{metric_spec}

Please provide:
1. Metric definition and formula
2. Python implementation with docstrings
3. Unit tests with expected values
4. Edge case handling
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def analyze_data(self, analysis_request: str) -> str:
        """Perform statistical analysis on data."""
        task = f"""
Perform statistical analysis:

{analysis_request}

Provide:
1. Analysis approach
2. Statistical methods used
3. Key findings
4. Supporting visualizations (if applicable)
5. Conclusions and recommendations
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def build_model(self, model_spec: str) -> str:
        """Build a predictive model."""
        task = f"""
Build a predictive model:

{model_spec}

Include:
1. Model type and rationale
2. Feature engineering
3. Training approach
4. Evaluation metrics
5. Python implementation
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def design_pipeline(self, pipeline_spec: str) -> str:
        """Design a data pipeline for statistics."""
        task = f"""
Design a data pipeline for:

{pipeline_spec}

Include:
1. Pipeline stages (extract, transform, load)
2. Data sources and destinations
3. Transformation logic
4. Error handling
5. Scheduling considerations
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def validate_data(self, validation_spec: str) -> str:
        """Validate data quality."""
        task = f"""
Validate data quality for:

{validation_spec}

Check:
1. Completeness (no missing values in key fields)
2. Consistency (formats, ranges)
3. Accuracy (compared to known sources)
4. Timeliness (up-to-date)
5. Provide validation code and report
"""
        response = self.agent.run(task)
        return response.content if hasattr(response, 'content') else str(response)
    
    def print_metric(self, metric: str):
        """Print metric implementation interactively."""
        self.agent.print_response(f"Implement metric: {metric}")


# Default instance
_default_stats_agent: Optional[StatsAgent] = None


def get_stats_agent() -> StatsAgent:
    """Get the default stats agent instance."""
    global _default_stats_agent
    if _default_stats_agent is None:
        _default_stats_agent = StatsAgent()
    return _default_stats_agent


if __name__ == "__main__":
    stats = StatsAgent()
    print("Statistical Modelling Specialist Agent")
    print("=" * 50)
    print("Expertise: Sabermetrics, Data Analysis, Predictive Models")
    
    while True:
        task = input("\nTask (or 'exit'): ")
        if task.lower() in ("exit", "quit"):
            break
        if task.strip():
            stats.print_metric(task)
