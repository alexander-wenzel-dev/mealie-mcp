---
paths:
  - "tests/live/**"
---

# Live test rubric

## Sentinel staging

Live tests use `mealie_client` and `sentinel_name` from `tests/live/conftest.py`. Each test creates a sentinel resource named with `sentinel_name`, exercises the tool, asserts on observable effects, then deletes the sentinel. Read-only tools follow the same shape: create, read, assert the sentinel appears, delete.

For nested resources (e.g. comments on a recipe), stage the parent sentinel first, then the child under it. Cleanup deletes the child before the parent so the parent delete does not orphan.

When a test stages more than one sentinel resource, every persisted free-text label or note field (title, description, note, content, etc.) derives from `sentinel_name`, not a hardcoded literal. The cleanup may key on `id`, but two overlapping runs would still write the same literal value into the operator's Mealie. Structural fields like dates, enum slots, and foreign-key ids do not need to derive from `sentinel_name`; they identify the entry, not the run that wrote it.

## Behavioural assertions, not smoke checks

Assertions observe a behavioural difference: presence vs absence, value change, ordering shift. A seed value equal to the schema default exercises nothing. Pick seeds and assertions so a regression in the underlying bug class would fail the test, not just the literal example a rule names. "No 422" is a smoke check, not a test.

If a parameter cannot be exercised against an observable effect, it should not ship. Record the deferral and the reason in the PR Risks section or a task file.

## Body-fields PUT-replace clobber

Mealie's update endpoints PUT-replace the resource: any field absent from the request body resets to its schema default on the server. An update tool that exposes only some of its body fields is clobber-prone on the rest; the tool guards against this with fetch-then-merge (see the tool rubric), and the live test must prove the guard holds.

If an update tool's body model carries fields the tool does not expose, the live test must:

1. Set non-default values on at least two such fields before the update.
2. Run the update through the tool.
3. Fetch the resource and assert both values survived.

One-field seeding lets the bug class slip through.

## Cleanup hygiene

Cleanup runs in a `pytest` fixture finalizer or a `try`/`finally` block, so it executes when the test body fails.

Cleanup calls in `finally` blocks suppress their own exceptions, e.g. `with contextlib.suppress(ToolError): recipe_crud.delete_recipe(...)`. `contextlib` is stdlib; `ToolError` is `fastmcp.exceptions.ToolError`. A raised cleanup error masks the real test failure with a misleading traceback.

For a lookup that must find an item, prefer `next((... for ... in ...), None)` with a following `assert ... is not None, f"<explanatory message>"` over a bare `next(...)`. If the lookup ever misses, the assertion names the missing item; a bare `next()` instead raises `StopIteration`, a confusing error that hides what was not found.

After any live-test failure, the operator confirms no `mcp-test-` data remains and deletes it before the next run. Tests should not rely on prior-run residue.

## Coverage per tool

Every new tool ships with at least one unit test and at least one live test. A diff that adds a tool without a live test is a deviation.

## No silencing

A failing live test is never marked `xfail` or skipped to ship. Fix the tool, fix the test, or descope and surface the decision.
