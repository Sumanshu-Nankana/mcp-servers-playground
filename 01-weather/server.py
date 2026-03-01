from fastmcp import FastMCP


mcp = FastMCP(name="weather")


@mcp.tool
def get_weather(location: str) -> str:
    """
    Get weather data for a given location
    Args:
       location (str): location can be a city, state or country etc
    """
    return "The weather is hot and dry"


if __name__ == "__main__":
    mcp.run()
