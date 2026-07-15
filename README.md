# mealie-mcp

[![CI](https://github.com/alexander-wenzel-dev/mealie-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/alexander-wenzel-dev/mealie-mcp/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)

Talk to your Mealie recipe manager in plain language. This MCP server lets an assistant like Claude read, create, and manage recipes, meal plans, and shopping lists on a Mealie instance you control.

> The only Mealie MCP with a generated typed client under a curated set of tools, each verified against a live Mealie, so they match what Mealie actually ships and stay correct as it evolves.

- **Generated client, not hand-typed** - the request functions and models are generated from Mealie's OpenAPI spec, not a hand-written wrapper
- **Curated toolset** - a focused set of tools with typed inputs and outputs
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
>
> _"Tag all my soup recipes as 'winter' in one go."_

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

To get a token, open your profile in Mealie and create one under Manage Your API
Tokens, then use its value for `MEALIE_API_TOKEN`.

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

## Running over HTTP

By default the server speaks stdio, which is what the client configs above use. To
serve it over HTTP instead, for remote or container hosting, set
`MEALIE_MCP_TRANSPORT=http`. The HTTP transport is gated by a static bearer token
and refuses to start without one. Generate a token with the bundled script:

```sh
./scripts/gen-token
```

Put the value in `MEALIE_MCP_HTTP_TOKEN`. Clients then send it as
`Authorization: Bearer <token>`. The relevant variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `MEALIE_MCP_TRANSPORT` | `stdio` | `stdio` or `http` |
| `MEALIE_MCP_HTTP_TOKEN` | none | required for HTTP; no default, generate one |
| `MEALIE_MCP_HTTP_HOST` | `127.0.0.1` | bind address |
| `MEALIE_MCP_HTTP_PORT` | `8000` | bind port |
| `MEALIE_MCP_HTTP_ALLOWED_HOSTS` | `127.0.0.1,localhost` | allowed `Host` headers |

To bind IPv6, set `MEALIE_MCP_HTTP_HOST` to `::1` (localhost) or `::` (all
interfaces) and add the bracketed literal `[::1]` to
`MEALIE_MCP_HTTP_ALLOWED_HOSTS`, since the allowlist matches the bracketed form.

On the HTTP transport the server validates the `Host` and `Origin` headers of
each request against `MEALIE_MCP_HTTP_ALLOWED_HOSTS` and rejects a mismatch,
which blocks DNS-rebinding and cross-origin browser requests.

The bearer token is a single shared key with no rotation or revocation. It is
meant for localhost or for a network you already trust. Do not expose the HTTP
transport to an untrusted network on its own: this server holds an admin Mealie
token, so anyone who reaches it drives Mealie as admin. For real authentication
or SSO, put a reverse proxy that terminates OIDC in front of it.

## Tools

The server exposes 97 tools across 16 groups, one per Mealie OpenAPI tag. New groups are added as the project grows.

<details>
<summary>All tool groups</summary>

### Recipes

| Group                 | Coverage                                                                                                                                                                                            |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `recipe_crud`         | Create, read, list, duplicate, update, and delete recipes; scrape from a URL or from HTML or JSON, suggest recipes from the foods on hand, patch the last-made timestamp, and set or delete the title image. |
| `recipe_comments`     | Create, read, list, update, and delete recipe comments.                                                                                                                                           |
| `recipe_timeline`     | Create, read, list, update, and delete a recipe's timeline events, its cooking journal.                                                                                                           |
| `recipe_bulk_actions` | Tag, categorize, apply settings to, or delete many recipes in one call.                                                                                                                           |

### Organizers and ingredient data

| Group                         | Coverage                                                                            |
| ----------------------------- | ----------------------------------------------------------------------------------- |
| `organizer_categories`        | Create, read by id or slug, list (including empty ones), update, and delete recipe categories. |
| `organizer_tags`              | Create, read by id or slug, list (including empty ones), update, and delete recipe tags.        |
| `organizer_tools`             | Create, read by id or slug, list, update, and delete recipe tools.                  |
| `groups_multi_purpose_labels` | Create, read, list, update, and delete multi-purpose labels.                        |
| `recipes_foods`               | Create, read, list, update, and delete ingredient foods.                            |
| `recipes_units`               | Create, read, list, update, and delete ingredient units.                            |

### Households

| Group                            | Coverage                                                                                                          |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `households_mealplans`           | Create, read, list, update, and delete meal plan entries; get today's plan and add a server-picked random entry. |
| `households_mealplan_rules`      | Create, read, list, update, and delete meal plan rules.                                                          |
| `households_shopping_lists`      | Create, read, list, update, and delete shopping lists, and add or remove a recipe's ingredients, one recipe or several. |
| `households_shopping_list_items` | List, add, update, delete, and bulk-delete shopping list items.                                                  |
| `households_cookbooks`           | Create, read, list, update, and delete cookbooks.                                                                |

### Users

| Group           | Coverage                                                                               |
| --------------- | -------------------------------------------------------------------------------------- |
| `users_ratings` | List a user's ratings and favorites, set a recipe rating, and add or remove favorites. |

</details>

## Contributing

Setup, the checks a change must pass, and the branch and commit conventions are in
[CONTRIBUTING.md](CONTRIBUTING.md).

## Security

To report a vulnerability or read the token-handling guidance, see
[SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE).
