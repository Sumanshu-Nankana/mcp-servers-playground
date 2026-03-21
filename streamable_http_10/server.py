from fastmcp import FastMCP

mcp = FastMCP(name="streamable_http")


@mcp.tool
def greetings(name: str) -> str:
    """
    Send a Greeting
    Args:
        name: name of the person to greet
    """
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
