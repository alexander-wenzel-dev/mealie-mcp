---
paths:
  - "src/mealie_mcp/tools/**"
---

# Tool implementation rubric

The generated client under `src/mealie_mcp/client/` is out of scope: it is regenerated from the OpenAPI spec and not hand-edited.

## Two-layer structure

Each MCP tool is two layers:

1. A typed module-level function taking `AuthenticatedClient` and the tool inputs. This is the testable unit.
2. A thin `@mcp.tool()` wrapper inside `register(mcp, get_client)`. The wrapper calls `get_client()` (the process-scoped singleton from `mealie_mcp.client_factory`) and forwards to the typed function.

Do not collapse the layers, put business logic in the wrapper, or call the generated client from the wrapper instead of the typed function.

## The wrapper docstring is the tool description

FastMCP derives each tool's description from the wrapper's docstring, so it is the primary interface the calling model reads. Write it as the product surface, not an afterthought:

- a one-line summary first,
- any behavioural caveat or Mealie quirk up front, before `Args:`,
- a Google-style `Args:` block giving each argument's default and format,
- a `Returns:` line naming the response shape.

When an argument is an opaque key, a slug or an id rather than a display name, say so here, since a display name silently returns no matches. `_list_recipes` in `recipe_crud.py` is the exemplar.

## Validation

Input validation uses `require_non_empty` from `_common.py`. Inline `if not value: raise ...` for the same shape is a deviation.

## Calling the generated client

Tools call the generated client's `sync_detailed` entry point, not the higher-level wrappers. `sync_detailed` exposes `status_code` and `content`, which the decoding helpers require.

## Decoding the response

Successful bodies go through the `expect_*` helpers in `_common.py`: `expect_dict`, `expect_list`, `expect_str`. Each takes the action name and the response, checks the status code (default `200`, pass `HTTPStatus.CREATED` and the like when the endpoint differs), decodes the body, asserts its shape with `isinstance`, and raises a `ToolError` otherwise. The generator's `_parse_response` uses `cast(T, response.json())`, a type hint with no runtime effect, so the `isinstance` guard these helpers apply is what stops an unexpected wire shape from propagating as a typed value.

`expect_*` folds in the status check, so a tool that uses them does not call `raise_api_error` itself. Reach for the lower-level `decode` plus `raise_api_error` only when unwrapping a non-standard envelope, for example pulling a single item out of a collection response. Pass `int(response.status_code)` to `raise_api_error`, since the generator types `status_code` as the `HTTPStatus` enum.

## Optional argument forwarding

Optional caller arguments translate to the generated client's `UNSET` sentinel via `to_unset(value)`. Passing `None` directly to a generated-client parameter typed as `T | Unset` is wrong because the generator serialises `None` as JSON `null`, which Mealie rejects on most query parameters.

## List tools

A paginated list tool follows a fixed shape: default `page=1, per_page=50`, call `require_pagination(page, per_page)` first, forward optional `order_by` through `to_unset` and `order_direction` through `parse_order_direction`, and return the raw pagination envelope via `expect_dict`. See `list_shopping_lists` in `households_shopping_lists.py`.

The pagination bound is two-sided, and its job is bounding tool output size, not server politeness. `per_page` is held to `1..100`: the ceiling caps how much a single call returns, and the floor rejects the two low values Mealie mishandles, `-1` (an unbounded "all rows" fetch that defeats the ceiling) and `0` (an empty page). `page` is held to `>= 1`, since Mealie silently coerces `0` to page 1 and reads a negative page as the last page, so an out-of-range value returns a surprising result rather than an error.

## Scoping a list

Do not expose Mealie's generic `queryFilter` expression as a list-scoping input. It is an untyped filter string, error prone for an assistant to build and a poor fit for typed tool inputs. Scope a list with explicit typed parameters instead, and build the `queryFilter` internally if the endpoint needs one. The recipe timeline list, for example, takes a typed `recipe_id` and builds the filter from it.

The rule is scoped to list-scoping inputs. When the filter DSL is the resource's own persisted field rather than a parameter that narrows a result set, exposing it verbatim is correct: `create_cookbook` and `update_cookbook` in `households_cookbooks.py` take `query_filter_string` directly, because a cookbook stores that string as its own definition.

When a tool interpolates a value into a `queryFilter` it builds internally, that value must first be validated to a shape that cannot alter the expression: UUID-parse ids, never interpolate free text. A value carrying a quote or a DSL operator would otherwise change the parsed filter. `list_recipe_timeline_events` UUID-parses `recipe_id` before interpolating it.

## Building a body from caller input

When a tool builds a generated-client body from caller-supplied data with `Model.from_dict(...)`, wrap the call in `try/except (AttributeError, KeyError, TypeError, ValueError)` and re-raise as `ToolError`, so malformed input surfaces as a clean tool error rather than a stack trace. See `update_recipe` in `recipe_crud.py`.

## Delete contract

Every delete tool uses `ack_delete(action, response, ack_id)` so the MCP contract returns the canonical `{"id": <ack_id>, "deleted": True}` shape. A hand-rolled return shape from a delete tool is a deviation.

## Acknowledging an empty-body write

Some write endpoints return no useful body, for example setting a rating or adding a favourite. `ack_delete` is only for deletes. For these, return a small dict echoing the inputs that identify the effect, as `set_recipe_rating` and `add_favorite` in `users_ratings.py` do. Do not invent a wider ack shape.

## Naming and grouping

Tool modules are grouped by Mealie OpenAPI tag, one module per group, mirroring `mealie_mcp.client.api`. Tool names follow `mealie_<verb>_<noun>`. A new tool group is a single new file with a `register(mcp, get_client)` callable; `register_all` auto-discovers it.

A non-underscore module that defines no `register` callable is rejected: `_require_register` raises rather than skipping it, so a group whose tools would never be exposed fails boot instead of vanishing behind a green merge gate. The per-group `call_tool` round-trip (see the live-test rubric) doubles as the registration check for a wired group: it fails if the group's tools are not registered. Together they mean a missing or misnamed `register` cannot ship silently, so a group needs no separate name-presence assertion against `mcp.list_tools()`.

## Update bodies

An update tool's body shape depends on the endpoint's HTTP method and on whether the update model carries fields the tool does not expose. Three variants exist in the code; pick by this ladder.

1. PATCH endpoint means a sparse body is correct. A PATCH applies only the fields present, so send just the caller's edits with no prefetch. `update_recipe` in `recipe_crud.py` builds a `Recipe` from the supplied fields alone and PATCHes it.

2. PUT endpoint where every field of the update model is a tool input means a sparse body with no prefetch. Construct the body directly from the arguments. `update_tag` in `organizer_tags.py` is the exemplar: a small model built from its arguments.

3. PUT endpoint where the update model has fields the tool does not expose means fetch-then-merge. A PUT replaces the resource: any field absent from the body resets to its schema default on the server, so send the full current resource with the caller's edits applied, never a sparse body. Two constructions:
   - `from_dict` merge when the model can absorb the fetched resource, as in `update_shopping_list` (`households_shopping_lists.py`).
   - hand-construction when the update model has required structural fields `from_dict` cannot default, as in `update_mealplan`, which builds `UpdatePlanEntry` field by field (`households_mealplans.py`).

A PUT tool that builds a sparse body silently resets every unexposed field. Its live test must prove the merge holds; see the clobber rule in the live-test rubric.

### The from_dict merge

The pattern, from `update_shopping_list`:

```python
existing = expect_dict("update_x", prefetch)   # route the prefetch through the tool's own action name
body = SomeUpdate.from_dict(existing)
body.additional_properties = {}                # drop keys the model does not declare
body.<field> = <new value>
```

`from_dict` carries every key of the fetched resource, including server-only keys the update model does not declare, into `additional_properties`; clearing it stops those keys being echoed back on the PUT. Assign only the fields the tool exposes; everything else round-trips from `existing` and survives the replace.

`from_dict` consumes wire-format camelCase keys. An unknown or wrong-cased key is not rejected. It is silently absorbed into `additional_properties` and sets nothing, so a snake_case or mistyped key fails quietly. When translating caller field names to the wire, map them explicitly; `_UPDATE_RECIPE_FIELD_MAP` in `recipe_crud.py` is the snake-to-camel precedent.

### None means "not supplied"

Update tools use `None` as the "field not supplied" sentinel and skip it, so a nullable field cannot be cleared through the tool surface. The docstring says clearing is unsupported. If a task genuinely needs to clear a text field, the escape hatch is treating an empty string as "clear" for that field, decided per tool.
