from fastmcp import FastMCP
from datetime import datetime


mcp = FastMCP(name="time-tool")


@mcp.tool
def get_current_time() -> str:
    """Returns the current date and time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
