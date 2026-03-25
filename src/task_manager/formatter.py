"""Rich terminal output for the task manager."""

from rich.console import Console
from rich.table import Table
from rich import box

from task_manager.models import Task

console = Console()

PRIORITY_COLORS = {
    "high": "red",
    "medium": "yellow",
    "low": "green",
}

STATUS_COLORS = {
    "pending": "white",
    "done": "dim",
}


def print_task_table(tasks: list[Task]) -> None:
    if not tasks:
        console.print("[dim]No tasks found.[/dim]")
        return

    table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim", width=4, justify="right")
    table.add_column("Title", min_width=20)
    table.add_column("Priority", width=10)
    table.add_column("Status", width=10)
    table.add_column("Created", width=20)

    for task in tasks:
        priority_color = PRIORITY_COLORS.get(task.priority, "white")
        status_color = STATUS_COLORS.get(task.status, "white")
        title_style = "dim" if task.is_done() else "white"

        table.add_row(
            str(task.id),
            f"[{title_style}]{task.title}[/{title_style}]",
            f"[{priority_color}]{task.priority}[/{priority_color}]",
            f"[{status_color}]{task.status}[/{status_color}]",
            task.created_at or "",
        )

    console.print(table)


def print_stats(stats: dict) -> None:
    console.print("\n[bold cyan]Task Statistics[/bold cyan]")
    console.print(f"  Total:    [bold]{stats['total']}[/bold]")
    console.print(f"  Pending:  [yellow]{stats['pending']}[/yellow]")
    console.print(f"  Done:     [green]{stats['done']}[/green]")

    if stats["by_priority"]:
        console.print("\n[bold]By Priority:[/bold]")
        for priority in ("high", "medium", "low"):
            count = stats["by_priority"].get(priority, 0)
            color = PRIORITY_COLORS.get(priority, "white")
            console.print(f"  [{color}]{priority:8}[/{color}]  {count}")
    console.print()


def print_success(message: str) -> None:
    console.print(f"[bold green]✓[/bold green] {message}")


def print_error(message: str) -> None:
    console.print(f"[bold red]✗[/bold red] {message}")
