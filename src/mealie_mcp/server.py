from fastmcp import FastMCP

mcp: FastMCP = FastMCP("mealie-mcp")


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
