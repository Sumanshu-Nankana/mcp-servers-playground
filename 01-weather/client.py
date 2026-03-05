from fastmcp import Client
import asyncio

client = Client("server.py")


async def main():
    try:
        async with client:
            print("Starting client...")
            # Basic Server interaction
            await client.ping()

            # List available operations
            print("Listing tools...")
            tools = await client.list_tools()
            print("Available tools:", tools)

            # Execute operations
            print("Calling tool...")
            result = await client.call_tool("get_weather", {"location": "USA"})
            print(result)
    except Exception as e:
        print("Error occurred:", e)


if __name__ == "__main__":
    asyncio.run(main())
