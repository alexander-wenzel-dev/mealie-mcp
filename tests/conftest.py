"""Shared pytest configuration.

Loads a checkout-local `.env` once at collection time so live tests (and any
unit test that touches the config loader) see the same values the operator
configured for the server.
"""

from __future__ import annotations

from dotenv import load_dotenv

load_dotenv()
