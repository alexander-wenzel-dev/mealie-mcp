"""FastMCP server entry point for the Mealie MCP."""

from __future__ import annotations

from dotenv import load_dotenv
from fastmcp import FastMCP

from mealie_mcp.client_factory import get_client
from mealie_mcp.tools import register_all

mcp: FastMCP = FastMCP("mealie-mcp")
register_all(mcp, get_client)


def main() -> None:
    load_dotenv()
    mcp.run()


if __name__ == "__main__":
    main()
