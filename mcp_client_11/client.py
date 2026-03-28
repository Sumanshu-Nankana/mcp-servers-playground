from fastmcp import Client
from fastmcp.client.transports import StdioTransport
import asyncio
import logging


logger = logging.getLogger(__name__)


server_params = StdioTransport(command="uv", args=["run", "server.py"])


async def main():
    try:
        print("Starting MCP STDIO Client...")
        async with Client(server_params) as client:
            await client.ping()
            print("MCP Stdio client connected with MCP Server...")

            print("\nListing tools...")
            tools = await client.list_tools()
            print("Available tools:", tools)

            print("\nCalling tool...")
            result = await client.call_tool(
                name="add_book", arguments={"title": "MI and AL", "author": "Apple Co."}
            )
            print("Tool Results:", result)

            print("\nListing Resources...")
            resources = await client.list_resources()
            print("Available resources:", resources)

            print("\nRead Resource...")
            resource = await client.read_resource(uri="books://all")
            print("Resource Results:", resource)

            print("\nListing resources templates...")
            resources = await client.list_resource_templates()
            print("Available resources templates:", resources)

            print("\nRead Resource Template...")
            resource = await client.read_resource(uri="books://1")
            print("Resource Results:", resource)

            print("\nListing Prompts...")
            prompts = await client.list_prompts()
            print("Available prompts:", prompts)

            print("\nGet Prompt..")
            prompt = await client.get_prompt(name="book_recommendation_prompt")
            print("Prompt Results:", prompt)

    except Exception as e:
        print("Some error occurred")
        logger.exception(e)


if __name__ == "__main__":
    asyncio.run(main())
