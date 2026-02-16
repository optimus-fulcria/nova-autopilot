"""
Tests for Nova AutoPilot
"""

import pytest
from nova_autopilot import AutoPilot, TaskResult, ExtractResult


class TestTaskResult:
    """Tests for TaskResult model."""

    def test_creation(self):
        result = TaskResult(success=True, data={"key": "value"})
        assert result.success is True
        assert result.data == {"key": "value"}
        assert result.error is None
        assert result.started_at is not None

    def test_failed_result(self):
        result = TaskResult(success=False, error="Something went wrong")
        assert result.success is False
        assert result.error == "Something went wrong"


class TestExtractResult:
    """Tests for ExtractResult model."""

    def test_creation(self):
        result = ExtractResult(
            success=True,
            data={"items": [1, 2, 3]},
            source_url="https://example.com"
        )
        assert result.success is True
        assert len(result.data["items"]) == 3
        assert result.source_url == "https://example.com"


class TestAutoPilot:
    """Tests for AutoPilot agent."""

    def test_initialization(self):
        pilot = AutoPilot()
        assert pilot.headless is True
        assert pilot.timeout == 60
        assert pilot.max_retries == 3

    def test_custom_config(self):
        pilot = AutoPilot(
            headless=False,
            timeout=30,
            max_retries=5
        )
        assert pilot.headless is False
        assert pilot.timeout == 30
        assert pilot.max_retries == 5

    def test_mock_execution(self):
        """Test execution in mock mode (no Nova SDK)."""
        pilot = AutoPilot()
        pilot._nova_class = None  # Force mock mode

        result = pilot.execute("Test task")

        assert isinstance(result, TaskResult)
        assert result.success is True
        assert result.data is not None

    def test_mock_extraction(self):
        """Test extraction in mock mode."""
        pilot = AutoPilot()
        pilot._nova_class = None

        result = pilot.extract(
            "Extract test data",
            starting_url="https://example.com"
        )

        assert isinstance(result, ExtractResult)
        assert result.source_url == "https://example.com"

    def test_chain_execution(self):
        """Test chained task execution."""
        pilot = AutoPilot()
        pilot._nova_class = None

        tasks = ["Task 1", "Task 2", "Task 3"]
        result = pilot.chain(tasks)

        assert result.tasks_completed == 3
        assert result.tasks_failed == 0
        assert result.all_succeeded is True


class TestTaskPlanning:
    """Tests for task planning with Bedrock."""

    def test_plan_without_bedrock(self):
        """Test planning when Bedrock is unavailable."""
        pilot = AutoPilot()

        plan = pilot._plan_task("Navigate to example.com")

        assert plan.task == "Navigate to example.com"
        assert len(plan.steps) > 0
        assert plan.estimated_duration > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
