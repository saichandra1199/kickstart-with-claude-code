"""CLI entry point for the task manager."""

import argparse
import sys

from task_manager import database as db
from task_manager.formatter import print_error, print_success, print_stats, print_task_table
from task_manager.models import VALID_PRIORITIES


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="task_manager",
        description="Smart Task Manager — a CLI task manager backed by SQLite",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument(
        "--priority",
        choices=VALID_PRIORITIES,
        default="medium",
        help="Task priority (default: medium)",
    )

    # list
    subparsers.add_parser("list", help="List all tasks")

    # complete
    complete_parser = subparsers.add_parser("complete", help="Mark a task as done")
    complete_parser.add_argument("id", type=int, help="Task ID")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    # stats
    subparsers.add_parser("stats", help="Show task statistics")

    return parser


def cmd_add(args: argparse.Namespace) -> None:
    task = db.add_task(args.title, args.priority)
    print_success(f"Added task #{task.id}: {task.title!r} [{task.priority}]")


def cmd_list(args: argparse.Namespace) -> None:
    tasks = db.list_tasks()
    print_task_table(tasks)


def cmd_complete(args: argparse.Namespace) -> None:
    task = db.complete_task(args.id)
    if task is None:
        print_error(f"Task #{args.id} not found.")
        sys.exit(1)
    print_success(f"Completed task #{task.id}: {task.title!r}")


def cmd_delete(args: argparse.Namespace) -> None:
    deleted = db.delete_task(args.id)
    if not deleted:
        print_error(f"Task #{args.id} not found.")
        sys.exit(1)
    print_success(f"Deleted task #{args.id}.")


def cmd_stats(args: argparse.Namespace) -> None:
    stats = db.get_stats()
    print_stats(stats)


COMMAND_HANDLERS = {
    "add": cmd_add,
    "list": cmd_list,
    "complete": cmd_complete,
    "delete": cmd_delete,
    "stats": cmd_stats,
}


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    handler = COMMAND_HANDLERS.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()
        sys.exit(1)
