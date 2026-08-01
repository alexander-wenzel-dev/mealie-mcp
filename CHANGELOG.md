# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `mealie_update_recipe` now takes `cook_time`. Mealie never fills this field
  itself; its importer maps a source recipe's cook time onto `perform_time`.
- `mealie_update_recipe` now takes `org_url`, the source URL of a recipe.
- `mealie_update_recipe` now takes `tools`, which links a recipe to the equipment
  catalogue `mealie_list_recipes` already filters on. The name and slug sent with
  a tool overwrite that tool's catalogue entry for every recipe using it, and an
  unknown `id` creates a new entry.

## [0.2.0] - 2026-07-26

### Added

- `mealie_update_recipe` now takes `recipe_servings` and `recipe_yield_quantity`,
  the two numeric fields Mealie's ingredient scaler reads.

### Changed

- The pinned Mealie OpenAPI spec moved from v3.20.1 to v3.21.0.

### Fixed

- `mealie_update_recipe` now states that an ingredient's `food` and `unit` each
  need both the `id` and the `name` of an existing record; either alone is
  rejected.
- The meal plan tools now state the slot Mealie seeds for an omitted
  `entry_type`: `breakfast` on `mealie_create_mealplan`, `dinner` on
  `mealie_create_random_mealplan`.
- `mealie_create_mealplan_rule` now states that Mealie `AND`-joins the filters of
  every rule matching a slot, so rules narrow each other instead of overriding.

## [0.1.0] - 2026-07-19

First public release.

### Added

- MCP server that wraps the Mealie REST API, exposing 97 tools across 16 groups,
  one per Mealie OpenAPI tag. Tools cover recipes, comments, timeline events,
  bulk recipe actions, categories, tags, tools, labels, foods, units, meal plans,
  meal plan rules, shopping lists, shopping list items, cookbooks, and user
  ratings and favorites.
- A typed Python client generated from Mealie's OpenAPI spec and pinned by
  version and checksum, so a Mealie upgrade is a regenerate-and-review step.
- stdio transport for local MCP clients, and an HTTP transport gated by a static
  bearer token with `Host` and `Origin` validation against DNS rebinding.
- A `Dockerfile` that runs the HTTP transport as a non-root user, with a
  `/health` endpoint for container healthchecks.
- Live tests that verify every tool against a real Mealie instance behaviourally.

### Security

- The HTTP transport refuses to start without a bearer token, and helpers redact
  the `Authorization` header so tokens never reach logs.

[Unreleased]: https://github.com/alexander-wenzel-dev/mealie-mcp/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/alexander-wenzel-dev/mealie-mcp/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/alexander-wenzel-dev/mealie-mcp/releases/tag/v0.1.0
