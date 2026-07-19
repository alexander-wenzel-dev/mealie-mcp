---
paths:
  - "tests/live/**"
---

# Live test rubric

## Sentinel staging

Live tests use `mealie_client` and `sentinel_name` from `tests/live/conftest.py`. Each test creates a sentinel resource named with `sentinel_name`, exercises the tool, asserts on observable effects, then deletes the sentinel. Read-only tools follow the same shape: create, read, assert the sentinel appears, delete.

For nested resources (e.g. comments on a recipe), stage the parent sentinel first, then the child under it. Cleanup deletes the child before the parent so the parent delete does not orphan.

Every persisted free-text label or note field (title, description, note, content, etc.) derives from `sentinel_name`, not a hardcoded literal, regardless of how many sentinels the test stages. The cleanup may key on `id`, but two overlapping runs must never write the same literal value into the operator's Mealie, and a single-sentinel test collides just as a multi-sentinel one does. Structural fields like dates, enum slots, and foreign-key ids do not need to derive from `sentinel_name`; they identify the entry, not the run that wrote it.

Staging may call the generated client directly when no tool covers the setup an assertion needs, for example creating a second household or a multi-purpose label. The sentinel and cleanup rules apply the same way. A raw `sync_detailed` used to seed or stage in the test body must not discard its response: route it through `expect_dict` (or the matching `expect_*`) with no `suppress`, so a failed setup fails the test loudly instead of seeding nothing and leaving the assertion to fail for the wrong reason. A call whose parsed body the setup actually consumes, assigned to a variable or unwrapped through `decode`, is already covered, since a failed setup surfaces when the value is used. The `suppress` form is for cleanup in `finally` only (see Cleanup hygiene).

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

## Docstring claims and default-seeded arguments

The clobber rule is one case of a wider discipline. Every claim a wrapper docstring makes that a caller can observe must have a live assertion that would fail if the claim were false: a required id on a field, a field preserved across an update, or a value seeded when an argument is omitted. A behavioural suite that never reads the docstring is blind to a false claim, so the test is what pins the prose to live behaviour. Adding a tool means covering its claims and its defaults this way, not only its happy path.

Assert the effect the claim promises. `update_recipe` asserts both that an id-bearing tag lands and that a name-and-slug-only tag is rejected, matching the docstring that says the id is required. A default-seeded argument is set to a non-default value with an observable assertion, or deferred with a recorded reason, as Behavioural assertions above requires; `create_label` asserts an omitted color stores Mealie's `#959595`.

When live behaviour contradicts the docstring, the docstring is what is wrong: correct it to match a live call, then assert the corrected claim.

## Cleanup hygiene

Cleanup runs in a `pytest` fixture finalizer or a `try`/`finally` block, so it executes when the test body fails.

Cleanup calls in `finally` blocks suppress their own exceptions, e.g. `with contextlib.suppress(ToolError): recipe_crud.delete_recipe(...)`. `contextlib` is stdlib; `ToolError` is `fastmcp.exceptions.ToolError`. A raised cleanup error masks the real test failure with a misleading traceback.

A raw `sync_detailed` cleanup does not raise on a non-2xx status; the generated client returns the error response rather than raising, so a bare `sync_detailed(...)` in `finally` ignores whether the delete succeeded and `contextlib.suppress(httpx.HTTPError)` around it suppresses nothing. Route the raw call through `expect_dict` (or the matching `expect_*`) so a failed cleanup surfaces, and wrap that in `contextlib.suppress(ToolError)` so it still cannot mask a body failure: `with contextlib.suppress(ToolError): expect_dict("delete_household", delete_one_...sync_detailed(...))`.

For a lookup that must find an item, prefer `next((... for ... in ...), None)` with a following `assert ... is not None, f"<explanatory message>"` over a bare `next(...)`. If the lookup ever misses, the assertion names the missing item; a bare `next()` instead raises `StopIteration`, a confusing error that hides what was not found.

After any live-test failure, the operator confirms no `mcp-test-` data remains and deletes it before the next run. Tests should not rely on prior-run residue.

## Coverage per tool

Every new tool ships with at least one live test. A diff that adds a tool without a live test is a deviation.

## Wrapper round-trip per group

A direct call to a typed function skips the `@mcp.tool()` wrapper, so a wrapper that forwards an argument to the wrong parameter or mis-serializes its result ships untested. Every tool group's wrapper is exercised by one `call_tool` round-trip on an in-memory `Client(mcp)` that asserts a persisted or returned value matches a named input. The `call_tool` fixture in `conftest.py` drives it. Groups whose create takes only a name share one parametrized test in `test_mcp_protocol.py`; groups with several arguments or a parent to stage carry their round-trip in their own live file, next to their staging. The recipe group is covered by the anchor round-trips in `test_mcp_protocol.py`.

## No silencing

A failing live test is never marked `xfail` or skipped to ship. Fix the tool, fix the test, or descope and surface the decision.
