from fastmcp import FastMCP

mcp = FastMCP(name="books")

books = [
    {"id": "1", "title": "The Pragmatic Programmer", "author": "David Thomas"},
    {
        "id": "2",
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
    },
    {"id": "3", "title": "Python Crash Course", "author": "Eric Matthes"},
]


@mcp.tool
def add_book(title: str, author: str) -> str:
    """Add a new book to the collection"""
    books.append({"id": str(len(books) + 1), "title": title, "author": author})
    return f"Book '{title}' added successfully."


@mcp.resource(uri="books://all")
def get_all_books() -> str:
    """Returns all books"""
    result = ""
    for b in books:
        result += f"ID:{b['id']} | {b['title']} by {b['author']}\n"
    return result


@mcp.resource(uri="books://{book_id}")
def get_book_by_id(book_id: str) -> str:
    """Returns a specific book by ID"""
    for b in books:
        if b["id"] == book_id:
            return f"{b['title']} by {b['author']}"
    return f"Book {book_id} not found"


@mcp.prompt
def book_recommendation_prompt() -> str:
    """Prompt to get book recommendations"""
    return "Based on my book collection, recommend 3 similar books I might enjoy and explain why."


if __name__ == "__main__":
    mcp.run()
