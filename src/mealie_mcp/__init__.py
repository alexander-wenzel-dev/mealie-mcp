"""Mealie MCP package.

Avoid importing submodules eagerly so the `regen-client` script can run even
when the generated client folder does not yet exist.

A checkout-local `.env` is loaded once at package import so every entry point
(server, regen-client, tests) sees the same environment without bespoke
loaders. Existing env vars are never overridden.
"""

from dotenv import load_dotenv

load_dotenv()
