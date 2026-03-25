# Smart Task Manager — Claude Code Demo Project

This project is a Python CLI task manager backed by SQLite. It is designed to demonstrate every major Claude Code feature in a single, working codebase.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the CLI
python -m task_manager add "Buy groceries" --priority high
python -m task_manager list
python -m task_manager complete 1
python -m task_manager delete 1
python -m task_manager stats

# Run tests
pytest tests/ -v
```

## Directory Structure

```
claude-basics/
├── CLAUDE.md                         # Feature 1: Project rules (this file)
├── .mcp.json                         # Feature 5: MCP SQLite server
├── .claude/
│   ├── settings.local.json           # Features 4 & 6: Hooks + permissions
│   ├── agents/task-analyzer.md       # Feature 3: Subagent for task analysis
│   └── skills/
│       ├── add-task/SKILL.md         # Feature 2: /add-task slash command
│       ├── show-stats/SKILL.md       # Feature 2: /show-stats slash command
│       └── run-tests/SKILL.md        # Feature 2: /run-tests slash command
├── src/task_manager/
│   ├── __init__.py
│   ├── __main__.py                   # Enables python -m task_manager
│   ├── cli.py                        # argparse entry point
│   ├── database.py                   # SQLite CRUD operations
│   ├── models.py                     # Task dataclass
│   └── formatter.py                  # Rich terminal output
├── tests/
│   ├── test_models.py
│   └── test_database.py
├── requirements.txt
└── pyproject.toml
```

## SQLite Schema

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    priority TEXT DEFAULT 'medium',   -- low, medium, high
    status TEXT DEFAULT 'pending',    -- pending, done
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    completed_at TEXT
);
```

Database file: `./tasks.db` (created on first run).

## Python Conventions

- Type hints on all function signatures
- PEP 8 style (enforced by ruff, line-length 88)
- `rich` library for all terminal output (no raw `print`)
- No ORM — raw `sqlite3` with `Row` factory for dict-like access
- `src/` layout: source lives in `src/task_manager/`, not project root

## Key Design Decisions

**`db_path` parameter pattern** — Every database function accepts `db_path: str = DEFAULT_DB_PATH`. Tests pass `tmp_path / "test.db"` (a real temp file) instead of `":memory:"` because SQLite `:memory:` databases are wiped when the connection closes (which happens inside `with sqlite3.connect(...)` context managers).

**`__main__.py`** — `python -m task_manager` requires a `__main__.py` file in the package. Without it Python raises `No module named task_manager.__main__; 'task_manager' is a package and cannot be directly executed`.

**`pythonpath = ["src"]` in pyproject.toml** — Without this, all pytest runs fail with `ModuleNotFoundError: No module named 'task_manager'` because pytest does not add `src/` to `sys.path` automatically.

---

## Claude Code Features Explained

### Feature 1 — CLAUDE.md (this file)

**What it is:** A markdown file at the project root that Claude reads automatically at the start of every session — no explicit instruction needed.

**Why it exists:** Gives Claude persistent project context (commands, conventions, architecture) without consuming conversation turns. Think of it as the project's README written for Claude specifically.

**Where it lives:** `CLAUDE.md` at the repository root (or any parent directory up to `~`).

---

### Feature 2 — Skills (Slash Commands)

**What they are:** Reusable prompt templates stored as `SKILL.md` files. Invoked with `/skill-name [args]` in the Claude Code chat.

**Why they exist:** Encode repetitive workflows once so you never have to type the same multi-step instructions again.

**Where they live:** `.claude/skills/<skill-name>/SKILL.md`

**Skills in this project:**
- `/add-task <title> [priority]` — adds a task and lists all tasks
- `/show-stats` — shows stats and task list
- `/run-tests` — runs pytest with full output

---

### Feature 3 — Agents (Subagents)

**What they are:** Specialized AI assistants with their own system prompt, model, and tool restrictions. Claude can spawn them automatically when a task matches their description.

**Why they exist:** Separate concerns — the main Claude handles conversation while a subagent focuses on a narrow, well-defined task (here: analyzing task patterns from the database).

**Where they live:** `.claude/agents/<agent-name>.md`

**Agent in this project:** `task-analyzer` — queries `tasks.db`, computes metrics, and returns a structured markdown report.

---

### Feature 4 — Hooks

**What they are:** Shell commands that run automatically when Claude Code events occur (tool calls, session start/stop, etc.).

**Why they exist:** Automate quality gates without manual intervention. The linting hook ensures Python files are always ruff-clean after Claude edits them.

**Where they live:** `hooks` section of `.claude/settings.local.json`

**Hooks in this project:**
- `PostToolUse` on `Write` and `Edit` → runs `uvx ruff check --fix src/`
- `Stop` → prints a reminder to run `python -m task_manager list`

---

### Feature 5 — MCP (Model Context Protocol)

**What it is:** A standard protocol that connects Claude to external tools and data sources. The SQLite MCP server lets Claude run SQL queries against `tasks.db` directly.

**Why it exists:** Claude can answer questions like "how many tasks by priority?" without writing Python code — it queries the database natively through the MCP tool.

**Where it lives:** `.mcp.json` at the project root

**MCP server in this project:** `mcp-server-sqlite` — run via `uvx`, connects to `./tasks.db`.

---

### Feature 6 — Settings & Permissions

**What they are:** `settings.local.json` controls which shell commands Claude can run without prompting the user for approval.

**Why they exist:** Reduce friction for trusted, project-specific commands while maintaining security for everything else.

**Where they live:** `.claude/settings.local.json` (project-level, not committed to git by default)

**Pre-approved commands:** `python*`, `python3*`, `uvx ruff*`, `pytest*`, `pip*`

---

### Feature 7 — Memory

**What it is:** Claude automatically writes notes about the project, user preferences, and decisions to `.claude/memory/` across sessions.

**Why it exists:** Persistent context that survives conversation resets. Claude can recall previous decisions, user preferences, and project-specific patterns without being re-told.

**Where it lives:** `.claude/memory/` (auto-managed by Claude, no setup needed)

**Usage:** After working in this project, check `.claude/memory/` to see what Claude has learned and remembered.
