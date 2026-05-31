"""FastMCP server entry point for the Mealie MCP."""

from __future__ import annotations

from fastmcp import FastMCP

from mealie_mcp.tools import register_all

mcp: FastMCP = FastMCP("mealie-mcp")
register_all(mcp)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
