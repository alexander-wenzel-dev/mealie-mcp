# scripts/

Operator helpers. Not packaged or shipped to end users.

## mealie-up

Boots a local Mealie container, waits for the API to come up, mints an admin
token, and prints `MEALIE_BASE_URL` and `MEALIE_API_TOKEN` to stdout for
redirection into `.env`. Progress and diagnostics go to stderr; stdout is
exactly two `KEY=value` lines.

### Usage

```
./scripts/mealie-up [--version pinned|latest|nightly|<tag>] [--port 9000] [--name mealie-mcp-dev]
```

### Versions

- `pinned` (default) reads `[tool.mealie-mcp.spec].version` from
  `pyproject.toml`. This is the version the generated client was built
  against. Use this for live tests that should match the pinned spec.
- `latest` resolves to `ghcr.io/mealie-recipes/mealie:latest`, the most
  recent tagged Mealie release.
- `nightly` resolves to `ghcr.io/mealie-recipes/mealie:nightly`. Use this
  to verify behaviour against an unreleased fix before bumping the spec
  floor.
- Any other value is passed through as an explicit image tag, for
  example `v3.20.0`.

### Populating `.env`

```
./scripts/mealie-up > .env.new && mv .env.new .env
```

Using a staging file avoids truncating a working `.env` if the script
fails. The script itself returns a non-zero exit code and writes nothing
to stdout on any failure path; the stage-then-move idiom is what protects
against the shell truncating the destination file the moment the
redirection is opened.

The operator owns `.env`; the script never writes it directly.

### Stopping the container

```
docker rm -f mealie-mcp-dev
```

### Requirements

- `docker`
- `python3` (3.11+, for `tomllib`)

Both are available on GitHub Actions `ubuntu-latest` runners by default.

### Admin credentials

The seeded admin credentials (`changeme@example.com` / `MyPassword`) are
hardcoded upstream in `mealie/core/settings/settings.py` as private
Pydantic settings (`_DEFAULT_EMAIL`, `_DEFAULT_PASSWORD`). They are not
overridable via container environment variables. If a future Mealie
release changes either value, this script's `/api/auth/token` POST fails
with 401 and the constants in `scripts/mealie-up` need to be updated.
