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

A paginated list tool follows a fixed shape: default `page=1, per_page=50`, call `require_per_page(per_page)` first (the shared ceiling is 100), forward optional `order_by` through `to_unset` and `order_direction` through `parse_order_direction`, and return the raw pagination envelope via `expect_dict`. See `list_shopping_lists` in `households_shopping_lists.py`.

## Building a body from caller input

When a tool builds a generated-client body from caller-supplied data with `Model.from_dict(...)`, wrap the call in `try/except (AttributeError, KeyError, TypeError, ValueError)` and re-raise as `ToolError`, so malformed input surfaces as a clean tool error rather than a stack trace. See `update_recipe` in `recipe_crud.py`.

## Delete contract

Every delete tool uses `ack_delete(action, response, ack_id)` so the MCP contract returns the canonical `{"id": <ack_id>, "deleted": True}` shape. A hand-rolled return shape from a delete tool is a deviation.

## Naming and grouping

Tool modules are grouped by Mealie OpenAPI tag, one module per group, mirroring `mealie_mcp.client.api`. Tool names follow `mealie_<verb>_<noun>`. A new tool group is a single new file with a `register(mcp, get_client)` callable; `register_all` auto-discovers it.

## Fetch-then-merge for PUT-replace bodies

Mealie's update endpoints PUT-replace the resource: any field absent from the request body resets to its schema default on the server. So an update tool that exposes only some fields must send the full current resource with the caller's edits applied, never a sparse body.

The pattern, from `update_shopping_list` in `households_shopping_lists.py`:

```python
existing = expect_dict("update_x", prefetch)   # route the prefetch through the tool's own action name
body = SomeUpdate.from_dict(existing)
body.additional_properties = {}                # drop keys the model does not declare
body.<field> = <new value>
```

`from_dict` carries every key of the fetched resource, including server-only keys the update model does not declare, into `additional_properties`; clearing it stops those keys being echoed back on the PUT. Assign only the fields the tool exposes; everything else round-trips from `existing` and survives the replace.

A tool that builds a sparse body instead silently resets every unexposed field. The live test for the tool must prove the merge holds; see the clobber rule in the live-test rubric.
