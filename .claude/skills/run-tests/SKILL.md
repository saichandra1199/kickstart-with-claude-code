# Run Tests Skill

Run the full pytest suite and report results.

## Arguments

None required. `$ARGUMENTS` is ignored.

## Steps

1. Run: `pytest tests/ -v --tb=short`
2. Parse the output to count:
   - Total tests run
   - Passed count
   - Failed count (if any)
   - Any errors
3. Report the summary (e.g., "14/14 tests passed." or "11/14 passed, 3 failed.")
4. If there are failures, show the failure details from pytest output
5. Ask the user before attempting to auto-fix any failures: "Would you like me to investigate and fix the failing tests?"

## Example Usage

```
/run-tests
```

## Expected Output

All 14 tests should pass on a clean install:
- `tests/test_models.py` — 5 tests (Task dataclass, defaults, methods)
- `tests/test_database.py` — 9 tests (CRUD operations with real temp SQLite file)
