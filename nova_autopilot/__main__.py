"""
Nova AutoPilot CLI

Usage:
    python -m nova_autopilot "your task description"
    python -m nova_autopilot --interactive
    python -m nova_autopilot --url "https://example.com" "task"
"""

import sys
import typer
from rich.console import Console
from rich.table import Table

from .autopilot import AutoPilot

app = typer.Typer(
    name="nova-autopilot",
    help="Autonomous Web Task Agent powered by Amazon Nova Act"
)
console = Console()


@app.command()
def main(
    task: str = typer.Argument(None, help="Task to execute"),
    url: str = typer.Option(None, "--url", "-u", help="Starting URL"),
    interactive: bool = typer.Option(
        False, "--interactive", "-i", help="Interactive mode"
    ),
    headless: bool = typer.Option(
        True, "--headless/--no-headless", help="Run browser headless"
    ),
    timeout: int = typer.Option(60, "--timeout", "-t", help="Action timeout"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """
    Execute web automation tasks using natural language.

    Examples:
        nova-autopilot "Search for AI news on Google"
        nova-autopilot --url "https://example.com" "Click the login button"
        nova-autopilot --interactive
    """
    pilot = AutoPilot(headless=headless, timeout=timeout)

    if interactive:
        pilot.interactive(starting_url=url)
        return

    if not task:
        console.print("[red]Error:[/red] No task provided. Use --interactive or provide a task.")
        console.print("\nUsage: nova-autopilot \"your task description\"")
        console.print("       nova-autopilot --interactive")
        raise typer.Exit(1)

    console.print(f"\n[bold blue]Nova AutoPilot[/bold blue]")
    console.print(f"[dim]Task: {task}[/dim]")
    if url:
        console.print(f"[dim]URL: {url}[/dim]")
    console.print()

    with console.status("[bold green]Executing task...[/bold green]"):
        result = pilot.execute(task, starting_url=url)

    if result.success:
        console.print("[green]✓ Task completed successfully[/green]\n")

        if result.data:
            console.print("[bold]Result:[/bold]")
            console.print(result.data)

        if verbose:
            table = Table(title="Execution Details")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            table.add_row("Execution Time", f"{result.execution_time:.2f}s")
            table.add_row("Steps Taken", str(len(result.steps_taken)))
            table.add_row("Screenshots", str(len(result.screenshots)))
            console.print(table)
    else:
        console.print("[red]✗ Task failed[/red]")
        if result.error:
            console.print(f"[red]Error: {result.error}[/red]")
        raise typer.Exit(1)


@app.command()
def extract(
    task: str = typer.Argument(..., help="What to extract"),
    url: str = typer.Option(..., "--url", "-u", help="URL to extract from"),
    output: str = typer.Option(None, "--output", "-o", help="Output file (JSON)"),
):
    """
    Extract structured data from a webpage.

    Example:
        nova-autopilot extract "product names and prices" --url "https://example.com/shop"
    """
    pilot = AutoPilot()

    console.print(f"\n[bold blue]Nova AutoPilot - Extract[/bold blue]")
    console.print(f"[dim]Target: {task}[/dim]")
    console.print(f"[dim]URL: {url}[/dim]\n")

    with console.status("[bold green]Extracting data...[/bold green]"):
        result = pilot.extract(task, starting_url=url)

    if result.success:
        console.print("[green]✓ Extraction successful[/green]\n")
        console.print(result.data)

        if output:
            import json
            with open(output, "w") as f:
                json.dump(result.data, f, indent=2)
            console.print(f"\n[dim]Saved to {output}[/dim]")
    else:
        console.print(f"[red]✗ Extraction failed: {result.error}[/red]")
        raise typer.Exit(1)


@app.command()
def chain(
    tasks: list[str] = typer.Argument(..., help="Tasks to execute in sequence"),
    url: str = typer.Option(None, "--url", "-u", help="Starting URL"),
):
    """
    Execute multiple tasks in sequence.

    Example:
        nova-autopilot chain "Login" "Go to dashboard" "Click settings"
    """
    pilot = AutoPilot()

    console.print(f"\n[bold blue]Nova AutoPilot - Chain[/bold blue]")
    for i, task in enumerate(tasks, 1):
        console.print(f"[dim]{i}. {task}[/dim]")
    console.print()

    with console.status("[bold green]Executing chain...[/bold green]"):
        result = pilot.chain(tasks, starting_url=url)

    if result.success:
        console.print(f"[green]✓ All {result.tasks_completed} tasks completed[/green]")
    else:
        console.print(
            f"[yellow]⚠ {result.tasks_completed} completed, "
            f"{result.tasks_failed} failed[/yellow]"
        )
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
