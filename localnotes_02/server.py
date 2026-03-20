from fastmcp import FastMCP


mcp = FastMCP(name="LocalNotes")


@mcp.tool
def add_note_to_file(content: str) -> str:
    """
    Appends the given content to the user's local notes.
    Args:
        content: the text content to add
    """

    filename = "notes.txt"
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(content + "\n")

        return f"Content added to {filename}."
    except Exception as e:
        return f"Error adding content to {filename} : {e}."


@mcp.tool
def read_notes() -> str:
    """
    Read and returns the contents of the users local notes file.
    """

    filename = "notes.txt"

    try:
        with open(filename, "r", encoding="utf-8") as f:
            notes = f.read()
        return notes if notes else "No notes found."
    except FileNotFoundError:
        return "No notes file found."
    except Exception as e:
        return f"Error reading notes from {filename} : {e}."


if __name__ == "__main__":
    mcp.run()
