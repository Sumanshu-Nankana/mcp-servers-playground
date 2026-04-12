import logging
import sys
from fastmcp import FastMCP
from tools import (
    save_memory,
    search_memory,
    list_memories,
    delete_memory,
    delete_all_memories,
)
from prompts import memory_assistant_prompt

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

mcp = FastMCP("MemoryMCP")

# register tools
mcp.tool(save_memory)
mcp.tool(search_memory)
mcp.tool(list_memories)
mcp.tool(delete_memory)
mcp.tool(delete_all_memories)

# register prompt
mcp.prompt(memory_assistant_prompt)

if __name__ == "__main__":
    logger.info("Starting MemoryMCP server")
    mcp.run()
