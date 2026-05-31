# CLAUDE.md

This file is the working procedure for every agent that touches this repo. Claude Code loads it automatically.

## Maintaining this file

This file is durable procedure. Transient content belongs in a task file under `tasks/`. When a section here becomes obsolete, remove it in the same commit that obsoletes it.

## Philosophy

YAGNI and KISS. Build what the task requires now. Resist abstractions, configuration, and fallbacks for cases that may never come.

## Writing style

Committed prose uses simple technical English, short sentences, and no em dashes.

## Project goal

Build a Python MCP server that wraps the Mealie REST API. The server exposes Mealie operations as MCP tools.

## In scope

- MCP tools that call the Mealie API.
- A generated, typed Python client from the Mealie OpenAPI spec.
- Local tests that hit a live Mealie test instance.
- Public release on GitHub under MIT.

## Out of scope

- Hosting or deploying Mealie itself.
- A web UI or any non-MCP transport.
- Multi-instance routing. One Mealie instance per server process.

## Stack

- Python 3.14.
- `uv` for environment, dependencies, and lock file.
- `FastMCP` for the MCP server.
- `openapi-python-client` to generate the Mealie client from the OpenAPI spec.
- `httpx` as the HTTP transport.
- `pytest` with markers for unit and live tests.
- `ruff` for lint and format.
- `mypy` for type checks.
- `bandit` and `pip-audit` for security scans.
- `pre-commit` for local hooks.
- GitHub Actions for CI.

## Generated client

- The Mealie OpenAPI spec is cached at `spec/mealie-openapi.json` and pinned by `[tool.mealie-mcp.spec]` in `pyproject.toml` (version, sha256).
- `uv run regen-client` uses the cache, verifies the SHA and `info.version` against the lockfile, and regenerates `src/mealie_mcp/client/`. Drift fails the run.
- `uv run regen-client --update` fetches `$MEALIE_BASE_URL/openapi.json`, refreshes the cache, rewrites the lockfile fields, and regenerates.
- The generated client folder is committed. `ruff` and `mypy` exclude it.
- Bump the spec in its own commit. Do not mix a spec bump with feature work.

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

## Test environment

- The operator owns the Mealie test instance and the `.env` file. They copy `.env.example` to `.env` and fill in real values.
- The agent does not provision the instance, create or edit `.env`, ask for credential values, or paste them into the conversation.
- If `.env` is missing, unit tests still run. Live tests fail fast with a clear message.
- An agent running with no `.env` may complete the inner loop up to and including `uv run pytest`. It must stop before `pytest -m live` and report that live verification is pending.

## Inner loop

A task is only ready for review when all of these commands pass.

```
uv run ruff format --check .
uv run ruff check .
uv run mypy src
uv run pytest
uv run pytest -m live   # run locally before merge, not in CI
```

## Test conventions

- Live tests follow a round trip pattern: create, verify, delete.
- For read-only tools, the round trip creates a sentinel, exercises the read, then deletes the sentinel.
- Every live test cleans up its own state in a `pytest` fixture finalizer or a `try`/`finally` block. Cleanup must run even when the test body fails.
- Test data uses the prefix `mcp-test-` followed by an ISO timestamp.
- Unit tests cover pure logic only. They do not perform HTTP calls.
- Live tests are tagged with `@pytest.mark.live`.
- Live tests reuse the shared fixture style in `tests/live/conftest.py`.
- A failing live test is never silenced or marked `xfail` to ship. Fix the tool, fix the test, or descope.
- After any live test failure, confirm by hand that no `mcp-test-` data remains. If it does, delete it before the next run.

## Tool design

- API errors surface as MCP errors with the original message preserved.

## Security rules

- Never commit `.env` or any file that contains real tokens, hostnames, IPs, or user names.
- `.env.example` carries variable names with placeholder values only.
- All public-facing docs and examples use `mealie.example.com`. Never use real hostnames.
- Logging never emits tokens, passwords, full URLs with query strings, or request bodies that may contain secrets. Helpers redact the `Authorization` header.
- Treat every Mealie response as untrusted input for MCP tool output schemas.

## Branch and PR workflow

- Never commit to `main`. Create a branch named `<type>/<scope>-<slug>` where `<type>` and `<scope>` match the conventional commit and `<slug>` is a short summary.
- Commit in small steps using conventional commits.
- Push as soon as the inner loop is green locally, then open a PR.
- PR title: the conventional commit subject for the headline change.
- PR body must contain, in order:
  - Link to the task file by slug if one exists.
  - A "Tools added" or "Changes" bullet list, name and one line each.
  - A "How tested" block with the tail of `pytest` and `pytest -m live` output.
  - A "Risks" block, even if it says "none".
- Open the PR against `main`. Mark ready for review only after CI is green.

## Conventional commits

Use conventional commits with lower-case subjects.

## When unsure

- If the OpenAPI spec and live behaviour disagree, trust live behaviour and record the gap in the PR body under "Risks".
- If two designs look equally reasonable, pick the one closer to the Mealie spec names and note the choice in the PR body.
- If a live test cannot run because the test instance is unreachable, stop and surface the failure. Do not skip live tests to ship.
- Never invent endpoints. If the spec lacks an operation, the tool is out of scope for the task.

## Task file template

Task files live in `tasks/` and are gitignored. Copy this block when starting a new task. Save the file as `tasks/task-NN-short-slug.md`.

````markdown
# Task NN: <short title>

## Goal
One sentence. What capability does this task add.

## In scope
- Bullet list of what this task covers.

## Out of scope
- Bullet list of what this task does not cover. Name the follow up task if relevant.

## Deliverables
- Code paths and files added or changed.
- New MCP tools, each with name and one line description.

## Acceptance criteria
- Bullet list of checks that must pass beyond the durable rules.

## Test plan
- Unit tests added.
- Live tests added.

## Security checklist
- Only deltas from the durable rules.

## Notes
Anything else. Hints for the follow up task.
````

## Definition of done

A task is done when:

- All inner loop commands pass locally.
- `uv run pytest -m live` passes against the developer's Mealie test instance.
- CI is green on the PR.
- Every new MCP tool has at least one unit test and one live test.
- Any new env var is documented in `.env.example` with a placeholder value.
- The commit message follows conventional commits.
- The PR description lists new tools and links the task file by slug.
