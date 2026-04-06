from fastmcp import FastMCP
import chromadb
from chromadb.utils import embedding_functions
from datetime import datetime
import uuid

COLLECTION_NAME = "MEMORIES"

mcp = FastMCP("MemoryMCP")
chroma_client = chromadb.PersistentClient(path="./memory_store")

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


def get_or_create_collection():
    """Get existing collection or create a new one"""
    return chroma_client.get_or_create_collection(
        name=COLLECTION_NAME, embedding_function=ef
    )


@mcp.tool
def save_memory(memory: str):
    """Save a memory string to the vector store"""
    collection = get_or_create_collection()
    memory_id = str(uuid.uuid7())
    collection.add(
        documents=[memory],
        ids=[memory_id],
        metadatas=[{"timestamp": datetime.now().isoformat()}],
    )

    return {"status": "saved", "id": memory_id}


@mcp.tool
def search_memory(query: str, n_results: int = 3) -> dict:
    """Search memories in the vector store and return relevant chunks"""
    collection = get_or_create_collection()
    result = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    if not result["documents"] or not result["documents"][0]:
        return {"results": []}

    memories = []
    for doc, meta, distance in zip(
        result["documents"][0], result["metadatas"][0], result["distances"][0]
    ):
        memories.append(
            {
                "memory": doc,
                "timestamp": meta.get("timestamp", "unknown") if meta else "unknown",
                "relevance_score": round(1 - distance, 3),
            }
        )
    return {"results": memories}


@mcp.tool
def list_memories() -> dict:
    """List all saved memories"""
    collection = get_or_create_collection()
    result = collection.get()
    if not result["documents"]:
        return {"memories": [], "count": 0}
    memories = []
    for id, doc, meta in zip(result["ids"], result["documents"], result["metadatas"]):
        memories.append(
            {"id": id, "memory": doc, "timestamp": meta.get("timestamp", "unknown")}
        )

    return {"memories": memories, "count": len(memories)}


@mcp.tool
def delete_all_memories() -> dict:
    """Delete all memories"""
    chroma_client.delete_collection(COLLECTION_NAME)
    return {"status": "all memories deleted"}


@mcp.tool
def delete_memory(memory_id: str) -> dict:
    """Delete a specific memory by ID
    IMPORTANT: If you don't have the memory_id,
    first call search_memory or list_memories to find it,
    then call delete_memory with the correct ID."""
    collection = get_or_create_collection()
    collection.delete(ids=[memory_id])
    return {"status": "deleted", "id": memory_id}


@mcp.prompt
def memory_assistant() -> str:
    """Get help with memory operations and best practices"""
    return """You are using MemoryMCP for long-term memory management.

How to use:
- save_memory: Save facts, preferences, or anything user wants remembered
- search_memory: Semantic search before answering any question
- list_memories: Browse all saved memories
- delete_memory: Remove a specific memory (find ID via search/list first)
- delete_all_memories: Clear everything

Best practices:
- ALWAYS search memories before answering user questions
- Save any preference or fact the user mentions
- When user says "remember that..." always call save_memory
- When deleting specific memory, first search/list to find the ID"""


if __name__ == "__main__":
    mcp.run()
