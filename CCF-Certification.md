# Claude Code Foundations (CCF) — Complete Certification Study Guide

> **Status of the exam:** As of March 2026, Anthropic has not yet published a formal CCF exam. What *does* exist is the **"Claude Code in Action"** course on [Anthropic Academy](https://anthropic.skilljar.com) that awards a completion certificate. This guide covers every testable concept drawn directly from the official Claude Code documentation so that you can score 100% on any assessment — current or future.
>
> **Official resources:**
> - Docs: <https://docs.anthropic.com/en/docs/claude-code/overview>
> - Academy: <https://anthropic.skilljar.com>
> - CLI reference: `claude --help`

---

## Table of Contents

**Part 1 — Claude Code CLI**
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

**Part 2 — Architect: API & System Design**
21. [Models Overview](#21-models-overview)
22. [Messages API Reference](#22-messages-api-reference)
23. [Tool Use](#23-tool-use)
24. [Extended Thinking](#24-extended-thinking)
25. [Prompt Engineering](#25-prompt-engineering)
26. [Computer Use](#26-computer-use)
27. [Agentic System Design](#27-agentic-system-design)
28. [Rate Limits](#28-rate-limits)
29. [AI Safety & Constitutional AI](#29-ai-safety--constitutional-ai)
30. [Architect Exam: Additional Gotchas](#30-architect-exam-additional-gotchas)
31. [Practice Questions — Architect Level](#31-practice-questions--architect-level)

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

---

# Part 2 — Claude Certified Architect: API & System Design

> This section covers the topics most likely tested in an **architect-level** certification: the Anthropic API, model selection, prompt engineering, tool use, extended thinking, agentic system design, rate limits, and AI safety.

---

## 21. Models Overview

### Current Models (as of March 2026)

| Model | API ID | Context Window | Max Output | Best For |
|---|---|---|---|---|
| **Claude Opus 4.6** | `claude-opus-4-6` | 1M tokens | 128k tokens | Complex reasoning, long-horizon agents |
| **Claude Sonnet 4.6** | `claude-sonnet-4-6` | 1M tokens | 64k tokens | Production workloads, balanced speed/intelligence |
| **Claude Haiku 4.5** | `claude-haiku-4-5-20251001` | 200k tokens | 64k tokens | High-volume, low-latency, cost-sensitive |

### Pricing (per million tokens)

| Model | Input | Output |
|---|---|---|
| Opus 4.6 | $5 | $25 |
| Sonnet 4.6 | $3 | $15 |
| Haiku 4.5 | $1 | $5 |

### Capability Flags

| Feature | Opus 4.6 | Sonnet 4.6 | Haiku 4.5 |
|---|---|---|---|
| Extended thinking (adaptive) | Yes | Yes | No |
| Extended thinking (manual) | Deprecated | Yes | Yes |
| Interleaved thinking | Yes (auto) | Yes (beta header) | No |
| 1M token context (native) | Yes | Yes | No |
| Computer use | Yes | Yes | Yes |

### 1M Context on Older Models

Sonnet 4.5 and Sonnet 4 can use 1M context with:
- Beta header: `context-1m-2025-08-07`
- Requires Tier 4 org

All other older models are hard-capped at 200k tokens.

### Deprecated Models

| Model | Retirement date |
|---|---|
| Claude Haiku 3 (`claude-3-haiku-20240307`) | **April 19, 2026** |

Use the Models API (`GET /v1/models`) to query available models and their `max_input_tokens`, `max_tokens`, and `capabilities` programmatically.

---

## 22. Messages API Reference

### Endpoint

```
POST https://api.anthropic.com/v1/messages
```

### Required Headers

```
x-api-key: $ANTHROPIC_API_KEY
anthropic-version: 2023-06-01
content-type: application/json
```

### Required Parameters

| Parameter | Type | Description |
|---|---|---|
| `model` | string | Model ID (e.g., `claude-sonnet-4-6`) |
| `max_tokens` | integer | Max tokens to generate. **No default — always required.** |
| `messages` | array | `[{"role": "user"|"assistant", "content": "..."}]` |

### Key Optional Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `system` | string or array | — | System prompt |
| `temperature` | float | 1.0 | Randomness: 0.0 (deterministic) → 1.0 (creative) |
| `top_p` | float | — | Nucleus sampling |
| `stop_sequences` | array | — | Custom stop strings |
| `stream` | boolean | false | Enable SSE streaming |
| `tools` | array | — | Tool definitions |
| `tool_choice` | object | `{"type": "auto"}` | Tool invocation strategy |
| `thinking` | object | — | Extended thinking config |
| `metadata` | object | — | e.g., `{"user_id": "abc"}` |
| `service_tier` | string | `"auto"` | `"auto"` or `"standard_only"` |

### Response Structure

```json
{
  "id": "msg_...",
  "type": "message",
  "role": "assistant",
  "content": [...content blocks...],
  "model": "claude-sonnet-4-6",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 100,
    "output_tokens": 50,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0
  }
}
```

### Stop Reasons

| Value | Meaning |
|---|---|
| `end_turn` | Model completed naturally |
| `max_tokens` | Hit `max_tokens` limit |
| `stop_sequence` | Hit a custom stop string |
| `tool_use` | Model invoked a client tool — **you must continue the loop** |
| `pause_turn` | Server-side tool loop limit hit (default 10) — **continue, do not discard** |

### Prompt Caching

Mark content blocks as cacheable:
```json
{"type": "text", "text": "...", "cache_control": {"type": "ephemeral", "ttl": "5m"}}
```

- Default TTL: `5m`. Use `1h` for long extended-thinking sessions.
- **`cache_read_input_tokens` do NOT count toward ITPM rate limits** on most models.
- Total actual input = `input_tokens` + `cache_creation_input_tokens` + `cache_read_input_tokens`
- `input_tokens` in the usage field = only tokens **after** the last cache breakpoint (not total)

---

## 23. Tool Use

### Three Categories of Tools

| Category | Who executes | Example |
|---|---|---|
| **Custom (client) tools** | You | Database lookup, file write |
| **Anthropic-defined client tools** | You (schema from Anthropic) | Computer use, text editor |
| **Server tools** | Anthropic's servers | Web search, code execution |

### Custom Tool Definition

```json
{
  "name": "get_weather",
  "description": "Get current weather for a location",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {"type": "string", "description": "City and state, e.g. Austin, TX"},
      "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
    },
    "required": ["location"]
  }
}
```

Add `"strict": true` inside `input_schema` to enable Structured Outputs (guaranteed schema conformance).

### `tool_choice` Options

```json
{"type": "auto"}                          // Claude decides (default)
{"type": "any"}                           // Must call at least one tool
{"type": "none"}                          // Must not call any tool
{"type": "tool", "name": "get_weather"}   // Force specific tool
{"type": "auto", "disable_parallel_tool_use": true}  // Disable parallel calls
```

> **Gotcha:** Extended thinking only supports `tool_choice: "auto"` or `"none"`. You cannot use `"any"` or `"tool"` with thinking enabled.

### Client Tool Use Workflow

```
1. Send: tools + messages → Claude
2. Receive: stop_reason="tool_use", content contains tool_use block
   {"type": "tool_use", "id": "toolu_...", "name": "get_weather", "input": {"location": "Austin, TX"}}
3. Execute the tool in your system
4. Send back: tool_result block as new user message
   {"type": "tool_result", "tool_use_id": "toolu_...", "content": "72°F, sunny"}
5. Claude produces final response
```

### Built-in Server Tools (versioned)

| Tool | Latest Version String |
|---|---|
| Web search | `web_search_20260209` |
| Web fetch | `web_fetch_20260309` |
| Code execution | `code_execution_20260120` |
| Bash | `bash_20250124` |
| Text editor | `text_editor_20250728` |
| Memory | `memory_20250818` |

Server tools run automatically in a loop (max 10 iterations). Returns `pause_turn` at limit.

### MCP ↔ API Schema Difference

MCP uses `inputSchema` (camelCase); Claude API uses `input_schema` (snake_case). **Rename the field** when converting MCP tool definitions to API format.

---

## 24. Extended Thinking

Extended thinking lets Claude reason through a problem internally before answering. Thinking tokens are **billed as output tokens**.

### When to Use

**Good fit:** complex math, multi-step logic, code debugging, research synthesis, strategic planning.

**Poor fit:** simple queries, latency-sensitive apps, strict cost budgets.

### Configuration

**Adaptive thinking** (recommended for Claude 4.6 models):
```json
{
  "thinking": {"type": "adaptive"},
  "output_config": {"effort": "high"}
}
```
Effort values: `"low"` | `"medium"` | `"high"` | `"max"`

**Manual thinking** (explicit token budget):
```json
{
  "thinking": {
    "type": "enabled",
    "budget_tokens": 10000,
    "display": "summarized"
  }
}
```

`display` options:
- `"summarized"` — returns summary text; full tokens still billed (default on Claude 4+)
- `"omitted"` — returns empty thinking field + signature; reduces streaming latency

### Rules for `budget_tokens`
- Must be `>= 1024`
- Must be `< max_tokens` (exception: interleaved thinking)
- Changing `budget_tokens` **invalidates the message cache** for that conversation

### Model Support

| Model | Thinking Mode |
|---|---|
| Opus 4.6 | Adaptive only (manual `"enabled"` deprecated) |
| Sonnet 4.6 | Both adaptive and manual; supports interleaved |
| Opus 4.5, 4.1, 4.0 | Manual; supports interleaved |
| Sonnet 4.5, 4.0 | Manual; supports interleaved |
| Haiku 4.5 | Manual only |
| Sonnet 3.7 | Manual; returns **full** thinking (not summarized) |

### Interleaved Thinking

Claude thinks between tool calls for more sophisticated agentic reasoning.
- Opus 4.6: automatic with adaptive thinking
- Sonnet 4.6 + Claude 4 models: requires beta header `interleaved-thinking-2025-05-14`

### Critical Multi-Turn Rule

When returning tool results in a conversation that uses thinking:
- The thinking block from the tool-use step **must be passed back unmodified**
- The API verifies the `signature` cryptographically — modification causes an error
- After the full tool-use cycle completes, you may drop previous thinking blocks

### Context Window Impact

Previous thinking blocks are **automatically stripped** from context calculation by the API in subsequent turns — you are not charged for them again.

---

## 25. Prompt Engineering

### Core Principles

**Be direct and specific**
- State exactly what you want; Claude won't assume unstated requirements
- Use numbered steps or bullets when order/completeness matters
- Explain *why* rules exist — Claude generalizes better from reasoning than bare rules

**Structure with XML tags**
```xml
<instructions>Your task is to summarize the document below.</instructions>
<document>{{document_content}}</document>
<format>Return a 3-bullet summary.</format>
```

Common tags: `<instructions>`, `<context>`, `<example>`, `<examples>`, `<input>`, `<document index="N">`, `<thinking>`, `<answer>`

**Few-shot / Multishot prompting**
- 3–5 examples is the recommended range
- Wrap examples in `<example>` tags to separate from instructions
- Make examples diverse (cover edge cases) and representative of real inputs

### Long-Context Best Practices (20k+ tokens)

- Put long documents **at the top** of the prompt, before instructions and query (can improve quality by ~30%)
- Use structured document wrappers:
  ```xml
  <document index="1">
    <source>quarterly-report.pdf</source>
    <document_content>{{content}}</document_content>
  </document>
  ```
- Ask Claude to quote relevant sections before answering

### Output Format Control

- Tell Claude what to do: "Write in flowing prose paragraphs" — not "Do not use bullets"
- Remove markdown from your prompt if you don't want markdown in the output
- Specify format with XML tags: "Write each section inside `<section>` tags"
- Opus 4.6 defaults to LaTeX for math — add "format math in plain text" to override

### System Prompts

- Assign a role: "You are a senior Python engineer reviewing a pull request."
- Set global behavior, formatting preferences, domain restrictions
- Operators can use system prompts to expand or restrict Claude's defaults within Anthropic policy

### Chain-of-Thought

- For extended thinking disabled: use `<thinking>` / `<answer>` tag pattern
- Multishot examples with `<thinking>` blocks teach Claude the desired reasoning style
- Ask for self-verification: "Before finishing, double-check your answer against [criteria]"

> **Gotcha:** Avoid the word "think" on Claude Opus 4.5 with thinking disabled — it can trigger unintended reasoning behavior. Use "consider," "evaluate," or "reason through" instead.

### Prefill Deprecation (Claude 4.6+)

Claude 4.6+ models do not support prefilled assistant turns. Migration paths:

| Old pattern | New approach |
|---|---|
| Prefill for output format | Use Structured Outputs or explicit format instructions |
| Prefill to skip preamble | System prompt: "Respond directly without preamble" |
| Prefill to continue response | User turn: "Your response was interrupted. Continue from where you left off." |

### Parallel Tool Calling

Include this in your system prompt to maximize Claude 4.6 parallelism:
```
If you intend to call multiple tools and there are no dependencies between the
calls, make all of the independent tool calls in a single response.
```

---

## 26. Computer Use

Computer use is a **beta feature** that lets Claude see a desktop (via screenshots) and control it with mouse/keyboard actions.

### Beta Headers

| Models | Beta Header |
|---|---|
| Opus 4.6, Sonnet 4.6, Opus 4.5 | `computer-use-2025-11-24` |
| All other supported models | `computer-use-2025-01-24` |

### Tool Versions

| Models | Tool Type String |
|---|---|
| Opus 4.6, Sonnet 4.6, Opus 4.5 | `computer_20251124` |
| All other supported models | `computer_20250124` |

> **Gotcha:** Tool versions are NOT backwards-compatible across model generations. Always use the version matching your model group.

### Tool Definition

```json
{
  "type": "computer_20251124",
  "name": "computer",
  "display_width_px": 1024,
  "display_height_px": 768,
  "display_number": 1
}
```

Companion tools typically included:
- `{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}`
- `{"type": "bash_20250124", "name": "bash"}`

### Available Actions

| Action | Versions | Notes |
|---|---|---|
| `screenshot` | All | Capture display |
| `left_click`, `type`, `key`, `mouse_move` | All | Basic interaction |
| `scroll`, `right_click`, `double_click`, `drag` | `20250124`+ | Enhanced interaction |
| `zoom` | `20251124` only | Inspect region at full resolution; requires `"enable_zoom": true` |

### Security Rules

1. Run in a **dedicated VM or container** with minimal privileges
2. Do not provide sensitive credentials unless necessary
3. Limit network access to an allowlist
4. Require human confirmation before consequential actions (payments, form submissions, etc.)
5. **Prompt injection risk:** Claude can be manipulated by instructions visible on screen — use isolation and Anthropic's classifiers but understand they are not perfect
6. Computer use is **not eligible for Zero Data Retention (ZDR)**

### Agent Loop Pattern

```python
while True and iterations < MAX_ITERATIONS:  # Always set a max!
    response = client.beta.messages.create(...)
    messages.append({"role": "assistant", "content": response.content})
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            result = execute_tool(block.name, block.input)
            tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})
    if not tool_results:
        break  # Done
    messages.append({"role": "user", "content": tool_results})
```

---

## 27. Agentic System Design

### Orchestrator / Subagent Pattern

```
Orchestrator (Claude)
├── Delegates task A → Subagent or tool
├── Delegates task B → Subagent or tool
└── Integrates results → final output
```

Claude 4.6+ models natively recognize when to delegate without explicit instructions.

### When to Use Subagents vs. Tools

| Scenario | Use |
|---|---|
| Independent parallel workstreams | Subagents |
| Tasks needing isolated context | Subagents |
| Simple deterministic actions | Tools |
| External API calls | Tools |
| Large file processing | Subagents |
| Sequential steps with shared state | Single context + tools |

### Long-Horizon State Management

For multi-session or multi-context tasks:

```
├── tests.json          # Structured test tracker
├── progress.txt        # Freeform notes on what's done / next steps
├── init.sh             # Setup script to restore state in a fresh session
└── git log             # Audit trail of completed work
```

Start a fresh context window with:
```
"Call pwd; review progress.txt, tests.json, and recent git log."
```

### Anti-Patterns to Avoid

| Anti-pattern | Fix |
|---|---|
| Claude hardcodes values to pass tests | Prompt: "Write general solutions, not hardcoded ones" |
| Claude over-engineers with unused abstractions | Prompt: "Only add complexity that is directly required" |
| Runaway agent loop (no termination) | Always set `max_turns` or `max_iterations` |
| Destructive action without confirmation | Prompt: "Confirm before destructive or shared-system operations" |
| Hallucinating code content | Prompt: "Never speculate about code. Read the file first." |

### Reversibility Heuristic

```
Freely take:       Local, reversible actions (edit file, run test)
Confirm before:    Destructive, shared-system, or hard-to-reverse actions
                   (git push --force, delete DB, send external message)
```

---

## 28. Rate Limits

### Limit Types

1. **RPM** — Requests per minute
2. **ITPM** — Input tokens per minute
3. **OTPM** — Output tokens per minute
4. **Spend limits** — Monthly maximum cost per org

Rate limits use the **token bucket algorithm** (continuous replenishment, not fixed interval reset).

### Tier System

| Tier | Cumulative Credit Required | Monthly Spend Limit |
|---|---|---|
| Tier 1 | $5 | $100 |
| Tier 2 | $40 | $500 |
| Tier 3 | $200 | $1,000 |
| Tier 4 | $400 | $200,000 |
| Monthly Invoicing | Negotiated | No limit |

### Rate Limits by Tier (Opus/Sonnet 4.x)

| Tier | RPM | ITPM | OTPM |
|---|---|---|---|
| Tier 1 | 50 | 30,000 | 8,000 |
| Tier 2 | 1,000 | 450,000 | 90,000 |
| Tier 3 | 2,000 | 800,000 | 160,000 |
| Tier 4 | 4,000 | 2,000,000 | 400,000 |

> **Important:** Opus 4.x limits are shared across Opus 4.6, 4.5, 4.1, and 4.0. Sonnet 4.x limits are shared across Sonnet 4.6, 4.5, and 4.0.

### Cache + ITPM Interaction

On most models, **`cache_read_input_tokens` do not count toward ITPM**. Only:
- `input_tokens` (tokens after last cache breakpoint)
- `cache_creation_input_tokens`

...count against the ITPM limit. This can dramatically multiply your effective throughput.

### Handling 429 Errors

```
HTTP 429 — rate limit exceeded
```

Response headers to read:

| Header | Description |
|---|---|
| `retry-after` | Seconds to wait before retrying |
| `anthropic-ratelimit-requests-remaining` | RPM remaining |
| `anthropic-ratelimit-input-tokens-remaining` | ITPM remaining (rounded to nearest 1k) |
| `anthropic-ratelimit-tokens-reset` | When limit replenishes (RFC 3339) |

> **Gotcha:** If usage ramps up sharply, you can hit 429 even before reaching the stated limit due to **acceleration rate limits**. Ramp up gradually.

### Message Batches API

For large-scale async processing (up to 100,000 requests per batch):

| Tier | RPM | Max in-queue | Max per batch |
|---|---|---|---|
| Tier 1 | 50 | 100,000 | 100,000 |
| Tier 4 | 4,000 | 500,000 | 100,000 |

---

## 29. AI Safety & Constitutional AI

### Constitutional AI (CAI)

Anthropic's training methodology for building safe models without large-scale human labeling of harmful outputs.

**Phase 1 — Supervised Learning:**
- Model generates responses to potentially harmful prompts
- Model self-critiques those responses against a written "constitution" (a set of principles)
- Model produces revised, improved responses
- This creates a training dataset of (bad → better) pairs

**Phase 2 — RLAIF (Reinforcement Learning from AI Feedback):**
- A preference model is trained from AI-generated comparisons (not human annotators)
- The preference model is used as a reward signal for RL training
- Result: model that is "harmless but non-evasive" — engages with difficult questions substantively

**Key result:** CAI produces models that refuse genuinely harmful requests while still being helpful on complex or sensitive topics, without the binary "refuse everything risky" failure mode.

### RLHF vs. RLAIF

| | RLHF | RLAIF |
|---|---|---|
| Feedback source | Human annotators | AI model (Claude itself) |
| Cost | High (human labor) | Lower |
| Scalability | Limited by human bandwidth | Scales with compute |
| Pioneer | OpenAI (InstructGPT) | Anthropic (CAI) |

### Hardcoded vs. Softcoded Behaviors

| Type | Description | Examples |
|---|---|---|
| **Hardcoded** | Absolute limits; cannot be changed by any operator or user instruction | CBRN weapons assistance, CSAM, undermining AI oversight |
| **Softcoded** | Defaults that operators/users can adjust within policy | Safe messaging guidelines (operators can turn off for medical providers), adult content (operators can enable on appropriate platforms) |

### Priority Hierarchy

```
1. Broadly safe          (supporting human oversight of AI)
2. Broadly ethical       (honest, non-deceptive, non-manipulative)
3. Adherent to Anthropic principles
4. Genuinely helpful
```

When these conflict, the higher priority wins.

### Responsible Scaling Policy (RSP)

Anthropic's internal framework for governing development and deployment of increasingly capable AI:
- Sets **AI Safety Levels (ASLs)** with required safety measures for each level
- Research and deployment decisions are gated on meeting the requirements for the current ASL
- Publicly committed policy — Anthropic holds itself accountable to it

### Practical API Implications

- There is no content filter toggle in the API — behavior is governed by Claude's trained dispositions and the system prompt
- Operators can expand or restrict Claude's defaults using the system prompt within Anthropic's usage policy
- Users can further adjust within the bounds operators allow
- Prompt injection in tool use and computer use contexts is a real risk — mitigate with sandboxing and isolation

---

## 30. Architect Exam: Additional Gotchas

| Trap | Correct Answer |
|---|---|
| `max_tokens` has a default | **No default** — it is always required |
| Thinking blocks can be modified when sending back tool results | **No** — they must be passed back unmodified; the signature is cryptographically verified |
| Changing `budget_tokens` keeps the message cache valid | **No** — it invalidates the message cache |
| `cache_read_input_tokens` count toward ITPM | **No** — on most models they do not count |
| `sse` is the recommended MCP transport for remote servers | **No** — `sse` is deprecated; use `http` (streamable-http) |
| `pause_turn` means the task is done | **No** — it means the server-side tool loop hit its limit; continue the conversation |
| Computer use is eligible for Zero Data Retention | **No** — explicitly not eligible for ZDR |
| `tool_choice: "any"` works with extended thinking | **No** — only `"auto"` and `"none"` are compatible with thinking |
| `input_tokens` in usage = total input sent | **No** — it's only tokens after the last cache breakpoint |
| Sonnet 4.6 thinking defaults to full output | **No** — Claude 4+ models return *summarized* thinking; Sonnet 3.7 returns full thinking |
| Opus 4.6 supports manual `budget_tokens` thinking | **No** — manual `"enabled"` is deprecated on Opus 4.6; use `"adaptive"` |

---

## 31. Practice Questions — Architect Level

---

**Q16.** A request to Claude Sonnet 4.6 returns `stop_reason: "tool_use"`. What must you do next?

<details>
<summary>Answer</summary>

Execute the tool(s) specified in the `tool_use` content block(s), then send a new `user` message containing `tool_result` block(s) with the results. The conversation is not complete — `tool_use` always requires a continuation step.

</details>

---

**Q17.** You're building a chatbot and want to cache a large system prompt to save costs. A user session has 10 turns. In which turn does the cache get created, and in which turns is it read?

<details>
<summary>Answer</summary>

The cache is **created in turn 1** (when the cacheable block is first sent with `cache_control`). It is **read in turns 2–10**, saving input token costs for each subsequent turn. `cache_creation_input_tokens` appear only in turn 1; `cache_read_input_tokens` appear in turns 2–10.

</details>

---

**Q18.** You want Claude Opus 4.6 to use extended thinking with maximum effort. What is the correct API configuration?

<details>
<summary>Answer</summary>

```json
{
  "thinking": {"type": "adaptive"},
  "output_config": {"effort": "max"}
}
```

Manual `"enabled"` thinking is deprecated on Opus 4.6. Use `"adaptive"` with `effort: "max"`.

</details>

---

**Q19.** Your application uses extended thinking and tool use together. After Claude calls a tool, you return the `tool_result`. What do you do with the thinking block from Claude's previous response?

<details>
<summary>Answer</summary>

**Pass it back unmodified.** The thinking block contains a cryptographic `signature` that the API verifies. If you modify or omit the thinking block when returning tool results, the API returns an error.

</details>

---

**Q20.** What is the ITPM rate limit for Claude Sonnet 4.6 at Tier 2, and how does prompt caching affect your effective throughput?

<details>
<summary>Answer</summary>

Tier 2 ITPM limit for Sonnet 4.x is **450,000 tokens/minute**. However, `cache_read_input_tokens` do **not** count toward ITPM on most models. If 80% of your input is cached, your effective throughput is approximately **2.25M tokens/minute** (450k / 0.2 = 2.25M total tokens delivered per minute).

</details>

---

**Q21.** An operator wants to enable adult content on their platform using Claude. How do they do this?

<details>
<summary>Answer</summary>

Via the **system prompt**. The operator writes system prompt instructions that grant permission for adult content within Anthropic's usage policy. There is no API toggle — Claude's behavior is governed by trained dispositions + system prompt context.

</details>

---

**Q22.** You're converting an MCP tool definition to the Claude API format. The MCP definition has an `inputSchema` field. What change is required?

<details>
<summary>Answer</summary>

Rename `inputSchema` (camelCase) to `input_schema` (snake_case). The Claude API uses snake_case for this field; MCP uses camelCase. No other structural changes are required.

</details>

---

**Q23.** What is the difference between RLHF and RLAIF, and which does Anthropic use in Constitutional AI?

<details>
<summary>Answer</summary>

- **RLHF:** Human annotators label preferred outputs; used to train a reward model for RL.
- **RLAIF:** AI generates the preference labels instead of humans; scales better and reduces cost.

Anthropic's Constitutional AI uses **RLAIF** in Phase 2 — the AI itself generates preference comparisons, which are then used as a reward signal for RL training.

</details>

---

**Q24.** A Tier 1 developer sends a burst of 60 requests in one minute to Claude Opus 4.6. What happens?

<details>
<summary>Answer</summary>

They exceed the **Tier 1 RPM limit of 50 requests/minute**. They will receive HTTP **429** responses for the excess requests. The response includes a `retry-after` header indicating how long to wait. Additionally, a sudden sharp ramp-up may trigger acceleration rate limits even before reaching the stated RPM ceiling.

</details>

---

## Updated Resources

| Resource | URL |
|---|---|
| Official Claude Code Docs | <https://docs.anthropic.com/en/docs/claude-code/overview> |
| Claude API Docs | <https://docs.anthropic.com/en/api/messages> |
| Models Overview | <https://docs.anthropic.com/en/docs/about-claude/models/overview> |
| Prompt Engineering Guide | <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview> |
| Tool Use Guide | <https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview> |
| Extended Thinking | <https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking> |
| Rate Limits | <https://docs.anthropic.com/en/api/rate-limits> |
| Anthropic Academy | <https://anthropic.skilljar.com> |
| Constitutional AI Paper | <https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback> |
| Settings Schema | `"$schema": "https://json.schemastore.org/claude-code-settings.json"` |

---

*Overall study priority: **Hooks + Settings + MCP + Subagents** (Claude Code sections) and **Tool Use + Extended Thinking + Rate Limits + Prompt Engineering** (Architect sections). The [Gotchas section](#19-common-exam-traps--gotchas) and [Architect Gotchas](#30-architect-exam-additional-gotchas) are the highest-density review material.*
