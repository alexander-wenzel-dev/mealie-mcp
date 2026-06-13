---
paths:
  - "src/mealie_mcp/tools/**"
---

# Tool implementation rubric

Detailed rules for MCP tool work in this repo. The generated client under `src/mealie_mcp/client/` is out of scope: it is regenerated from the OpenAPI spec and not hand-edited.

## Two-layer structure

Each MCP tool is two layers:

1. A typed module-level function taking `AuthenticatedClient` and the tool inputs. This is the testable unit.
2. A thin `@mcp.tool()` wrapper inside `register(mcp, get_client)`. The wrapper calls `get_client()` (the process-scoped singleton from `mealie_mcp.client_factory`) and forwards to the typed function.

Do not collapse the layers, put business logic in the wrapper, or call the generated client from the wrapper instead of the typed function.

## Validation

Input validation uses `require_non_empty` from `_common.py`. Inline `if not value: raise ...` for the same shape is a deviation.

## Generated client call

Tools call the generated client's `sync_detailed` entry point, not the higher-level wrappers. `sync_detailed` exposes `status_code` and `content`, which the error-mapping and decoding helpers require. A call to a non-`sync_detailed` variant loses error access.

## Error mapping

Non-success responses go through `raise_api_error` from `_common.py`. Status codes are compared with `HTTPStatus` constants. `response.status_code` is cast to `int` when forwarded to `raise_api_error`, since the generator types `status_code` as the `HTTPStatus` enum and `raise_api_error` expects `int`.

## Body decoding and shape guards

Successful bodies are decoded with `decode` from `_common.py`. Decoded values get explicit `isinstance` shape guards before being returned. The generator's `_parse_response` uses `cast(T, response.json())`, which is a type hint with no runtime effect. Without the `isinstance` guard, an unexpected wire shape silently propagates as a typed value.

## Optional argument forwarding

Optional caller arguments translate to the generated client's `UNSET` sentinel via `to_unset(value)`. Passing `None` directly to a generated-client parameter typed as `T | Unset` is wrong because the generator serialises `None` differently from `UNSET`.

## Delete contract

Every delete tool uses `ack_delete(action, response, ack_id)` so the MCP contract returns the canonical `{"id": <ack_id>, "deleted": True}` shape. A hand-rolled return shape from a delete tool is a deviation.

## Naming and grouping

Tool modules are grouped by Mealie OpenAPI tag, one module per group, mirroring `mealie_mcp.client.api`. Tool names follow `mealie_<verb>_<noun>`. A new tool group is a single new file with a `register(mcp, get_client)` callable; `register_all` auto-discovers it.

## Fetch-then-merge for PUT-replace bodies

Mealie's update endpoints PUT-replace the resource. If the tool exposes only some body fields, and the body model carries other fields (whether they default to `UNSET` or to a concrete value), the implementation must fetch the current resource, merge the caller's edits, and send the full body. Without fetch-then-merge, unexposed fields silently reset to schema defaults on every update, because non-`UNSET` defaults serialise into the request and `UNSET` defaults still expose the field to PUT-replace.
