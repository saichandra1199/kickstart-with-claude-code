# Claude Code Foundations (CCF) — Complete Certification Study Guide

> **Status of the exam:** As of March 2026, Anthropic has not yet published a formal CCF exam. What *does* exist is the **"Claude Code in Action"** course on [Anthropic Academy](https://anthropic.skilljar.com) that awards a completion certificate. This guide covers every testable concept drawn directly from the official Claude Code documentation so that you can score 100% on any assessment — current or future.
>
> **Official resources:**
> - Docs: <https://docs.anthropic.com/en/docs/claude-code/overview>
> - Academy: <https://anthropic.skilljar.com>
> - CLI reference: `claude --help`

---

## Table of Contents

1. [What is Claude Code?](#1-what-is-claude-code)
2. [Installation & Surfaces](#2-installation--surfaces)
3. [CLI Reference](#3-cli-reference)
4. [CLAUDE.md — Project Memory](#4-claudemd--project-memory)
5. [Settings & Configuration](#5-settings--configuration)
6. [Permissions & Security](#6-permissions--security)
7. [Hooks — Lifecycle Automation](#7-hooks--lifecycle-automation)
8. [MCP — Model Context Protocol](#8-mcp--model-context-protocol)
9. [Memory System](#9-memory-system)
10. [Skills (Slash Commands)](#10-skills-slash-commands)
11. [Sub-Agents](#11-sub-agents)
12. [Agent Teams](#12-agent-teams)
13. [Context Management](#13-context-management)
14. [Worktrees](#14-worktrees)
15. [Headless / Automation Mode](#15-headless--automation-mode)
16. [IDE Integrations](#16-ide-integrations)
17. [Built-in Slash Commands](#17-built-in-slash-commands)
18. [Quick-Reference Cheat Sheet](#18-quick-reference-cheat-sheet)
19. [Common Exam Traps & Gotchas](#19-common-exam-traps--gotchas)
20. [Practice Questions](#20-practice-questions)

---

## 1. What is Claude Code?

Claude Code is an **agentic coding tool** built by Anthropic. It operates as an interactive agent that can:

- Read files, edit code, run shell commands
- Create git commits and pull requests
- Connect to external tools via MCP servers
- Spawn specialized subagents
- Run headlessly in CI/CD pipelines
- Schedule recurring tasks

**Core philosophy:** Unix-composable — pipeable, scriptable, chainable with other tools.

### The Agentic Loop

```
User prompt → Claude reads context → Plans actions → Executes tools → Reports results → Repeats
```

Claude operates in a loop, using tools (Read, Write, Edit, Bash, Glob, Grep, WebFetch, etc.) until the task is complete or it needs user input.

---

## 2. Installation & Surfaces

### Installation Methods

| Method | Command | Auto-updates? |
|---|---|---|
| Native (recommended) | `curl -fsSL https://claude.ai/install.sh \| bash` (macOS/Linux/WSL) | Yes |
| Windows PowerShell | `irm https://claude.ai/install.ps1 \| iex` | Yes |
| Homebrew | `brew install --cask claude-code` | No (`brew upgrade`) |
| WinGet | `winget install Anthropic.ClaudeCode` | No |

### Surfaces / Where You Can Use Claude Code

| Surface | Key features |
|---|---|
| **Terminal CLI** | Full-featured, composable, pipe/script support |
| **VS Code / Cursor** | Inline diffs, `@`-mentions, plan review, conversation history |
| **JetBrains** | Interactive diff viewing, selection context sharing |
| **Desktop app** | Visual diffs, multiple sessions side-by-side, scheduled tasks |
| **Web** (`claude.ai/code`) | No local setup; long-running tasks; works from browser and iOS |

### Session Portability

| Command | Effect |
|---|---|
| `/teleport` | Move web session to terminal |
| `/desktop` | Move terminal session to desktop app |
| Remote Control | Control terminal Claude Code from any browser |

---

## 3. CLI Reference

### Starting a Session

```bash
claude                          # Start interactive session
claude "fix the tests"          # Start with initial prompt
claude -p "fix the tests"       # Non-interactive (headless) mode
claude --resume                 # Resume last session
claude --resume <session-id>    # Resume specific session
claude --continue               # Continue most recent conversation
```

### Key Flags

| Flag | Effect |
|---|---|
| `-p`, `--print` | Non-interactive mode; print response and exit |
| `--output-format` | `text` (default), `json`, `stream-json` |
| `--model <id>` | Override model for this session |
| `--permission-mode` | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `--dangerously-skip-permissions` | Skip all permission prompts (use with caution) |
| `--add-dir <path>` | Add extra working directory |
| `--agents <json>` | Inline subagent definitions for this session |
| `--system-prompt <text>` | Override system prompt (non-interactive only) |
| `--append-system-prompt <text>` | Append to system prompt (non-interactive only) |
| `--allowedTools` | Comma-separated tools to allow (non-interactive) |
| `--disallowedTools` | Comma-separated tools to block (non-interactive) |
| `--max-turns <n>` | Maximum agentic turns before stopping |
| `--verbose` | Show full tool input/output |
| `--debug` | Debug-level logging |
| `--no-markdown` | Disable markdown rendering |

### Permission Modes

| Mode | What Claude can do |
|---|---|
| `default` | Asks before most actions |
| `acceptEdits` | Auto-approves file edits; asks for bash |
| `dontAsk` | Auto-approves most actions |
| `bypassPermissions` | Skip all checks (use only in isolated environments) |
| `plan` | Read-only research; no edits or commands |

### MCP CLI Commands

```bash
claude mcp add <name> -- <command> [args]        # Add stdio server
claude mcp add --transport http <name> <url>     # Add HTTP server
claude mcp add --scope user <name> -- <command>  # Add user-scoped server
claude mcp list                                  # List all servers
claude mcp get <name>                            # Show server details
claude mcp remove <name>                         # Remove server
claude mcp reset-project-choices                 # Reset .mcp.json approvals
```

---

## 4. CLAUDE.md — Project Memory

### What It Is

A Markdown file that Claude reads **automatically at the start of every session** — no explicit instruction needed. It provides persistent project context without consuming conversation turns.

### File Locations & Priority

| Location | Scope | When loaded |
|---|---|---|
| `~/.claude/CLAUDE.md` | Global (all projects) | Always |
| `./CLAUDE.md` | Project root | When working in that project |
| `<any-parent>/CLAUDE.md` | Parent directory | Traversed up to `~` |
| `<subdir>/CLAUDE.md` | Subdirectory | When Claude is working in that subdir |

**Important:** Claude reads ALL CLAUDE.md files from `~` down to the current directory. They are all active simultaneously.

### What to Put in CLAUDE.md

- Project overview and architecture
- Run/test/build commands (`npm test`, `make build`, etc.)
- Code conventions and style rules
- Directory structure explanation
- Key design decisions and "gotchas"
- Links to docs or specs
- Things Claude should always or never do in this project

### What NOT to Put

- Secrets or API keys
- Highly volatile information that changes daily
- Generic advice already in Claude's training

### `@import` Directive

CLAUDE.md files can import other files:

```markdown
@import ./docs/architecture.md
@import ./CONTRIBUTING.md
```

Imported files are inlined at the location of the `@import` directive.

---

## 5. Settings & Configuration

### Configuration Scopes (Highest → Lowest Priority)

| # | Scope | File location | Shared? |
|---|---|---|---|
| 1 | **Managed** (IT/MDM) | System-level; varies by OS | All users |
| 2 | **Command-line args** | Session flags | No |
| 3 | **Local** | `.claude/settings.local.json` | No (gitignored) |
| 4 | **Project** | `.claude/settings.json` | Yes (commit to git) |
| 5 | **User** | `~/.claude/settings.json` | No |

**Key rule:** Deny rules take precedence over allow rules **within the same scope**. More specific scope wins on a per-setting basis.

### File Locations Summary

| File | Purpose |
|---|---|
| `~/.claude/settings.json` | User-level settings (all your projects) |
| `.claude/settings.json` | Project settings (share with team via git) |
| `.claude/settings.local.json` | Local overrides (gitignore this) |
| `~/.claude.json` | Global config: OAuth, MCP servers, caches, per-project state |
| `.mcp.json` | Project-scoped MCP servers |

### Key Settings Fields

```jsonc
{
  // Model
  "model": "claude-sonnet-4-6",        // Override default model
  "availableModels": ["sonnet", "opus"], // Restrict model picker

  // Behavior
  "language": "japanese",              // Response language
  "autoMemoryEnabled": true,           // Auto memory on/off
  "includeGitInstructions": true,      // Include git status in system prompt
  "effortLevel": "high",               // Persist effort: low/medium/high

  // Appearance
  "prefersReducedMotion": false,
  "spinnerTipsEnabled": true,

  // Teams
  "teammateMode": "auto",              // "auto" | "in-process" | "tmux"

  // Attribution (git commits/PRs)
  "attribution": {
    "commit": "",                      // Empty string hides attribution
    "pr": ""
  },

  // Updates
  "autoUpdatesChannel": "latest",      // "latest" | "stable" (~1 week old)

  // Hooks
  "disableAllHooks": false,

  // Permissions
  "permissions": {
    "allow": ["Bash(npm run *)"],
    "deny": ["Bash(rm -rf *)"],
    "defaultMode": "default",
    "additionalDirectories": ["../shared-lib"]
  }
}
```

### Managed Settings Delivery (Enterprise)

| OS | Method | Location |
|---|---|---|
| macOS | MDM (Jamf, Kandji) | `com.anthropic.claudecode` preferences domain |
| macOS | File | `/Library/Application Support/ClaudeCode/managed-settings.json` |
| Linux/WSL | File | `/etc/claude-code/managed-settings.json` |
| Windows | Registry | `HKLM\SOFTWARE\Policies\ClaudeCode` → `Settings` (REG_SZ) |
| Windows | File | `C:\Program Files\ClaudeCode\managed-settings.json` |

> **Gotcha:** Windows legacy path `C:\ProgramData\ClaudeCode\managed-settings.json` is no longer supported as of v2.1.75.

---

## 6. Permissions & Security

### Permission Rule Syntax

```
Tool                          # All calls to this tool
Tool(specifier)               # Specific pattern for this tool
Bash(npm run *)               # Prefix wildcard (anything starting with "npm run ")
Read(./.env)                  # Exact file path
WebFetch(domain:example.com)  # Domain match
Agent(subagent-name)          # Specific subagent
Skill(deploy *)               # Skill matching prefix
```

**Evaluation order: deny first → ask → allow. First match wins.**

### Sandbox Settings

| Setting | Default | Description |
|---|---|---|
| `sandbox.enabled` | `false` | Enable bash sandboxing (macOS, Linux, WSL2) |
| `sandbox.autoAllowBashIfSandboxed` | `true` | Auto-approve bash when sandboxed |
| `sandbox.excludedCommands` | `[]` | Commands that run outside sandbox |
| `sandbox.filesystem.allowWrite` | `[]` | Additional writable paths |
| `sandbox.filesystem.denyWrite` | `[]` | Blocked write paths |
| `sandbox.network.allowedDomains` | `[]` | Allowed outbound domains (`*.example.com` wildcards) |
| `sandbox.network.allowLocalBinding` | `false` | Allow binding to localhost (macOS only) |

### Sandbox Path Prefixes

| Prefix | Resolves to |
|---|---|
| `/path` | Absolute path |
| `~/path` | Relative to home directory |
| `./path` or no prefix | Relative to project root (project settings) or `~/.claude` (user settings) |

### Auto Mode

Auto mode automatically determines permission level based on the environment (CI vs. local dev). It is configured via `permissions.autoMode` (not in project settings — only user/managed settings).

---

## 7. Hooks — Lifecycle Automation

Hooks run shell commands, HTTP requests, LLM prompts, or spawn subagents at specific lifecycle events.

### 4 Hook Handler Types

| Type | Mechanism | Blocking? |
|---|---|---|
| `command` | Shell command; receives JSON on stdin | Yes (exit 2 or JSON `continue: false`) |
| `http` | HTTP POST with JSON body | Yes (2xx + JSON decision) |
| `prompt` | Single-turn LLM evaluation; `$ARGUMENTS` placeholder | Yes (yes/no output) |
| `agent` | Spawns a subagent with tool access | Yes |

### Hook Configuration Schema

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "regex_pattern_or_object",
        "hooks": [
          {
            "type": "command",
            "command": "echo hello",
            "timeout": 600,
            "statusMessage": "Running custom check...",
            "once": false,
            "async": false
          }
        ]
      }
    ]
  }
}
```

### All 24 Lifecycle Events

**Session events:**

| Event | Matcher values | Blockable? |
|---|---|---|
| `SessionStart` | `startup`, `resume`, `clear`, `compact` | No |
| `SessionEnd` | `clear`, `resume`, `logout`, `prompt_input_exit`, etc. | No |
| `InstructionsLoaded` | `session_start`, `nested_traversal`, etc. | No |

**User interaction:**

| Event | Notes | Blockable? |
|---|---|---|
| `UserPromptSubmit` | Fires on every user message; matcher not supported | Yes |
| `Notification` | `permission_prompt`, `idle_prompt`, `auth_success` | No |

**Tool execution:**

| Event | Notes | Blockable? |
|---|---|---|
| `PreToolUse` | Runs before tool; matcher = tool name | **Yes** |
| `PermissionRequest` | Fires when permission dialog would appear | **Yes** |
| `PostToolUse` | Runs after tool completes (tool already ran) | No (feedback only) |
| `PostToolUseFailure` | Runs when a tool fails | No |

**Agent events:**

| Event | Notes | Blockable? |
|---|---|---|
| `SubagentStart` | When subagent starts | No |
| `SubagentStop` | When subagent finishes | **Yes** |
| `Stop` | When Claude finishes a response | **Yes** (makes Claude continue) |
| `StopFailure` | On error: `rate_limit`, `auth_failed`, `billing_error`, etc. | No |

**Team events:**

| Event | Blockable? |
|---|---|
| `TeammateIdle` | **Yes** |
| `TaskCompleted` | **Yes** |

**Configuration:**

| Event | Notes | Blockable? |
|---|---|---|
| `ConfigChange` | `user_settings`, `project_settings`, etc. | **Yes** (not for `policy_settings`) |
| `PreCompact` | `manual` or `auto` | No |
| `PostCompact` | `manual` or `auto` | No |

**Worktree / MCP:**

| Event | Notes | Blockable? |
|---|---|---|
| `WorktreeCreate` | Must print absolute path to stdout | Yes (non-zero exit) |
| `WorktreeRemove` | Async; failures only logged | No |
| `Elicitation` | MCP server needs user input | **Yes** |
| `ElicitationResult` | MCP server got user input | **Yes** |

### Hook Exit Codes (command type)

| Exit code | JSON parsed? | Effect |
|---|---|---|
| `0` | Yes | Proceed; apply any JSON decisions |
| `2` | No | **Blocking error**; stderr fed to Claude as error message |
| Other | No | Non-blocking error; stderr in verbose mode only |

### Hook Output JSON

```json
{
  "continue": true,
  "stopReason": "Message shown when continue=false",
  "suppressOutput": false,
  "systemMessage": "Warning injected into Claude's context"
}
```

**For `PreToolUse` — blocking a specific tool:**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "Why this decision was made",
    "updatedInput": {},
    "additionalContext": "Extra context for Claude"
  }
}
```

**For `Stop` / `SubagentStop`:**
```json
{ "decision": "block", "reason": "Why Claude should continue working" }
```

### Environment Variables in Hooks

```bash
$CLAUDE_PROJECT_DIR        # Project root directory
$CLAUDE_ENV_FILE           # SessionStart only: file for persistent env vars
${CLAUDE_PLUGIN_ROOT}      # Plugin install directory
${CLAUDE_PLUGIN_DATA}      # Plugin persistent data directory
$CLAUDE_CODE_REMOTE        # "true" if running in web session
```

**Persist environment variables across a session (SessionStart only):**
```bash
echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
```

### Settings Precedence for Hooks

1. Managed policy
2. Plugin hooks (`hooks/hooks.json`)
3. `.claude/settings.local.json`
4. `.claude/settings.json`
5. `~/.claude/settings.json`
6. Component frontmatter (skills/agents)

### Key Hook Gotchas

1. Shell profiles that print text break JSON parsing — stdout must be **only** clean JSON
2. Use exit `0` + JSON for structured control; exit `2` ignores all JSON output
3. `disableAllHooks` in user/project settings **cannot** disable managed hooks
4. `ConfigChange` cannot block `policy_settings` source changes
5. `SessionEnd` default timeout = 1.5s; override with `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS`
6. Identical handlers (same command/URL) are **deduplicated** — run only once
7. HTTP hooks never block on errors; must return 2xx + JSON to block
8. `WorktreeRemove` and `InstructionsLoaded` run **asynchronously**
9. Always quote paths: `"\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/my.sh"`
10. MCP tool naming in matchers: `mcp__<server>__<tool>` (e.g., `mcp__memory__.*`)

---

## 8. MCP — Model Context Protocol

MCP is an **open standard** for connecting AI tools to external data sources and services (Jira, Slack, Google Drive, GitHub, databases, etc.).

### Transport Types

| Transport | Status | Use case |
|---|---|---|
| `http` (streamable-http) | **Recommended** | Remote cloud services |
| `stdio` | Current | Local processes, direct system access |
| `sse` | **Deprecated** | Legacy remote services |
| `ws` | Supported | WebSocket |

### Installing MCP Servers

```bash
# HTTP (recommended for remote)
claude mcp add --transport http notion https://mcp.notion.com/mcp
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer ${TOKEN}"

# Stdio (local process)
claude mcp add my-server -- npx -y @some/mcp-package
claude mcp add --env API_KEY=mykey airtable -- npx -y airtable-mcp-server

# Windows - wrap with cmd /c
claude mcp add my-server -- cmd /c npx -y @some/package
```

> **Gotcha:** All flags (`--transport`, `--env`, `--scope`, `--header`) must come **before** the server name. `--` separates server name from its command/args.

### MCP Scopes

| Scope | Storage | Shared? |
|---|---|---|
| `local` (default) | `~/.claude.json` under project path | No |
| `project` | `.mcp.json` in project root | Yes (commit to git) |
| `user` | `~/.claude.json` global section | No (cross-project) |

**Precedence:** `local` > `project` > `user` (for same-name conflicts)

> **Gotcha:** "Local" MCP scope stores in `~/.claude.json`, NOT `.claude/settings.local.json`. These are different files.

### `.mcp.json` Format

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "./tasks.db"]
    },
    "notion": {
      "type": "http",
      "url": "${API_BASE_URL:-https://mcp.notion.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${NOTION_TOKEN}"
      }
    }
  }
}
```

**Environment variable expansion:**
- `${VAR}` — expand env var (fails if unset)
- `${VAR:-default}` — expand or use default
- Supported in: `command`, `args`, `env`, `url`, `headers`

### Important MCP Environment Variables

| Variable | Effect |
|---|---|
| `MCP_TIMEOUT` | Server startup timeout (e.g., `MCP_TIMEOUT=10000`) |
| `MAX_MCP_OUTPUT_TOKENS` | Override 10,000-token default limit (e.g., `MAX_MCP_OUTPUT_TOKENS=50000`) |

### Dynamic Tool Updates

Claude Code supports MCP `list_changed` notifications. When a server sends this, Claude Code **automatically refreshes** available tools/prompts/resources without disconnect/reconnect.

### Slash Commands in Claude Code

```
/mcp          # Show MCP server status + authenticate OAuth servers
```

---

## 9. Memory System

Claude Code has two memory mechanisms:

### Auto Memory

Claude **automatically writes notes** to `.claude/projects/<project>/memory/` (or `~/.claude/projects/.../memory/`) across sessions. No setup needed.

| Setting | Default | Description |
|---|---|---|
| `autoMemoryEnabled` | `true` | Enable/disable |
| `autoMemoryDirectory` | `~/.claude/projects/<project>/memory/` | Override location |

### CLAUDE.md (Manual Memory)

The main way to give Claude persistent context — see [Section 4](#4-claudemd--project-memory).

### Memory in Subagents

Subagents can have their own persistent memory via the `memory` frontmatter field:

| Value | Location |
|---|---|
| `user` | `~/.claude/agent-memory/<agent-name>/` |
| `project` | `.claude/agent-memory/<agent-name>/` |
| `local` | `.claude/agent-memory-local/<agent-name>/` |

When enabled: first 200 lines of `MEMORY.md` are injected into the subagent's system prompt automatically.

---

## 10. Skills (Slash Commands)

Skills are reusable prompt templates invoked with `/skill-name [args]`.

### File Structure

```
.claude/skills/
└── my-skill/
    └── SKILL.md
```

Or for user-level (all projects):
```
~/.claude/skills/
└── my-skill/
    └── SKILL.md
```

### SKILL.md Format

```markdown
---
name: my-skill              # Optional; defaults to directory name
description: What this does # Shown in skill picker
allowed-tools: Bash, Read   # Optional tool restriction
---

Your prompt template here.
Reference args with $ARGUMENTS.

Example: Run `python -m task_manager add "$ARGUMENTS"`
```

### Frontmatter Fields

| Field | Description |
|---|---|
| `name` | Skill name (defaults to directory name) |
| `description` | Shown in skill picker |
| `allowed-tools` | Comma-separated tool allowlist |
| `argument-hint` | Shown in UI when typing the command (e.g., `<title> [priority]`) |

### Scopes & Priority

| Location | Scope | Priority |
|---|---|---|
| `.claude/skills/` | Current project | 1 (highest) |
| `~/.claude/skills/` | All your projects | 2 |
| Plugin `skills/` directory | Where plugin enabled | 3 (lowest) |

### Using Skills in Hooks

Skills can have a hook with `"once": true` to run setup logic once on first use.

### Preloading Skills into Subagents

In a subagent's frontmatter:
```yaml
skills:
  - my-skill
  - another-skill
```

This injects the full skill content into the subagent's system prompt at startup.

---

## 11. Sub-Agents

Subagents are specialized AI assistants with their own context window, system prompt, tool access, model, and permissions.

### Built-in Subagents

| Agent | Model | Tools | Purpose |
|---|---|---|---|
| `Explore` | Haiku | Read-only | File discovery, code search |
| `Plan` | Inherits | Read-only | Research during plan mode |
| `general-purpose` | Inherits | All | Complex multi-step tasks |
| `statusline-setup` | Sonnet | Read, Edit | `/statusline` configuration |
| `claude-code-guide` | Haiku | Glob, Grep, Read, WebFetch, WebSearch | Answering Claude Code questions |

### Subagent File Locations & Priority

| Location | Scope | Priority |
|---|---|---|
| `--agents` CLI flag | Current session | 1 (highest) |
| `.claude/agents/` | Current project | 2 |
| `~/.claude/agents/` | All your projects | 3 |
| Plugin `agents/` directory | Where plugin enabled | 4 (lowest) |

Same name at multiple levels → higher priority wins.

### Subagent Frontmatter

```yaml
---
name: code-reviewer          # Required: lowercase, hyphens only
description: >               # Required: when Claude should spawn this agent
  Reviews code for security issues and performance.
  Use when user asks for a code review.
model: sonnet                # Optional: sonnet | opus | haiku | inherit | full ID
tools:                       # Optional: allowlist (omit = inherit all)
  - Read
  - Glob
  - Grep
disallowedTools:             # Optional: deny specific tools
  - Write
  - Edit
permissionMode: default      # Optional: default|acceptEdits|dontAsk|bypassPermissions|plan
maxTurns: 10                 # Optional: max agentic turns
isolation: worktree          # Optional: run in isolated git worktree
background: false            # Optional: always run as background task
effort: high                 # Optional: low|medium|high|max (Opus 4.6 only)
memory: project              # Optional: user|project|local
skills:                      # Optional: preload these skills
  - my-skill
mcpServers:                  # Optional: MCP servers for this agent only
  - sqlite
hooks:                       # Optional: hooks scoped to this agent
  PostToolUse: [...]
---

Your system prompt here. This replaces the default Claude Code system prompt
for this subagent.
```

### Model Aliases

| Alias | Resolves to |
|---|---|
| `sonnet` | Latest Claude Sonnet |
| `opus` | Latest Claude Opus |
| `haiku` | Latest Claude Haiku |
| `inherit` | Same as parent (default) |
| Full ID | e.g., `claude-sonnet-4-6` |

### Tool Control Rules

- `disallowedTools` is applied **first**, then `tools` resolved against remaining pool
- A tool in both lists = removed
- `Agent(worker, researcher)` in `tools` = only these subagents can be spawned
- `Agent` (no parens) = any subagent can be spawned
- Omitting `Agent` from `tools` = cannot spawn any subagents

> **Critical gotcha:** `Task` tool was renamed to `Agent` in v2.1.63. `Task(...)` still works as alias.

> **Critical gotcha:** Subagents **cannot spawn other subagents**. Only the main conversation can spawn subagents.

### Permission Inheritance

- Subagents inherit parent conversation's permission mode
- Can override via `permissionMode` in frontmatter
- Exception: if parent uses `bypassPermissions`, it takes precedence always
- Exception: if parent uses auto mode, subagent inherits auto mode; `permissionMode` is ignored

### Spawning Subagents

Claude spawns subagents automatically when the task matches a subagent's `description`. You can also explicitly ask: "Use the code-reviewer agent to review this PR."

---

## 12. Agent Teams

Agent teams are multiple Claude Code instances working in parallel, coordinated by a main orchestrator session.

### How They Work

```
Main session (orchestrator)
├── Spawns Teammate A (e.g., "write the tests")
├── Spawns Teammate B (e.g., "update the docs")
└── Waits for results → integrates output
```

Each teammate runs in its own context window. They do NOT share context directly.

### Display Modes (`teammateMode`)

| Mode | Description |
|---|---|
| `auto` | Automatically chooses based on environment |
| `in-process` | Teammates run in the same process (web/desktop) |
| `tmux` | Each teammate gets its own tmux pane (terminal) |

### Key Differences: Subagents vs Agent Teams

| | Subagents | Agent Teams |
|---|---|---|
| Scope | Single session | Multiple sessions |
| Context | Shared parent context | Separate context windows |
| Nesting | Cannot nest | Can nest teams |
| Cost | Lower (shared context) | Higher (separate contexts) |
| Use case | Focused sub-tasks | Parallel large workstreams |

---

## 13. Context Management

### Context Window

Claude Code has a finite context window. When it fills up, older content is compacted/summarized automatically.

### Compaction

- **Auto-compact:** Triggered automatically when context is near full
- **Manual:** `/compact` in the conversation
- **`/compact <instructions>`** — compact with specific focus instructions

Hooks: `PreCompact` (matcher: `manual|auto`), `PostCompact`.

### Context Commands

| Command | Effect |
|---|---|
| `/clear` | Clear conversation and start fresh |
| `/compact` | Summarize and compress conversation |
| `/context` | Show current context usage |

### Tips for Managing Context

- Use CLAUDE.md instead of re-explaining project structure each session
- Use subagents to offload large tasks (each has its own context window)
- Use `/compact <focus>` to summarize while keeping specific context
- Use worktrees for parallel workstreams (each session = independent context)

---

## 14. Worktrees

Git worktrees let you work on multiple branches simultaneously, each in its own directory and Claude Code session.

### Creating a Worktree

```
/worktree [name]   # Create isolated worktree from current branch
```

Or via subagent frontmatter:
```yaml
isolation: worktree
```

Auto-cleanup: if the agent makes no changes, the worktree is deleted automatically.

### Worktree Settings

```json
{
  "worktree": {
    "symlinkDirectories": ["node_modules", ".cache"],
    "sparsePaths": ["packages/my-app"]
  }
}
```

### Custom Worktree Hooks

```json
"WorktreeCreate": [{"hooks": [{"type": "command", "command": "echo /path/to/new/worktree"}]}],
"WorktreeRemove": [{"hooks": [{"type": "command", "command": "cleanup.sh"}]}]
```

`WorktreeCreate` hook **must** print only the absolute path to stdout.

---

## 15. Headless / Automation Mode

Run Claude Code non-interactively in scripts, CI/CD, or pipelines.

### Basic Usage

```bash
# Simple one-shot
claude -p "explain this function" --output-format text

# With specific tools
claude -p "run the tests and fix failures" \
  --allowedTools "Bash,Read,Write,Edit"

# Pipe input
cat error.log | claude -p "what is causing this error?"

# JSON output for scripting
claude -p "list all API endpoints" --output-format json

# Streaming JSON
claude -p "fix all type errors" --output-format stream-json
```

### Output Formats

| Format | Description |
|---|---|
| `text` | Plain text (default) |
| `json` | Single JSON response object |
| `stream-json` | Newline-delimited JSON events (for real-time processing) |

### Environment Variables

```bash
ANTHROPIC_API_KEY=sk-ant-...    # Required for API auth
CLAUDE_CONFIG_DIR=./config      # Override config directory
MCP_TIMEOUT=10000               # MCP server startup timeout
MAX_MCP_OUTPUT_TOKENS=50000     # Override MCP output token limit
CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS=5000  # SessionEnd hook timeout
```

### SDK / Programmatic Use

Claude Code exposes an Agent SDK for building custom agents and tools programmatically. See `claude --help` for SDK documentation entry points.

---

## 16. IDE Integrations

### VS Code / Cursor

- Install via VS Code marketplace or `claude` command auto-installs
- Inline diffs with accept/reject buttons
- `@`-mention files from the editor
- Plan mode review in sidebar
- Conversation history across sessions
- `Cmd/Ctrl+Esc` — toggle Claude Code panel

### JetBrains (IntelliJ, PyCharm, etc.)

- Interactive diff viewing
- Share selected code as context with a keyboard shortcut
- Install via JetBrains Marketplace

### `autoConnectIde` Setting

Set `autoConnectIde: true` in `~/.claude.json` to auto-connect when opening Claude Code inside an IDE terminal.

---

## 17. Built-in Slash Commands

| Command | Description |
|---|---|
| `/help` | Show help |
| `/clear` | Clear conversation |
| `/compact [instructions]` | Compress context |
| `/context` | Show context usage |
| `/cost` | Show token costs for this session |
| `/doctor` | Diagnose Claude Code setup issues |
| `/feedback` | Submit feedback to Anthropic |
| `/hooks` | View configured hooks (read-only) |
| `/ide` | Connect to IDE integration |
| `/init` | Initialize CLAUDE.md for this project |
| `/login` | Switch accounts or login methods |
| `/logout` | Log out |
| `/mcp` | MCP server status and OAuth auth |
| `/memory` | View/edit memory files |
| `/model` | Switch model for this session |
| `/permissions` | View current permission settings |
| `/pr-comments` | Load GitHub PR comments as context |
| `/reload-plugins` | Reload plugins mid-session |
| `/review` | Start code review workflow |
| `/skills` | List available skills |
| `/statusline` | Configure custom status line |
| `/terminal-setup` | Set up terminal for best experience |
| `/think` | Toggle extended thinking |
| `/vim` | Toggle vim keybindings |
| `/worktree [name]` | Create isolated git worktree |
| `/fast` | Toggle fast mode (faster output) |

---

## 18. Quick-Reference Cheat Sheet

```
CONFIGURATION HIERARCHY (highest → lowest)
  Managed (IT/MDM) > CLI args > .claude/settings.local.json > .claude/settings.json > ~/.claude/settings.json

PERMISSION RULES
  deny > ask > allow (first match wins)
  Bash(npm run *)    Read(./.env)    WebFetch(domain:*)    Agent(name)

HOOK TYPES
  command | http | prompt | agent

BLOCKABLE HOOK EVENTS
  PreToolUse, PermissionRequest, UserPromptSubmit, Stop, SubagentStop,
  TeammateIdle, TaskCompleted, ConfigChange, Elicitation, ElicitationResult

HOOK EXIT CODES
  0 = proceed    2 = blocking error fed to Claude    other = non-blocking error

MCP SCOPES (local > project > user)
  local  → ~/.claude.json (project path)
  project → .mcp.json
  user   → ~/.claude.json (global)

MCP TRANSPORT (use http for remote, stdio for local)

SUBAGENT TOOL NESTING LIMIT
  Main → Subagent (cannot spawn further subagents)

CLAUDE.MD LOADING
  All files from ~ down to current dir are loaded simultaneously

MEMORY LOCATIONS
  Auto memory:    ~/.claude/projects/<project>/memory/
  Agent memory:   .claude/agent-memory/<agent-name>/
```

---

## 19. Common Exam Traps & Gotchas

These are the questions most likely to trip you up:

### Settings & Config

- **Trap:** "Local scope" for MCP servers is `~/.claude.json`, NOT `.claude/settings.local.json`. Local MCP scope = per-project but personal, stored in home dir JSON.
- **Trap:** `settings.local.json` is gitignored by default — it's for personal local overrides, NOT shared with team.
- **Trap:** `autoMemoryDirectory` is only accepted in user settings, NOT project settings.
- **Trap:** Windows legacy managed settings path (`C:\ProgramData\...`) is deprecated since v2.1.75; use `C:\Program Files\ClaudeCode\managed-settings.json`.
- **Trap:** `autoMode` config is only in user/managed settings — NOT in `.claude/settings.json`.

### Hooks

- **Trap:** `PostToolUse` is NOT blocking — the tool has already run. Use `PreToolUse` to block.
- **Trap:** Exit code `2` ignores ALL JSON output. Use exit `0` + JSON `continue: false` for structured blocking.
- **Trap:** `SessionEnd` hooks have a **1.5-second** default timeout (much shorter than other hooks).
- **Trap:** Shell profiles that print text break JSON parsing — hooks must output **only** clean JSON to stdout.
- **Trap:** `disableAllHooks` in user/project settings **cannot** disable managed hooks.
- **Trap:** `ConfigChange` fires when settings change but CANNOT block `policy_settings` changes.
- **Trap:** HTTP hooks NEVER block on connection errors; they must return 2xx + valid JSON decision.

### MCP

- **Trap:** `sse` transport is **deprecated** — use `http` (streamable-http) for remote servers.
- **Trap:** `--transport`, `--env`, `--scope` flags must come BEFORE the server name in `claude mcp add`.
- **Trap:** The default `MAX_MCP_OUTPUT_TOKENS` limit is **10,000** tokens per tool call.

### Subagents

- **Trap:** Subagents **cannot spawn other subagents** — nesting is one level only.
- **Trap:** `Task` was renamed to `Agent` in v2.1.63 — old `Task(...)` syntax still works as alias.
- **Trap:** If parent uses `bypassPermissions`, subagent `permissionMode` frontmatter is **ignored**.
- **Trap:** If parent uses auto mode, subagent `permissionMode` frontmatter is **ignored**.
- **Trap:** `disallowedTools` is applied FIRST, then `tools` — a tool in both lists is denied.

### CLAUDE.md

- **Trap:** ALL CLAUDE.md files from `~` down to the current directory are loaded simultaneously (not just the nearest one).
- **Trap:** `@import ./file.md` inlines at the location of the directive — order matters.

### Context & Performance

- **Trap:** `autoUpdatesChannel: "stable"` means approximately **1 week old** builds, not just "stable".

---

## 20. Practice Questions

Test yourself. Answers follow each question.

---

**Q1.** You want Claude to automatically run `ruff check --fix src/` every time it edits a Python file. Which hook event should you use?

<details>
<summary>Answer</summary>

**`PostToolUse`** with `matcher: {"tool_name": "Edit"}` (and optionally `"Write"`). Note: `PostToolUse` is not blocking — but that's fine here; you just want linting to run after the edit.

</details>

---

**Q2.** A hook that runs on `PreToolUse` exits with code `2`. What happens?

<details>
<summary>Answer</summary>

The tool is **blocked**. Exit code `2` is a blocking error — stderr is fed to Claude as an error message. No JSON is parsed from stdout.

</details>

---

**Q3.** You add an MCP server with `claude mcp add myserver -- npx -y my-package`. What scope does it use?

<details>
<summary>Answer</summary>

**`local`** scope (default). It is stored in `~/.claude.json` under the current project's path — personal to you, not shared with teammates.

</details>

---

**Q4.** Your team wants to share an MCP server config via git. Where should it be defined?

<details>
<summary>Answer</summary>

In **`.mcp.json`** at the project root (project scope). This file can be committed to git and shared with all teammates.

</details>

---

**Q5.** You have a subagent with `tools: [Read, Glob, Grep]`. Can it spawn other subagents?

<details>
<summary>Answer</summary>

**No.** `Agent` is not in its tools list, so it cannot spawn subagents. Additionally, subagents fundamentally cannot spawn other subagents in Claude Code.

</details>

---

**Q6.** What is the difference between `.claude/settings.local.json` and the "local" scope for MCP servers?

<details>
<summary>Answer</summary>

They are **completely different things**:
- `.claude/settings.local.json` = project-level personal settings file (gitignored)
- MCP "local" scope = stored in `~/.claude.json` under the project's path (also personal, but in home dir)

</details>

---

**Q7.** Which settings scope has the highest priority?

<details>
<summary>Answer</summary>

**Managed** (IT/MDM-deployed) settings. Order: Managed > CLI args > local > project > user.

</details>

---

**Q8.** A `SessionEnd` hook is running a cleanup script. The script takes 3 seconds. Will it complete?

<details>
<summary>Answer</summary>

**Maybe not.** `SessionEnd` hooks have a default timeout of **1.5 seconds**. Override with `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS=5000`.

</details>

---

**Q9.** How do you make a hook run only once (e.g., first time a skill is invoked)?

<details>
<summary>Answer</summary>

Set `"once": true` in the hook definition. This is supported for skill hooks — the hook removes itself after the first run.

</details>

---

**Q10.** You want Claude to query a production database without you having to approve every SQL query. What's the minimal permission change needed?

<details>
<summary>Answer</summary>

Add a permission `allow` rule for the MCP tool pattern. For example:
```json
"allow": ["mcp__database__query"]
```
Or use `defaultMode: "dontAsk"` to skip all permission prompts (less targeted).

</details>

---

**Q11.** What is the default token limit for a single MCP tool call response?

<details>
<summary>Answer</summary>

**10,000 tokens**. Override with `MAX_MCP_OUTPUT_TOKENS` environment variable.

</details>

---

**Q12.** Your CLAUDE.md has `@import ./docs/api.md`. Where does the imported content appear?

<details>
<summary>Answer</summary>

**Inline at the location of the `@import` directive** within the CLAUDE.md file — not appended at the end.

</details>

---

**Q13.** A subagent has `permissionMode: dontAsk` in its frontmatter. The parent session is in `bypassPermissions` mode. What permission mode does the subagent actually use?

<details>
<summary>Answer</summary>

**`bypassPermissions`** — the parent's mode takes precedence and cannot be overridden by subagent frontmatter.

</details>

---

**Q14.** You want to prevent Claude from making any changes to the repository while it researches a solution. Which permission mode should you use?

<details>
<summary>Answer</summary>

**`plan` mode** — read-only; Claude can read files and run read-only tools but cannot write, edit, or run shell commands.

</details>

---

**Q15.** In a `PreToolUse` hook, you want to allow the tool to run but inject extra context for Claude. How?

<details>
<summary>Answer</summary>

Return exit code `0` with JSON including:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "additionalContext": "Remember: this file has a lock. Acquire it first."
  }
}
```

</details>

---

## Resources

| Resource | URL |
|---|---|
| Official Docs | <https://docs.anthropic.com/en/docs/claude-code/overview> |
| Anthropic Academy | <https://anthropic.skilljar.com> |
| "Claude Code in Action" course | <https://anthropic.skilljar.com> → Claude Code in Action |
| Settings schema (IDE validation) | `"$schema": "https://json.schemastore.org/claude-code-settings.json"` |
| MCP servers registry | <https://mcp.so> |
| GitHub Issues / Feedback | `claude /feedback` inside Claude Code |

---

*Study tip: The highest-value topics for any Claude Code assessment are **Hooks** (event lifecycle, blocking behavior, exit codes), **Settings** (scope precedence, file locations), **MCP** (scopes, transport types, `.mcp.json` syntax), and **Subagents** (frontmatter fields, nesting limits, permission inheritance). Focus extra time on the [Gotchas section](#19-common-exam-traps--gotchas).*
