"""
Nova AutoPilot - Autonomous Web Task Agent powered by Amazon Nova Act

An intelligent agent that handles complex web-based tasks using natural language.
"""

from .autopilot import AutoPilot
from .models import TaskResult, ExtractResult, ChainResult

__version__ = "0.1.0"
__all__ = ["AutoPilot", "TaskResult", "ExtractResult", "ChainResult"]
