from fastmcp import FastMCP

mcp = FastMCP(name="prompt")


@mcp.prompt
def analyze_topic(topic: str) -> str:
    """
    Returns the prompt that will do a detailed analysis on a topic
    Args:
       topic (str): The topic to analyze
    """
    return f"Do a detailed analysis on the following topic: {topic}"


@mcp.prompt
def write_detailed_historical_report(topic: str, number_of_paragraphs: int) -> str:
    """
    Writes a detailed historical report for the topic
    Args:
        topic (str): The topic to analyze
        number_of_paragraphs (int): The number of paragraphs in the topic
    """
    prompt = f"""
    Create a concise research report on the history of {topic}.
    The report should contain three sections: INTRODUCTION. MAIN. AND CONCLUSION.
    The MAIN section should be {number_of_paragraphs} paragraphs long.
    Include a timeline of key events.
    The conclusion should be in bullet points format.
    """

    return prompt


if __name__ == "__main__":
    mcp.run()
