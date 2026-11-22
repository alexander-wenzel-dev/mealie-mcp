"""Input-validation tests for the household self-service tools.

The Mealie HTTP contract is exercised by `tests/live/test_households_self_service.py`;
shared helper behaviour lives in `tests/unit/test_common.py`.
"""

from __future__ import annotations

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import households_self_service


@pytest.fixture
def client() -> AuthenticatedClient:
    """Client whose HTTP path is never reached because validation raises first."""
    return AuthenticatedClient(base_url="https://mealie.example.com", token="t")


class TestGetHouseholdRecipe:
    def test_rejects_empty_slug_or_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="slug_or_id must be a non-empty string"):
            households_self_service.get_household_recipe(client, slug_or_id="  ")
