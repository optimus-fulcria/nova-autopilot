"""
Nova AutoPilot - Core Agent Implementation

Uses Amazon Nova Act for browser automation and Amazon Bedrock for reasoning.
"""

import os
import time
import json
import logging
from typing import Any, Optional
from datetime import datetime
from contextlib import contextmanager

from dotenv import load_dotenv

from .models import TaskResult, ExtractResult, ChainResult, TaskPlan, ActionStep

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AutoPilot:
    """
    Autonomous Web Task Agent powered by Amazon Nova Act.

    Handles complex web-based tasks using natural language instructions.
    """

    def __init__(
        self,
        headless: bool = True,
        timeout: int = 60,
        max_retries: int = 3,
        region: str = None,
        model_id: str = None
    ):
        """
        Initialize the AutoPilot agent.

        Args:
            headless: Run browser in headless mode
            timeout: Maximum time per action in seconds
            max_retries: Number of retry attempts for failed actions
            region: AWS region for Bedrock
            model_id: Bedrock model ID for task planning
        """
        self.headless = headless
        self.timeout = timeout
        self.max_retries = max_retries
        self.region = region or os.getenv("AWS_REGION", "us-east-1")
        self.model_id = model_id or os.getenv(
            "NOVA_BEDROCK_MODEL", "amazon.nova-pro-v1:0"
        )

        self._nova = None
        self._bedrock = None
        self._session_active = False

    def _init_nova(self):
        """Initialize Nova Act SDK."""
        try:
            from nova_act import NovaAct
            self._nova_class = NovaAct
            logger.info("Nova Act SDK initialized")
        except ImportError:
            logger.warning("Nova Act SDK not installed, using mock mode")
            self._nova_class = None

    def _init_bedrock(self):
        """Initialize Amazon Bedrock client."""
        try:
            import boto3
            self._bedrock = boto3.client(
                "bedrock-runtime",
                region_name=self.region
            )
            logger.info(f"Bedrock client initialized in {self.region}")
        except Exception as e:
            logger.warning(f"Bedrock initialization failed: {e}")
            self._bedrock = None

    @contextmanager
    def _browser_session(self, starting_url: str = None):
        """Context manager for browser sessions."""
        if self._nova_class is None:
            self._init_nova()

        if self._nova_class:
            nova = self._nova_class(
                starting_page=starting_url or "about:blank",
                headless=self.headless,
                timeout=self.timeout
            )
            try:
                nova.start()
                self._session_active = True
                yield nova
            finally:
                nova.stop()
                self._session_active = False
        else:
            # Mock mode for testing without Nova Act
            yield MockNovaSession(starting_url)

    def _plan_task(self, task: str) -> TaskPlan:
        """
        Use Bedrock to plan task execution.

        Args:
            task: Natural language task description

        Returns:
            TaskPlan with steps to execute
        """
        if self._bedrock is None:
            self._init_bedrock()

        if self._bedrock is None:
            # Return simple plan without Bedrock
            return TaskPlan(
                task=task,
                steps=[ActionStep(action="execute", value=task)],
                estimated_duration=30.0
            )

        try:
            # Use Nova Pro for task planning
            prompt = f"""Analyze this web automation task and create an execution plan.

Task: {task}

Return a JSON object with:
- steps: array of action objects (action, target, value)
- estimated_duration: seconds
- requires_auth: boolean
- human_review_needed: boolean

Be specific about selectors and actions. Keep steps atomic."""

            response = self._bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1000,
                    "temperature": 0.3
                })
            )

            result = json.loads(response["body"].read())
            plan_data = json.loads(result["content"][0]["text"])

            steps = [
                ActionStep(
                    action=s.get("action", ""),
                    target=s.get("target"),
                    value=s.get("value")
                )
                for s in plan_data.get("steps", [])
            ]

            return TaskPlan(
                task=task,
                steps=steps,
                estimated_duration=plan_data.get("estimated_duration", 30.0),
                requires_auth=plan_data.get("requires_auth", False),
                human_review_needed=plan_data.get("human_review_needed", False)
            )

        except Exception as e:
            logger.warning(f"Task planning failed: {e}")
            return TaskPlan(
                task=task,
                steps=[ActionStep(action="execute", value=task)],
                estimated_duration=30.0
            )

    def execute(
        self,
        task: str,
        starting_url: str = None,
        capture_screenshots: bool = True
    ) -> TaskResult:
        """
        Execute a web automation task.

        Args:
            task: Natural language description of the task
            starting_url: Initial URL to navigate to
            capture_screenshots: Whether to capture screenshots

        Returns:
            TaskResult with execution details
        """
        start_time = time.time()
        result = TaskResult(success=False, started_at=datetime.utcnow())

        try:
            # Plan the task
            plan = self._plan_task(task)

            if plan.human_review_needed:
                logger.warning("Task may require human review")

            with self._browser_session(starting_url) as nova:
                # Execute through Nova Act
                for attempt in range(self.max_retries):
                    try:
                        nova_result = nova.act(task)

                        result.success = True
                        result.data = nova_result
                        result.steps_taken = [
                            step.action for step in plan.steps
                        ]

                        if capture_screenshots:
                            try:
                                screenshot = nova.screenshot()
                                if screenshot:
                                    result.screenshots.append(screenshot)
                            except Exception:
                                pass

                        break

                    except Exception as e:
                        logger.warning(f"Attempt {attempt + 1} failed: {e}")
                        if attempt == self.max_retries - 1:
                            result.error = str(e)

        except Exception as e:
            result.error = str(e)
            logger.error(f"Task execution failed: {e}")

        result.execution_time = time.time() - start_time
        result.completed_at = datetime.utcnow()

        return result

    def extract(
        self,
        task: str,
        starting_url: str = None,
        schema: dict = None
    ) -> ExtractResult:
        """
        Extract structured data from a webpage.

        Args:
            task: What data to extract
            starting_url: URL to extract from
            schema: Optional JSON schema for validation

        Returns:
            ExtractResult with extracted data
        """
        start_time = time.time()
        result = ExtractResult(success=False, source_url=starting_url)

        try:
            with self._browser_session(starting_url) as nova:
                # Use act_get for structured extraction
                if hasattr(nova, "act_get"):
                    data = nova.act_get(task)
                else:
                    # Fallback to regular act with JSON instruction
                    raw = nova.act(f"{task}. Return the result as JSON.")
                    data = json.loads(raw) if isinstance(raw, str) else raw

                result.data = data
                result.success = True

                # Validate against schema if provided
                if schema:
                    try:
                        from jsonschema import validate
                        validate(instance=data, schema=schema)
                        result.schema_validated = True
                    except Exception as e:
                        logger.warning(f"Schema validation failed: {e}")
                        result.schema_validated = False

        except Exception as e:
            result.error = str(e)
            logger.error(f"Extraction failed: {e}")

        result.extraction_time = time.time() - start_time
        return result

    def chain(
        self,
        tasks: list[str],
        starting_url: str = None,
        stop_on_failure: bool = True
    ) -> ChainResult:
        """
        Execute a chain of tasks in sequence.

        Args:
            tasks: List of task descriptions
            starting_url: Initial URL
            stop_on_failure: Stop chain if any task fails

        Returns:
            ChainResult with all task results
        """
        start_time = time.time()
        result = ChainResult(success=True)

        current_url = starting_url

        for task in tasks:
            task_result = self.execute(task, starting_url=current_url)
            result.results.append(task_result)

            if task_result.success:
                result.tasks_completed += 1
            else:
                result.tasks_failed += 1
                result.success = False
                if stop_on_failure:
                    break

        result.total_execution_time = time.time() - start_time
        return result

    def interactive(self, starting_url: str = None):
        """
        Start an interactive session for manual task execution.

        Args:
            starting_url: Initial URL to navigate to
        """
        from rich.console import Console
        from rich.prompt import Prompt

        console = Console()

        console.print("\n[bold blue]Nova AutoPilot Interactive Mode[/bold blue]")
        console.print("Type tasks in natural language. Type 'quit' to exit.\n")

        with self._browser_session(starting_url) as nova:
            while True:
                try:
                    task = Prompt.ask("[green]Task[/green]")

                    if task.lower() in ("quit", "exit", "q"):
                        break

                    if task.lower() == "screenshot":
                        screenshot = nova.screenshot()
                        console.print("[yellow]Screenshot captured[/yellow]")
                        continue

                    console.print(f"[dim]Executing: {task}[/dim]")
                    result = nova.act(task)
                    console.print(f"[green]Result:[/green] {result}")

                except KeyboardInterrupt:
                    break
                except Exception as e:
                    console.print(f"[red]Error:[/red] {e}")

        console.print("\n[blue]Session ended[/blue]")


class MockNovaSession:
    """Mock Nova session for testing without SDK."""

    def __init__(self, starting_url: str = None):
        self.url = starting_url
        logger.info("Running in mock mode (Nova Act SDK not available)")

    def start(self):
        pass

    def stop(self):
        pass

    def act(self, task: str) -> dict:
        logger.info(f"Mock executing: {task}")
        return {"status": "mock", "task": task}

    def act_get(self, task: str) -> dict:
        return {"data": [], "status": "mock"}

    def screenshot(self) -> bytes:
        return b""

    def navigate(self, url: str):
        self.url = url
