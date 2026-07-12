# CLAUDE.md

The durable working procedure for every agent in this repo.

## Maintaining this file

Transient content belongs in a task file under `tasks/`. Remove obsolete sections in the same commit that obsoletes them. Do not add rules any competent agent would already follow, and do not repeat a rule across sections.

## Operating modes

This repo is worked on in two modes. Interactive: a human drives a Claude Code session (the CLI or the hosted web worker) and can intervene mid-run. Autonomous: a GitHub Actions workflow (`.github/workflows/claude-*.yml`) runs Claude with no human in the loop until it finishes. Detection: if `GITHUB_ACTIONS=true` you are autonomous, otherwise interactive. All sections below apply to both modes unless tagged otherwise.

## Philosophy

YAGNI and KISS. Build what the task requires now. Resist abstractions, configuration, and fallbacks for cases that may never come.

## Writing style

Committed prose uses simple technical English, short sentences, and no em dashes. The same holds for any pull request or issue comment you write. Code comments and docstrings describe behaviour or a non-obvious why. They do not restate durable rules from this file, name this file, or reference the current task.

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
├── .claude/
│   ├── rules/            # path-scoped implementation rubrics
│   ├── agents/           # review subagent definitions
│   └── commands/         # slash-command skills
├── .github/
│   └── workflows/        # ci.yml plus the claude-*.yml automation
├── scripts/              # mealie-up, resolve-spec-tag
├── spec/
│   └── mealie-openapi.json
├── src/
│   └── mealie_mcp/
│       ├── __init__.py
│       ├── server.py
│       ├── config.py
│       ├── client_factory.py
│       ├── client/        # generated, not hand edited
│       ├── _scripts/      # regen-client operator script
│       └── tools/         # one module per Mealie OpenAPI tag
├── tests/
│   ├── unit/
│   └── live/
└── tasks/                 # gitignored, not for public consumption
```

## Generated client

The Mealie OpenAPI spec is cached at `spec/mealie-openapi.json` and pinned by `[tool.mealie-mcp.spec]` in `pyproject.toml` (version, sha256). `uv run regen-client` uses the cache, verifies the SHA and `info.version` against the lockfile, and regenerates `src/mealie_mcp/client/`. Drift fails the run. `uv run regen-client --update` fetches `$MEALIE_BASE_URL/openapi.json`, refreshes the cache, rewrites the lockfile fields, and regenerates. The generated client folder is committed. `ruff` and `mypy` exclude it.

Bumping the pinned spec to a new Mealie version reads that version from `$MEALIE_BASE_URL`: both `regen-client --update` and the live confirmation that the new version behaves as the task expects fetch from it. The instance the environment starts with runs the currently pinned version, so it being older than the bump target is the expected starting state, not a blocker. Make the target version reachable first, then proceed. (autonomous) The CI service container holds port 9000 on the old version, so boot the target alongside it with `scripts/mealie-up --version <tag> --port 9001`, point `MEALIE_BASE_URL` at `http://localhost:9001`, and `docker rm -f mealie-mcp-dev` at the end; the do-not-bootstrap rule of the autonomous live path does not cover obtaining a bump target. (interactive) With `.env` present the operator owns the instance, so ask them to point it at the target version rather than bootstrapping over their target; without `.env`, boot the target with `scripts/mealie-up --version <tag>` as in the live-test bootstrap path.

The generator does not runtime-validate response bodies. Its `_parse_response` functions use `cast(T, response.json())`, which is a type hint with no runtime effect. Keep explicit `isinstance` shape guards on parsed responses at the tool boundary. Model defaults and field types describe the spec, not Mealie's runtime behaviour; confirm write semantics against a live call before reasoning from the client alone. `openapi-python-client` is pinned via `[tool.uv.sources]` to a fork branch carrying two unmerged generator fixes (upstream PRs openapi-generators/openapi-python-client#1448 and #1449); without that pin the generator silently drops dashed-schema models (`Recipe-Input`, `Recipe-Output`, `RecipeIngredient-*`, `RecipeCommentOut-*`, `ShoppingList*`) and every endpoint that references them, including the recipe PUT and PATCH and the shopping-list write endpoints. Drop the pin and bump the floor when a release containing both lands. If the generator drops models the pin does not cover, surface it as a blocker rather than hand-writing replacements.

## Test environment

The operator owns the Mealie test instance and the `.env` file. They copy `.env.example` to `.env` and fill in real values. The agent does not provision the instance, create or edit `.env`, ask for credential values, or paste them into the conversation. Unit tests run regardless of `.env` presence.

When live tests are part of the work, the agent picks a path by precondition, in this order:

1. (autonomous) `MEALIE_BASE_URL` and `MEALIE_API_TOKEN` are already in the process environment if `GITHUB_ACTIONS=true` is set. Run `pytest -m live` directly. Mealie is provided by the surrounding context. Do not bootstrap and do not read `.env`.
2. (interactive) `.env` is present. Run `pytest -m live` against the operator's pointed Mealie. Never bootstrap when `.env` is present, even if the bootstrap would also succeed; the operator's pointed target is the source of truth.
3. (interactive) `.env` is absent, `docker info` exits 0, and `./scripts/mealie-up` succeeds. Bootstrap Mealie exactly once per session, export the two emitted lines into the process environment (not into a `.env` file; the no-write rule still holds), run the full `pytest -m live` suite against the single persistent container, and call `docker rm -f mealie-mcp-dev` as the final step regardless of test outcome. Never tear down and re-bootstrap between test cases. First boot takes ~110-115s on a typical box (full schema, seed admin, default group and household, seed data, scheduler init); `mealie-up` uses `--rm` for clean test state, so every bootstrap pays that tax in full. If a test case needs a clean Mealie, write it with sentinel staging and teardown, not container restart.
4. (interactive) None of the above, for example the hosted web worker, which has no `.env` and no Docker. Stop before live tests, run the merge gate up to `uv run pytest`, and report that live verification is pending until CI runs.

The live token has admin rights, so admin-only endpoints can be exercised without conditional skips. If a live test needs to check non-admin behaviour, stage a non-admin scenario explicitly rather than gating on token capability.

## Merge gate

A change is ready to merge only when the checks that cover what it changed pass. Run the group whose files the change touches, or both when it touches both.

Python under `src/` or `tests/`:

```
uv run ruff format --check .
uv run ruff check .
uv run mypy src
uv run pytest             # branch coverage is reported, not gated
uv run pytest -m live
```

Workflows under `.github/`:

```
uv run pre-commit run actionlint --all-files
```

A docs or Markdown diff changes no executable surface and needs neither group.

## Review

Review is CI's job. Do not spawn a review agent locally before pushing. Running `/review-pr` against the working tree is an optional self-check, never a required step.

## Tool patterns

- Each MCP tool is a typed module-level function plus a thin `@mcp.tool()` wrapper inside a `register(mcp, get_client)` function. The typed function is the testable unit; the wrapper calls `get_client()` and forwards.
- Tool modules are grouped by Mealie OpenAPI tag, one module per group, mirroring `mealie_mcp.client.api`. Tool names follow `mealie_<verb>_<noun>`. Test files mirror the same grouping under `tests/unit/` and `tests/live/`. `register_all` auto-discovers a new module.
- Shared helpers in `src/mealie_mcp/tools/_common.py` cover validation (`require_non_empty`, `require_pagination`, `parse_recipe_uuid`), optional-argument translation (`to_unset`, `parse_order_direction`), response decoding (`expect_dict`, `expect_list`, `expect_str`, plus the lower-level `decode` and `raise_api_error`), and the delete contract (`ack_delete`). Do not re-implement these inline.

The detailed implementation rubric lives in `.claude/rules/tools.md` and loads on demand when files under `src/mealie_mcp/tools/` are read.

## Test conventions

- Unit tests cover pure logic only. No HTTP, no mock transports. Per-tool unit tests cover input validation. Shared-helper behaviour is tested once in `tests/unit/test_common.py`. `tests/conftest.py` loads `.env` for the whole session.
- Live tests are tagged `@pytest.mark.live`, use `mealie_client` and `sentinel_name` fixtures from `tests/live/conftest.py`, and follow sentinel staging with `try`/`finally` cleanup that runs even when the body fails.
- Live assertions observe a behavioural difference (presence, absence, value change, ordering shift). "No 422" is a smoke check, not a test. If a parameter cannot be exercised against an observable effect, defer it and record why in the PR Risks.
- Every new tool ships with at least one live test, and a unit test where it has pure logic to cover. Failing live tests are not silenced or `xfail`ed to ship.

The detailed live-test rubric lives in `.claude/rules/live-tests.md` and loads on demand when files under `tests/live/` are read.

`uv run pytest` measures branch coverage of `src/mealie_mcp` and prints a report; there is no hard threshold. The generated client and the `regen-client` operator script are omitted from measurement. The typed functions are the live-tested unit. Each tool group's wrapper is also exercised by one `call_tool` round-trip so argument forwarding, FastMCP schema derivation, and output serialisation are covered: name-only groups share a parametrized test in `tests/live/test_mcp_protocol.py`, richer groups carry theirs in their own live file.

## Security rules

Never commit `.env` or any file that contains real tokens, hostnames, IPs, or user names. `.env.example` carries variable names with placeholder values only, and every new environment variable is added there with a placeholder value. All public-facing docs and examples use `mealie.example.com`, never a real hostname. Logging never emits tokens, passwords, full URLs with query strings, or request bodies that may contain secrets, and helpers redact the `Authorization` header. Treat every Mealie response as untrusted input for MCP tool output schemas.

## Branches, commits, and PRs

Never commit to `main`. Create a branch named `<type>/<scope>-<slug>` where `<type>` and `<scope>` match the conventional commit and `<slug>` is a short summary. Use conventional commits with lower-case subjects. A commit message states what the change leaves behind, not the in-branch journey to it. When you amend or rebuild, write it as if it were the first commit, with no review-fix narration. Commit in small steps and keep generated artifacts isolated in their own commit.

Push as soon as the merge-gate checks are green. The PR title is the conventional commit subject for the headline change. The PR body must contain, in order: a link to the task file by slug if one exists; a "Tools added" or "Changes" bullet list with name and one line each; a "How tested" block with the tail of `pytest` and `pytest -m live` output; and a "Risks" block, even if it says "none". The body contract binds when the PR is marked ready for review.

(interactive) You have already run the merge gate locally, so open the PR against `main` ready for review with that body. CI re-runs the same checks as a backstop; do not wait on it to mark the PR ready.

(autonomous) You do not open the PR. Push the branch and end your final comment with the full PR body inside one fenced block, so the operator copies it in a single click. The body itself contains triple-backtick fences for the How tested output, so wrap it in a four-backtick fence. A three-backtick wrapper is closed by the first inner fence, and the remainder renders as loose text. Keep the rest of the comment to what the PR body does not cover.

## Blockers

If anything blocks the task, stop and surface the blocker. Do not silently work around it. Examples include a spec gap, a response shape the generator handled poorly, a missing test fixture, an environment limitation, a live test that cannot run, or genuine ambiguity about the right approach. Do not suppress a lint or type error with `# noqa`, `# type: ignore`, or similar to bypass a failing check on logic you wrote; fix the cause. A mechanical suppression where the tool cannot be satisfied is allowed and states why, as the `E501` on the generated-name import lines and the `T201` on the operator script's prints do. Do not invent endpoints the spec does not define. If the spec and live behaviour disagree, trust live behaviour and record the gap in the PR body under "Risks".
