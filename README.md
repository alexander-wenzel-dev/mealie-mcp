# mealie-mcp

An MCP server for the Mealie recipe manager.

The server wraps the Mealie REST API and exposes its operations as MCP tools, so an MCP-capable assistant like Claude can read, create, and manage recipes on a Mealie instance you control.

Status: early development. Not yet published to PyPI.

## Requirements

- Python 3.14
- [uv](https://docs.astral.sh/uv/)
- A reachable Mealie instance and a Mealie API token

## Install

Clone the repo so an MCP client can launch the server from your local checkout.

```sh
git clone https://github.com/alexander-wenzel-dev/mealie-mcp.git
cd mealie-mcp
uv sync
```

## Configure

Register the server in your MCP client. The example below works for any client that uses the standard MCP server config (Claude Desktop, Cursor, and others). Replace `/absolute/path/to/mealie-mcp` with the path to your clone.

```json
{
  "mcpServers": {
    "mealie": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/mealie-mcp", "run", "mealie-mcp"],
      "env": {
        "MEALIE_BASE_URL": "https://mealie.example.com",
        "MEALIE_API_TOKEN": "replace-me"
      }
    }
  }
}
```

For Claude Code:

```sh
claude mcp add mealie --env MEALIE_BASE_URL=https://mealie.example.com --env MEALIE_API_TOKEN=replace-me -- uv --directory "$(pwd)" run mealie-mcp
```

## Run tests

```sh
uv run pytest          # unit tests
uv run pytest -m live  # live tests, require a local .env
```

## License

MIT. See [LICENSE](LICENSE).
