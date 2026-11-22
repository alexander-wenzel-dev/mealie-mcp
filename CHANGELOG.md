# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `mealie_merge_category` and `mealie_merge_tag` resolve a duplicate by merging
  one organizer into another and return the surviving organizer. Recipes on the
  source move to the target and the source is deleted. Cookbook and meal plan
  rule filters that name the source keep its id. Both need Mealie v3.27.0.
- `mealie_merge_tool` merges one recipe tool into another the same way.
- `mealie_merge_label` merges one multi purpose label into another. Foods and
  shopping list items on the source move to the target, shopping lists drop
  the source from their label order, and the source is deleted.
- `mealie_list_empty_tools`, `mealie_list_empty_labels` and
  `mealie_list_empty_foods` list the unused entries. A label is in use on a
  food or a shopping list item, a food on a recipe or a shopping list item.
- `mealie_get_household_recipe` reads when the current household last made a
  recipe, in UTC, null when it never did.
- `mealie_create_recipe_asset_from_url` attaches an image from a URL to a
  recipe as an asset. Each call adds a new asset; the title image stays.

### Changed

- **Breaking:** the supported Mealie floor is v3.31.0, raised from v3.26.0. The
  tools still run against an older Mealie, but their docstrings describe the
  v3.31.0 behaviour.
- **Breaking:** `mealie_update_recipe` no longer takes `cook_time`. Mealie
  v3.31.0 drops the recipe `cookTime` field and moves stored values into
  `performTime`, which the UI shows as Cook Time. Set the cooking duration
  through `perform_time_seconds`.
- The pinned Mealie OpenAPI spec moved from v3.27.0 to v3.31.0. Most request
  and response schemas are renamed, and the tools follow the new models.
- `mealie_update_recipe` takes `total_time_seconds`, `prep_time_seconds` and
  `perform_time_seconds`. Mealie v3.31.0 stores a recipe time as a duration in
  seconds and moves parseable time texts there on upgrade; `total_time`,
  `prep_time` and `perform_time` are the free text displayed after it. A step
  keeps its `durationSeconds` only when it is sent with it.
- `mealie_list_mealplans` takes `include_week_entries`. Mealie leaves entries
  planned for a whole week out of the list unless it is set, and out of
  today's plan always.
- `mealie_create_mealplan` takes `end_date` and `recipe_scale`, and
  `mealie_create_random_mealplan` takes `end_date`. A week entry needs
  `end_date` exactly six days after `date`.
- `mealie_update_mealplan` changes an entry's recipe, recipe scale and week. An
  empty `recipe_id` removes the recipe link and an empty `end_date` makes the
  entry a single day.
- `mealie_update_recipe` resolves each tag, category and tool by id or by name.
  An id of an existing entry wins, a known name links its entry, a new name
  creates one, and an empty name is dropped. An update no longer rewrites a
  tool's catalogue entry.
- `mealie_tag_recipes` and `mealie_categorize_recipes` take items with only a
  name and resolve them the same way. The three bulk recipe actions fail with a
  404 and change no recipe when a slug in the batch matches no recipe.
- `mealie_update_shopping_list_item` keeps an item's recipe links when it
  checks the item off.
- `mealie_update_last_made` documents that the recipe payload carries no
  `lastMade`; Mealie v3.31.0 stores the timestamp per household. Read it with
  `mealie_get_household_recipe`.

### Fixed

- `mealie_update_mealplan` keeps a week entry's span and the entry's recipe
  scale. A new date moves the week with it. Against a Mealie without a recipe
  scale it sends none instead of failing.

## [0.5.0] - 2026-09-19

### Changed

- **Breaking:** the supported Mealie floor is v3.26.0, raised from v3.23.0.
  Below it, merging a food or a unit strands the shopping list items that used
  it, and two meal plan rules filtering one slot match no recipe. The tools
  still run against an older Mealie; three of them describe behaviour it does
  not have.
- The pinned Mealie OpenAPI spec moved from v3.23.1 to v3.27.0.
- `mealie_suggest_recipes` items carry a `substitutedFoods` list naming each
  missing food and the food that stands in for it, and the tool documents it.
  Mealie fills the list from the substitutions recorded on a food, and sends it
  because its `includeSubstitutions` parameter defaults to true server-side.
- FastMCP moves to 4.0.3, which replaces mcp 1.28.1 with mcp 2.2.0 and
  mcp-types.

### Fixed

- The six list-returning tools declare `list[dict[str, Any]]`, so FastMCP
  derives an output schema for them again and their results come back as
  structured content.
- `mealie_merge_food` and `mealie_merge_unit` now state that a shopping list
  item on the source moves to the target. Mealie repoints it from v3.25.0
  instead of leaving it on the deleted id.
- `mealie_create_mealplan_rule` now states that a slot whose rules together
  match no recipe fails with a 404. Two filters on `tags.name` matched nothing
  at all before Mealie v3.26.0; from that version they select the recipes
  carrying both tags.
- `mealie_set_recipe_image_from_url` now states that Mealie refuses a URL
  resolving to a private or internal address unless its `HTTP_ALLOW_LIST`
  names the host. That check arrived in Mealie v3.26.0.
- Fifteen `extras` fields on generated models defaulted to a model instance
  that every object of its class shared, because a class body evaluates a
  default once. They default to `UNSET` now.

### Security

- The generated client is built with openapi-python-client 0.29.1. 0.29.0 was
  affected by GHSA-5293-mq8x-g3xj, where a malicious OpenAPI document can make
  the generator emit arbitrary code that then runs in consumers of the
  generated client.

## [0.4.0] - 2026-08-21

### Changed

- The pinned Mealie OpenAPI spec moved from v3.22.0 to v3.23.1.
- `mealie_set_recipe_image_from_url` returns the recipe's new image key as
  `{"image": <key>}` in place of a confirmation. Each call mints a new key.
  Setting a recipe image needs Mealie v3.23.0 or newer.

### Fixed

- A tool reports Mealie's own message when a call fails, without the raw
  database error Mealie sends alongside it. That text carries the SQL statement
  and the values bound to it.
- `mealie_update_recipe` rejects an unusable item in `recipe_instructions`,
  `notes`, `tags` or `recipe_category` with an error naming the field and the
  index.
- `mealie_update_recipe` now states that a `tags` or `recipe_category` item
  needs the `id`, `name` and `slug` of an existing record together.
- `mealie_update_recipe` now states that a `referenceId` Mealie generates is not
  stored. The next response carries a different one, so the id a new ingredient
  comes back with cannot link a step to it.
- `mealie_update_recipe` now states where Mealie renders a step's `title` and
  `summary`, so the two are no longer named as interchangeable.

## [0.3.1] - 2026-08-02

### Changed

- The pinned Mealie OpenAPI spec moved from v3.21.0 to v3.22.0.

## [0.3.0] - 2026-08-02

### Added

- `mealie_merge_food` and `mealie_merge_unit` resolve a duplicate by merging one
  record into another. Recipe ingredients move to the target and the source is
  deleted with its aliases. A shopping list item that references the source
  keeps the deleted id and resolves to no food or unit. A merge into itself is
  rejected. Mealie answers a self merge with a success and deletes the record.
- `mealie_create_food` and `mealie_update_food` now take `label_id`, the
  multi-purpose label that sorts a food into an aisle on a shopping list. On an
  update an empty string detaches the current label.
- `mealie_create_unit` and `mealie_update_unit` now take `description`. An empty
  string clears it on an update.
- `mealie_add_shopping_list_item` now takes `food_id`, `unit_id`, and
  `label_id`. An item that carries a food and a unit is merged into an unchecked
  item on the list with the same pair, and their quantities are summed, which a
  free-text item never is.
- `mealie_update_shopping_list_item` now takes `label_id`, the multi-purpose
  label that sorts an item into an aisle.
- `mealie_add_shopping_list_items` creates several shopping list items in one
  call. Each item names its own list. The write is not atomic.
- `mealie_update_shopping_list_items` edits or checks off several shopping list
  items in one call. Each item is read before anything is written, so an unknown
  id fails the call and leaves the rest untouched.
- `mealie_update_recipe` now takes `cook_time`. Mealie never fills this field
  itself; its importer maps a source recipe's cook time onto `perform_time`.
- `mealie_update_recipe` now takes `org_url`, the source URL of a recipe.
- `mealie_update_recipe` now takes `tools`, which links a recipe to the equipment
  catalogue `mealie_list_recipes` already filters on. The name and slug sent with
  a tool overwrite that tool's catalogue entry for every recipe using it, and an
  unknown `id` creates a new entry.

### Fixed

- `mealie_update_shopping_list_item` and `mealie_update_shopping_list_items`
  detach an item's label when `label_id` is an empty string.
- `mealie_update_recipe` documents `referenceId` on an ingredient and
  `ingredientReferences` on a step. Rewriting the ingredient list without
  sending each item's `referenceId` back makes Mealie mint new ids and leaves
  the step links pointing at ingredients that no longer exist.

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

[Unreleased]: https://github.com/alexander-wenzel-dev/mealie-mcp/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/alexander-wenzel-dev/mealie-mcp/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/alexander-wenzel-dev/mealie-mcp/compare/v0.3.1...v0.4.0
[0.3.1]: https://github.com/alexander-wenzel-dev/mealie-mcp/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/alexander-wenzel-dev/mealie-mcp/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/alexander-wenzel-dev/mealie-mcp/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/alexander-wenzel-dev/mealie-mcp/releases/tag/v0.1.0
