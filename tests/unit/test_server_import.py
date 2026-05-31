from fastmcp import FastMCP

from mealie_mcp import server


def test_server_module_exposes_fastmcp_instance() -> None:
    assert isinstance(server.mcp, FastMCP)
