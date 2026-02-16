"""
Data models for Nova AutoPilot
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime


@dataclass
class TaskResult:
    """Result of a task execution."""
    success: bool
    data: Any = None
    error: Optional[str] = None
    screenshots: list[bytes] = field(default_factory=list)
    steps_taken: list[str] = field(default_factory=list)
    execution_time: float = 0.0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        if self.started_at is None:
            self.started_at = datetime.utcnow()


@dataclass
class ExtractResult:
    """Result of a data extraction task."""
    success: bool
    data: dict | list = field(default_factory=dict)
    source_url: Optional[str] = None
    extraction_time: float = 0.0
    schema_validated: bool = False
    error: Optional[str] = None


@dataclass
class ChainResult:
    """Result of chained task execution."""
    success: bool
    results: list[TaskResult] = field(default_factory=list)
    total_execution_time: float = 0.0
    tasks_completed: int = 0
    tasks_failed: int = 0

    @property
    def all_succeeded(self) -> bool:
        return self.tasks_failed == 0 and self.tasks_completed > 0


@dataclass
class ActionStep:
    """A single action step in task execution."""
    action: str
    target: Optional[str] = None
    value: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    success: bool = True
    screenshot: Optional[bytes] = None


@dataclass
class TaskPlan:
    """Planned steps for task execution."""
    task: str
    steps: list[ActionStep] = field(default_factory=list)
    estimated_duration: float = 0.0
    requires_auth: bool = False
    human_review_needed: bool = False
