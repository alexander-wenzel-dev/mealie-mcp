"""FastMCP server entry point for the Mealie MCP."""

from __future__ import annotations

from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
from starlette.requests import Request
from starlette.responses import JSONResponse

from mealie_mcp.client_factory import get_client
from mealie_mcp.config import load_transport_config
from mealie_mcp.tools import register_all

mcp: FastMCP = FastMCP("mealie-mcp")
register_all(mcp, get_client)


@mcp.custom_route("/health", methods=["GET"])
async def health(_request: Request) -> JSONResponse:
    """Liveness probe for orchestrators. No token, no upstream call."""
    return JSONResponse({"status": "ok"})


def build_auth(token: str) -> StaticTokenVerifier:
    """Return a bearer-token verifier accepting the single configured token."""
    return StaticTokenVerifier(tokens={token: {"client_id": "mealie-mcp"}})


def main() -> None:
    load_dotenv()
    cfg = load_transport_config()
    if cfg.transport == "stdio":
        mcp.run()
        return
    mcp.auth = build_auth(cfg.auth_token)
    mcp.run(
        transport="http",
        host=cfg.host,
        port=cfg.port,
        host_origin_protection=True,
        allowed_hosts=list(cfg.allowed_hosts),
    )


if __name__ == "__main__":
    main()
