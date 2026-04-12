import uuid
from datetime import datetime
import logging
from storage import get_or_create_collection, chroma_client
from config import COLLECTION_NAME, DEFAULT_N_RESULTS

logger = logging.getLogger(__name__)


def save_memory(memory: str):
    """Save a memory string to the vector store"""
    logger.info(f"Saving memory: {memory[:50]}...")
    collection = get_or_create_collection()
    memory_id = str(uuid.uuid7())
    collection.add(
        documents=[memory],
        ids=[memory_id],
        metadatas=[{"timestamp": datetime.now().isoformat()}],
    )
    logger.info(f"Memory saved with id: {memory_id}")
    return {"status": "saved", "id": memory_id}


def search_memory(query: str, n_results: int = DEFAULT_N_RESULTS) -> dict:
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


def delete_all_memories() -> dict:
    """Delete all memories"""
    chroma_client.delete_collection(COLLECTION_NAME)
    return {"status": "all memories deleted"}


def delete_memory(memory_id: str) -> dict:
    """Delete a specific memory by ID
    IMPORTANT: If you don't have the memory_id,
    first call search_memory or list_memories to find it,
    then call delete_memory with the correct ID."""
    collection = get_or_create_collection()
    collection.delete(ids=[memory_id])
    return {"status": "deleted", "id": memory_id}
