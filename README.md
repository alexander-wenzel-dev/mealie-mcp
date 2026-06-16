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

## Tools

The server exposes MCP tools grouped by Mealie OpenAPI tag. New groups are added as the project grows.

| Group                            | Coverage                                                                                                               |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `recipe_crud`                    | Create, read, list, duplicate, update, scrape from URL or JSON-LD, patch the last-made timestamp, and delete recipes.   |
| `recipe_comments`                | Create, read, list, update, and delete recipe comments.                                                                |
| `organizer_categories`           | Create, read by id or slug, list, update, and delete recipe categories.                                                |
| `organizer_tags`                 | Create, read by id or slug, list, update, and delete recipe tags.                                                      |
| `organizer_tools`                | Create, read by id or slug, list, update, and delete recipe tools.                                                     |
| `recipes_foods`                  | Create, read, list, update, and delete ingredient foods.                                                               |
| `recipes_units`                  | Create, read, list, update, and delete ingredient units.                                                               |
| `households_mealplans`           | Create, read, list, update, and delete meal plan entries.                                                              |
| `households_shopping_lists`      | Create, read, list, update, and delete shopping lists.                                                                 |
| `households_shopping_list_items` | Add, update, and delete shopping list items.                                                                           |

## Regenerate the API client

The Mealie OpenAPI spec is cached at `spec/mealie-openapi.json` and pinned in `pyproject.toml`. Regenerate the typed client from the cached spec:

```sh
uv run regen-client            # use the cached spec
uv run regen-client --update   # refetch from $MEALIE_BASE_URL/openapi.json and re-pin
```

## Run tests

```sh
uv run pytest          # unit tests
uv run pytest -m live  # live tests, require a local .env
```

## License

MIT. See [LICENSE](LICENSE).
