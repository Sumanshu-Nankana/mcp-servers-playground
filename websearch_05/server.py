from fastmcp import FastMCP
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


mcp = FastMCP(name="websearch")
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1"
)


@mcp.tool
def perform_websearch(query: str) -> str:
    """
    Performs a web search on a query
    Args:
        query (str): The query to web search
    """

    messages = [
        # {
        #     "role": "system",
        #     "content": "You are an AI assistant that searches the web and responds to the query",
        # },
        {
            "role": "user",
            "content": query,
        }
    ]

    completion = client.chat.completions.create(
        messages=messages,
        model="groq/compound-mini",
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    mcp.run()
