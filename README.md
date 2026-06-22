# mealie-mcp

[![CI](https://github.com/alexander-wenzel-dev/mealie-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/alexander-wenzel-dev/mealie-mcp/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)

An MCP server for the Mealie recipe manager.

The server wraps the Mealie REST API and exposes its operations as MCP tools, so an MCP-capable assistant like Claude can read, create, and manage recipes on a Mealie instance you control.

Status: early development. Not yet published to PyPI.

## What it looks like

Once registered, you talk to your Mealie instance in plain language:

> _"Scrape this recipe from &lt;url&gt; and tag it as 'weeknight'."_
>
> _"Add the ingredients of my Lasagna recipe to this week's shopping list."_
>
> _"What did I rate the Thai curry, and mark it as a favorite."_

The assistant picks the matching tools and calls them against your instance.

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

<details>
<summary>All tool groups</summary>

| Group                            | Coverage                                                                                                               |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `recipe_crud`                    | Create, read, list, duplicate, update, scrape from URL or JSON-LD, patch the last-made timestamp, suggest recipes from the foods on hand, and delete recipes. |
| `recipe_comments`                | Create, read, list, update, and delete recipe comments.                                                                |
| `recipe_timeline`                | Create, read, list, update, and delete a recipe's timeline events, its cooking journal.                                |
| `organizer_categories`           | Create, read by id or slug, list, update, and delete recipe categories.                                                |
| `organizer_tags`                 | Create, read by id or slug, list, update, and delete recipe tags.                                                      |
| `organizer_tools`                | Create, read by id or slug, list, update, and delete recipe tools.                                                     |
| `recipes_foods`                  | Create, read, list, update, and delete ingredient foods.                                                               |
| `recipes_units`                  | Create, read, list, update, and delete ingredient units.                                                               |
| `households_mealplans`           | Create, read, list, update, and delete meal plan entries.                                                              |
| `households_shopping_lists`      | Create, read, list, update, and delete shopping lists, and add or remove a recipe's ingredients.                       |
| `households_shopping_list_items` | Add, update, and delete shopping list items.                                                                           |
| `users_ratings`                  | List a user's ratings and favorites, set a recipe rating, and add or remove favorites.                                 |

</details>

### Filtering and ordering

List tools take `page` and `per_page`, and where the Mealie endpoint supports it, `order_by` and `order_direction`.

Mealie's generic `queryFilter` expression is deliberately not exposed. It is an untyped filter string that is error prone for an assistant to build and a poor fit for typed tool inputs. Tools that need to scope a list use explicit parameters instead. The recipe timeline list, for example, filters by recipe id internally rather than asking the caller for a filter expression.

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
