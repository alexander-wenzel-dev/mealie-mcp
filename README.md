# mealie-mcp

[![CI](https://github.com/alexander-wenzel-dev/mealie-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/alexander-wenzel-dev/mealie-mcp/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)

Talk to your Mealie recipe manager in plain language. This MCP server lets an assistant like Claude read, create, and manage recipes, meal plans, and shopping lists on a Mealie instance you control.

> Built on a typed client generated straight from Mealie's own API, so the tools match what Mealie actually ships and stay correct as Mealie evolves.

- **Generated, not hand-typed** - request and response shapes come from Mealie's OpenAPI spec
- **Version-pinned** - a Mealie upgrade is regenerate-and-review, not a manual audit
- **Verified live** - every tool is tested against a real Mealie, behavioural not smoke

Status: early development. Not yet published to PyPI.

## What it looks like

Once registered, you ask in plain language and the assistant picks the matching tools:

> _"Scrape this recipe from &lt;url&gt; and tag it as 'weeknight'."_
>
> _"Add the ingredients of my Lasagna recipe to this week's shopping list."_
>
> _"What can I cook from the chicken, spinach, and feta I have on hand?"_
>
> _"Mark the Thai curry as a favorite and rate it four stars."_
>
> _"Put mushroom risotto on the meal plan for Sunday dinner."_
>
> _"Log that I made the focaccia today."_

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
| `households_shopping_list_items` | List, add, update, and delete shopping list items.                                                                     |
| `users_ratings`                  | List a user's ratings and favorites, set a recipe rating, and add or remove favorites.                                 |

</details>

## Regenerate the API client

The Mealie OpenAPI spec is cached at `spec/mealie-openapi.json` and pinned in `pyproject.toml`. Regenerate the typed client from the cached spec:

```sh
uv run regen-client            # use the cached spec
uv run regen-client --update   # refetch from $MEALIE_BASE_URL/openapi.json and re-pin
```

## Run tests

```sh
uv run pytest          # unit tests
uv run pytest -m live  # live tests, need a running Mealie
```

Unit tests need nothing extra. Live tests run against a real Mealie instance.

To stand one up locally, `scripts/mealie-up` boots a container, mints an admin token, and prints `MEALIE_BASE_URL` and `MEALIE_API_TOKEN` to stdout for `.env`:

```sh
./scripts/mealie-up > .env.new && mv .env.new .env
```

The staging file avoids truncating a working `.env` if the script fails. The variable names are also listed in `.env.example`. By default the script boots the Mealie version pinned in `pyproject.toml`, the same version the generated client and CI are built against, so the live suite stays reproducible. See [`scripts/README.md`](scripts/README.md) for version options and how to stop the container.

Then run the live suite:

```sh
uv run pytest -m live
```

## License

MIT. See [LICENSE](LICENSE).
