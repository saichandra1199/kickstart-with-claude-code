# Add Task Skill

Add a new task to the task manager and show the updated task list.

## Arguments

`$ARGUMENTS` — format: `<title> [priority]`

- `title` (required): The task description (quote if it contains spaces)
- `priority` (optional): `high`, `medium`, or `low` (default: `medium`)

## Steps

1. Parse `$ARGUMENTS` to extract title and optional priority
   - If priority is not provided, use `medium`
   - Valid priorities: `high`, `medium`, `low`
2. Run: `python -m task_manager add "<title>" --priority <priority>`
3. Run: `python -m task_manager list`
4. Report the new task ID and confirm it was added

## Example Usage

```
/add-task "Buy groceries" high
/add-task "Write tests"
/add-task "Deploy to production" low
```

## Error Handling

- If priority is invalid, default to `medium` and note the correction
- If no title is provided, ask the user for one before proceeding
