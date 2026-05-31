# CLAUDE.md

The durable working procedure for every agent in this repo.

## Maintaining this file

Transient content belongs in a task file under `tasks/`. Remove obsolete sections in the same commit that obsoletes them. Do not add rules any competent agent would already follow, and do not repeat a rule across sections.

## Philosophy

YAGNI and KISS. Build what the task requires now. Resist abstractions, configuration, and fallbacks for cases that may never come.

## Writing style

Committed prose uses simple technical English, short sentences, and no em dashes. Code comments and docstrings describe behaviour or a non-obvious why. They do not restate durable rules from this file, name this file, or reference the current task.

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
- `python-dotenv` for `.env` loading at package import.
- `pytest` with markers for unit and live tests.
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

The generator does not runtime-validate response bodies. Its `_parse_response` functions use `cast(T, response.json())`, which is a type hint with no runtime effect. Keep explicit `isinstance` shape guards on parsed responses at the tool boundary. The current spec also drops the `ShoppingList*` model schemas during generation, a known generator warning that does not affect recipe operations. If the generator drops models needed for an API group, that group is unimplementable until the upstream spec is fixed; surface it as a blocker rather than hand-writing replacement models.

## Test environment

The operator owns the Mealie test instance and the `.env` file. They copy `.env.example` to `.env` and fill in real values. The agent does not provision the instance, create or edit `.env`, ask for credential values, or paste them into the conversation. If `.env` is missing, unit tests still run; live tests fail fast with a clear message. An agent without `.env` runs the definition-of-ready checks up to `uv run pytest`, stops before `pytest -m live`, and reports that live verification is pending.

## Definition of ready

A task is only ready for review when all of these commands pass.

```
uv run ruff format --check .
uv run ruff check .
uv run mypy src
uv run pytest
uv run pytest -m live   # run locally before merge, not in CI
```

## Tool patterns

Each MCP tool has two layers. The first is a typed module-level function that takes an `AuthenticatedClient` and the tool inputs, validates them with the shared `require_non_empty` helper, calls the generated client's `sync_detailed` entry point (so the raw `status_code` and `content` are available for error mapping), maps non-success responses through the shared `raise_api_error` helper, decodes successful bodies with the shared `decode` helper, and returns a JSON-compatible value validated with explicit `isinstance` shape guards. This layer is the testable unit. The second is a thin `@mcp.tool()` wrapper inside a `register(mcp)` function; the wrapper calls `build_client()` (the only sanctioned construction path for the authenticated client) and forwards to the typed function. The server wires everything by importing each tool module in `src/mealie_mcp/tools/__init__.py` and calling its `register(mcp)` from a single `register_all` entry point.

Tool modules are grouped by Mealie OpenAPI tag, one module per group, mirroring the layout of `mealie_mcp.client.api`. Tool names follow `mealie_<verb>_<noun>`. Shared helpers live in `src/mealie_mcp/tools/_common.py`; do not re-implement validation, error mapping, or body decoding inline. Compare status codes with `HTTPStatus` constants and cast `response.status_code` to `int` when forwarding it to `raise_api_error`, since the generator types `status_code` as the `HTTPStatus` enum.

## Test conventions

Unit tests cover pure logic only. They do not perform HTTP calls, including via mock transports. Per-tool unit tests cover input validation. Shared-helper behaviour (`decode`, `raise_api_error`, `require_non_empty`) is tested once in `tests/unit/test_common.py`, not re-tested through each tool.

Live tests are tagged `@pytest.mark.live` and reuse the shared fixtures in `tests/live/conftest.py`: `mealie_client` (session-scoped authenticated client) and `sentinel_name` (per-test unique `mcp-test-` name). They follow a sentinel-staging pattern: create a sentinel resource using `sentinel_name`, exercise the tool, assert on observable effects, then delete the sentinel. Cleanup runs in a `pytest` fixture finalizer or a `try`/`finally` block so it executes even when the test body fails. Read-only tools still follow the pattern: create the sentinel, perform the read, assert the sentinel appears, delete it. For resources nested under a parent (for example, comments on a recipe), stage the parent sentinel first, then the child sentinel under it; cleanup deletes both.

A failing live test is never silenced or marked `xfail` to ship. Fix the tool, fix the test, or descope and surface the decision. After any live test failure, confirm by hand that no `mcp-test-` data remains and delete it before the next run.

Every new tool ships with at least one unit test and at least one live test.

## Security rules

Never commit `.env` or any file that contains real tokens, hostnames, IPs, or user names. `.env.example` carries variable names with placeholder values only, and every new environment variable is added there with a placeholder value. All public-facing docs and examples use `mealie.example.com`, never a real hostname. Logging never emits tokens, passwords, full URLs with query strings, or request bodies that may contain secrets, and helpers redact the `Authorization` header. Treat every Mealie response as untrusted input for MCP tool output schemas.

## Branches, commits, and PRs

Never commit to `main`. Create a branch named `<type>/<scope>-<slug>` where `<type>` and `<scope>` match the conventional commit and `<slug>` is a short summary. Use conventional commits with lower-case subjects. Commit in small steps and keep generated artifacts isolated in their own commit.

Push as soon as the definition-of-ready checks are green locally, then open a PR against `main`. PR title is the conventional commit subject for the headline change. The PR body must contain, in order: a link to the task file by slug if one exists; a "Tools added" or "Changes" bullet list with name and one line each; a "How tested" block with the tail of `pytest` and `pytest -m live` output; and a "Risks" block, even if it says "none". Mark ready for review only after CI is green.

## Blockers

If anything blocks the task, stop and surface the blocker. Do not silently work around it. Examples include a spec gap, a response shape the generator handled poorly, a missing test fixture, an environment limitation, a live test that cannot run, or genuine ambiguity about the right approach. Do not suppress lint or type errors with `# noqa`, `# type: ignore`, or similar to keep going. Do not invent endpoints the spec does not define. If the spec and live behaviour disagree, trust live behaviour and record the gap in the PR body under "Risks".
