# Contributing

Thanks for your interest in improving mealie-mcp. This guide covers the local
setup, the checks a change must pass, and the branch and commit conventions.

## Setup

You need Python 3.14 and [uv](https://docs.astral.sh/uv/). Then:

```sh
git clone https://github.com/alexander-wenzel-dev/mealie-mcp.git
cd mealie-mcp
uv sync
```

Install the git hooks once so lint and format run on commit:

```sh
uv run pre-commit install
```

## The generated client

The Mealie API client under `src/mealie_mcp/client/` is generated from Mealie's
OpenAPI spec and is not hand edited. The spec is cached at
`spec/mealie-openapi.json` and pinned in `pyproject.toml`. Regenerate it with:

```sh
uv run regen-client            # from the cached spec
uv run regen-client --update   # refetch from $MEALIE_BASE_URL/openapi.json and re-pin
```

## Checks

Run the checks that cover what you changed before opening a pull request:

```sh
uv run ruff format --check .
uv run ruff check .
uv run mypy src
uv run pytest             # unit tests
uv run pytest -m live     # live tests, need a running Mealie
```

Unit tests need nothing extra. Live tests run against a real Mealie instance. To
stand one up locally, see [`scripts/README.md`](scripts/README.md).

Every new tool ships with a live test, and a unit test where it has pure logic to
cover.

## Branches and commits

Do not commit to `main`. Work on a branch named `<type>/<scope>-<slug>`, where
`<type>` and `<scope>` match the conventional commit for the change.

Use [Conventional Commits](https://www.conventionalcommits.org/) with lower-case
subjects, for example `feat(recipes): add bulk tag action`. A commit message
states what the change leaves behind.

## Security

Never commit real tokens, hostnames, or URLs. Use `mealie.example.com` and
placeholder values in examples. See [SECURITY.md](SECURITY.md) for reporting
vulnerabilities and handling your Mealie token.
