import json

from fastmcp import Client
from fastmcp.client.transports import StdioTransport
import asyncio
import logging
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


logger = logging.getLogger(__name__)

llm_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1"
)

server_params = StdioTransport(
    command="uv",
    args=[
        "--directory",
        "C:\\Users\\suman\\OneDrive\\Desktop\\mcp-servers-playground\\mcp_client_11",
        "run",
        "server.py",
    ],
)


async def run(query):
    try:
        print("Starting MCP STDIO Client...")
        async with Client(server_params) as client:
            await client.ping()
            print("MCP Stdio client connected with MCP Server...")

            print("\nListing tools...")
            tools_result = await client.list_tools()
            print("Available tools:", tools_result)

            # OpenAI accepts tools in specific format, not the MCP format
            # https://developers.openai.com/api/docs/guides/function-calling
            openai_tools = []
            for tool in tools_result:
                tool_details = {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema,
                    },
                }
                openai_tools.append(tool_details)

            messages = [{"role": "user", "content": query}]

            response = llm_client.chat.completions.create(
                messages=messages,
                tools=openai_tools,
                tool_choice="auto",
                model="llama-3.3-70b-versatile",
            )

            messages.append(response.choices[0].message)

            if response.choices[0].message.tool_calls:
                for tool_execution in response.choices[0].message.tool_calls:
                    result = await client.call_tool(
                        tool_execution.function.name,
                        arguments=json.loads(tool_execution.function.arguments),
                    )

                    # Append Tool output to the messages which will be passed to model
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_execution.id,
                            "content": result.content[0].text,
                        }
                    )
            else:
                return response.choices[0].message.content

            response = llm_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                tools=openai_tools,
                tool_choice="auto",
            )

            return response.choices[0].message.content

    except Exception as e:
        print("Some error occurred")
        logger.exception(e)


if __name__ == "__main__":
    query = (
        "Please add the Book FastMCP-Tutorial whose author is MCP into my collections"
    )
    output = asyncio.run(run(query))
    print("\nUser will see this output: ", output)
