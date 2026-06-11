# CLAUDE.md

The durable working procedure for every agent in this repo.

## Maintaining this file

Transient content belongs in a task file under `tasks/`. Remove obsolete sections in the same commit that obsoletes them. Do not add rules any competent agent would already follow, and do not repeat a rule across sections.

## Operating contexts

This repo is worked on in two contexts: a Claude Code session (CLI or hosted worker) and the cloud agent (`.github/workflows/claude-*.yml`). Detection: if `GITHUB_ACTIONS=true` you are the cloud agent, otherwise the session. All sections below apply to both contexts unless tagged otherwise.

## Philosophy

YAGNI and KISS. Build what the task requires now. Resist abstractions, configuration, and fallbacks for cases that may never come.

## Writing style

Committed prose uses simple technical English, short sentences, and no em dashes. Code comments and docstrings describe behaviour or a non-obvious why. They do not restate durable rules from this file, name this file, or reference the current task.

Names for tests, modules, functions, and sections describe what the thing is or verifies, not the procedure or the current task's framing. A name should still read correctly when the original context is gone.

## Project

Build a Python MCP server that wraps the Mealie REST API. The server exposes Mealie operations as MCP tools.

In scope: MCP tools that call the Mealie API, a generated typed Python client from the Mealie OpenAPI spec, local tests against a live Mealie instance, and a public release on GitHub under MIT.

Out of scope: hosting or deploying Mealie itself, any web UI or non-MCP transport, and multi-instance routing. One Mealie instance per server process.

## Stack

- Python 3.14.
- `uv` for environment, dependencies, and lock file.
- `FastMCP` for the MCP server.
- `openapi-python-client` to generate the Mealie client from the OpenAPI spec.
- `httpx` as the HTTP transport.
- `python-dotenv` for `.env` loading at entry points (`server.main`, `regen-client`, and `tests/conftest.py`). Not at package import.
- `pytest` with markers for unit and live tests.
- `pytest-cov` for coverage measurement and reporting.
- `ruff` for lint and format.
- `mypy` for type checks.
- `bandit` and `pip-audit` for security scans.
- `pre-commit` for local hooks.
- GitHub Actions for CI.

## Repo layout

```
.
├── CLAUDE.md
├── README.md
├── LICENSE
├── pyproject.toml
├── uv.lock
├── .python-version
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── .github/
│   └── workflows/
│       └── ci.yml
├── spec/
│   └── mealie-openapi.json
├── src/
│   └── mealie_mcp/
│       ├── __init__.py
│       ├── server.py
│       ├── config.py
│       └── client/        # generated, not hand edited
├── tests/
│   ├── unit/
│   └── live/
└── tasks/                 # gitignored, not for public consumption
```

## Generated client

The Mealie OpenAPI spec is cached at `spec/mealie-openapi.json` and pinned by `[tool.mealie-mcp.spec]` in `pyproject.toml` (version, sha256). `uv run regen-client` uses the cache, verifies the SHA and `info.version` against the lockfile, and regenerates `src/mealie_mcp/client/`. Drift fails the run. `uv run regen-client --update` fetches `$MEALIE_BASE_URL/openapi.json`, refreshes the cache, rewrites the lockfile fields, and regenerates. The generated client folder is committed. `ruff` and `mypy` exclude it.

The generator does not runtime-validate response bodies. Its `_parse_response` functions use `cast(T, response.json())`, which is a type hint with no runtime effect. Keep explicit `isinstance` shape guards on parsed responses at the tool boundary. `openapi-python-client` is pinned via `[tool.uv.sources]` to a fork branch carrying two unmerged generator fixes (upstream PRs openapi-generators/openapi-python-client#1448 and #1449); without that pin the generator silently drops dashed-schema models (`Recipe-Input`, `Recipe-Output`, `RecipeIngredient-*`, `RecipeCommentOut-*`, `ShoppingList*`) and every endpoint that references them, including the recipe PUT and PATCH and the shopping-list write endpoints. Drop the pin and bump the floor when a release containing both lands. If the generator drops models the pin does not cover, surface it as a blocker rather than hand-writing replacements.

## Test environment

The operator owns the Mealie test instance and the `.env` file. They copy `.env.example` to `.env` and fill in real values. The agent does not provision the instance, create or edit `.env`, ask for credential values, or paste them into the conversation. Unit tests run regardless of `.env` presence.

When live tests are part of the work, the agent picks a path by precondition, in this order:

1. (cloud context) `MEALIE_BASE_URL` and `MEALIE_API_TOKEN` are already in the process environment. Run `pytest -m live` directly. Mealie is provided by the surrounding context. Do not bootstrap and do not read `.env`.
2. (session) `.env` is present. Run `pytest -m live` against the operator's pointed Mealie. Never bootstrap when `.env` is present, even if the bootstrap would also succeed; the operator's pointed target is the source of truth.
3. (session) `.env` is absent, `docker info` exits 0, and `./scripts/mealie-up` succeeds. Bootstrap Mealie exactly once per session, export the two emitted lines into the process environment (not into a `.env` file; the no-write rule still holds), run the full `pytest -m live` suite against the single persistent container, and call `docker rm -f mealie-mcp-dev` as the final step regardless of test outcome. Never tear down and re-bootstrap between test cases. First boot takes ~110-115s on a typical box (full schema, seed admin, default group and household, seed data, scheduler init); `mealie-up` uses `--rm` for clean test state, so every bootstrap pays that tax in full. If a test case needs a clean Mealie, write it with sentinel staging and teardown, not container restart.
4. (session) None of the above. Stop before live tests, run def-of-ready up to `uv run pytest`, and report that live verification is pending via the cloud agent's CI run.

The live token has admin rights, so admin-only endpoints can be exercised without conditional skips. If a live test needs to check non-admin behaviour, stage a non-admin scenario explicitly rather than gating on token capability.

## Definition of ready

A task is only ready for review when all of these commands pass.

```
uv run ruff format --check .
uv run ruff check .
uv run mypy src
uv run pytest             # branch coverage is reported, not gated
uv run pytest -m live
```

Skip these checks when the diff is Markdown only. There is no executable surface to verify.

## Independent review before PR

After the definition-of-ready checks pass and before opening the PR, spawn a fresh-eyes verification agent. Hand it the diff and a neutral brief that asks for real flaws only: logical, technical, contract-level. No hints, no leading angles, no list of suspected issues. If the agent surfaces a real flaw, fix it before opening the PR. If it returns only nits or nothing, proceed.

Skip the agent when the PR is purely a regenerated artifact tree. The diff is machine output; verification is the def-of-ready run plus a spot-check that expected outputs are present. Also skip the agent for a Markdown-only diff. No logic to review.

## Tool patterns

Each MCP tool has two layers. The first is a typed module-level function that takes an `AuthenticatedClient` and the tool inputs, validates them with the shared `require_non_empty` helper, calls the generated client's `sync_detailed` entry point (so the raw `status_code` and `content` are available for error mapping), maps non-success responses through the shared `raise_api_error` helper, decodes successful bodies with the shared `decode` helper, and returns a JSON-compatible value validated with explicit `isinstance` shape guards. This layer is the testable unit. The second is a thin `@mcp.tool()` wrapper inside a `register(mcp, get_client)` function; the wrapper calls `get_client()` (the process-scoped singleton provider from `mealie_mcp.client_factory`) and forwards to the typed function. Tool modules in `src/mealie_mcp/tools/` are auto-discovered by `register_all`; a new group is a single new file with a `register` callable.

Tool modules are grouped by Mealie OpenAPI tag, one module per group, mirroring the layout of `mealie_mcp.client.api`. Tool names follow `mealie_<verb>_<noun>`. Test files follow the same grouping: `tests/unit/test_<group>.py` and `tests/live/test_<group>.py`. Shared helpers live in `src/mealie_mcp/tools/_common.py`; do not re-implement validation, error mapping, or body decoding inline. Use `to_unset(value)` to translate optional caller arguments into the generated client's `UNSET` sentinel. Use `ack_delete(action, response, ack_id)` for every delete tool so the MCP contract returns the canonical ``{"id": <ack_id>, "deleted": True}`` shape. Compare status codes with `HTTPStatus` constants and cast `response.status_code` to `int` when forwarding it to `raise_api_error`, since the generator types `status_code` as the `HTTPStatus` enum.

## Test conventions

Unit tests cover pure logic only. They do not perform HTTP calls, including via mock transports. Per-tool unit tests cover input validation. Shared-helper behaviour in `tools/_common.py` is tested once in `tests/unit/test_common.py`, not re-tested through each tool. `tests/conftest.py` loads `.env` for the whole session.

Live tests are tagged `@pytest.mark.live` and reuse the shared fixtures in `tests/live/conftest.py`: `mealie_client` (session-scoped authenticated client) and `sentinel_name` (per-test unique `mcp-test-` name). They follow a sentinel-staging pattern: create a sentinel resource using `sentinel_name`, exercise the tool, assert on observable effects, then delete the sentinel. Cleanup runs in a `pytest` fixture finalizer or a `try`/`finally` block so it executes even when the test body fails. Read-only tools still follow the pattern: create the sentinel, perform the read, assert the sentinel appears, delete it. For resources nested under a parent (for example, comments on a recipe), stage the parent sentinel first, then the child sentinel under it; cleanup deletes both.

Live assertions observe a behavioural difference, not just that the call did not error. "No 422" is a smoke check, not a test. If a parameter cannot be exercised against an observable effect (presence, absence, value change, ordering shift), do not ship it; defer the parameter and record the reason in the task file or the PR body under "Risks".

A failing live test is never silenced or marked `xfail` to ship. Fix the tool, fix the test, or descope and surface the decision. After any live test failure, confirm by hand that no `mcp-test-` data remains and delete it before the next run.

Every new tool ships with at least one unit test and at least one live test.

`uv run pytest` measures branch coverage of `src/mealie_mcp` and prints a report; there is no hard threshold. The generated client and the `regen-client` operator script are omitted from measurement. Per-tool dispatch code is exercised by live tests, not unit tests, so the unit number alone is a partial view. The real guardrail is the "at least one unit test and one live test per tool" rule above; the coverage report is for visibility.

## Security rules

Never commit `.env` or any file that contains real tokens, hostnames, IPs, or user names. `.env.example` carries variable names with placeholder values only, and every new environment variable is added there with a placeholder value. All public-facing docs and examples use `mealie.example.com`, never a real hostname. Logging never emits tokens, passwords, full URLs with query strings, or request bodies that may contain secrets, and helpers redact the `Authorization` header. Treat every Mealie response as untrusted input for MCP tool output schemas.

## Branches, commits, and PRs

Never commit to `main`. Create a branch named `<type>/<scope>-<slug>` where `<type>` and `<scope>` match the conventional commit and `<slug>` is a short summary. Use conventional commits with lower-case subjects. Commit in small steps and keep generated artifacts isolated in their own commit.

Push as soon as the definition-of-ready checks are green locally, then open a PR against `main`. PR title is the conventional commit subject for the headline change. The PR body must contain, in order: a link to the task file by slug if one exists; a "Tools added" or "Changes" bullet list with name and one line each; a "How tested" block with the tail of `pytest` and `pytest -m live` output; and a "Risks" block, even if it says "none". Mark ready for review only after CI is green.

## Blockers

If anything blocks the task, stop and surface the blocker. Do not silently work around it. Examples include a spec gap, a response shape the generator handled poorly, a missing test fixture, an environment limitation, a live test that cannot run, or genuine ambiguity about the right approach. Do not suppress lint or type errors with `# noqa`, `# type: ignore`, or similar to keep going. Do not invent endpoints the spec does not define. If the spec and live behaviour disagree, trust live behaviour and record the gap in the PR body under "Risks".
