# Kickstart with Claude Code

A Python CLI task manager backed by SQLite, built to demonstrate every major [Claude Code](https://claude.ai/claude-code) feature in a single working project.

## Features Demonstrated

| Feature | Where |
|---|---|
| **CLAUDE.md** — project rules Claude reads automatically | `CLAUDE.md` |
| **Skills** — custom slash commands | `.claude/skills/*/SKILL.md` |
| **Agents** — specialized subagents | `.claude/agents/task-analyzer.md` |
| **Hooks** — auto-lint on file edits | `.claude/settings.local.json` |
| **MCP** — Claude queries SQLite directly | `.mcp.json` |
| **Settings & Permissions** — pre-approve CLI commands | `.claude/settings.local.json` |
| **Memory** — persistent notes across sessions | `.claude/memory/` (auto-managed) |

## Requirements

- Python 3.11+
- [pip](https://pip.pypa.io/)
- [uvx](https://docs.astral.sh/uv/) (for hooks and MCP server)

## Installation

```bash
git clone https://github.com/saichandra1199/kickstart-with-claude-code.git
cd kickstart-with-claude-code
pip install -r requirements.txt
pip install -e .
```

## Running the CLI

```bash
# Add tasks
python -m task_manager add "Buy groceries" --priority high
python -m task_manager add "Write tests" --priority medium
python -m task_manager add "Deploy to prod" --priority low

# List all tasks
python -m task_manager list

# Mark a task complete
python -m task_manager complete 1

# Delete a task
python -m task_manager delete 2

# Show statistics
python -m task_manager stats
```

## Running the Tests

```bash
pytest tests/ -v
```

All 15 tests should pass:
- `tests/test_models.py` — 5 tests (Task dataclass, defaults, methods)
- `tests/test_database.py` — 10 tests (CRUD operations with real temp SQLite file)

## Using Claude Code Features

Open this project in Claude Code (`claude` in the project root) and try:

```
# Skills (slash commands)
/add-task "Learn Claude Code" high
/show-stats
/run-tests

# Agent
analyze my task patterns

# MCP (requires uvx + mcp-server-sqlite)
how many tasks do I have by priority?
```

The `CLAUDE.md` file explains every feature in detail — Claude reads it automatically at session start.

## Project Structure

```
├── CLAUDE.md                         # Claude Code project rules
├── .mcp.json                         # MCP SQLite server config
├── .claude/
│   ├── settings.local.json           # Hooks and permissions
│   ├── agents/task-analyzer.md       # Task analysis subagent
│   └── skills/
│       ├── add-task/SKILL.md
│       ├── show-stats/SKILL.md
│       └── run-tests/SKILL.md
├── src/task_manager/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── database.py
│   ├── models.py
│   └── formatter.py
├── tests/
│   ├── test_models.py
│   └── test_database.py
├── requirements.txt
└── pyproject.toml
```
