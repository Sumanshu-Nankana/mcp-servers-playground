import chromadb
from chromadb.utils import embedding_functions
from config import COLLECTION_NAME, MEMORY_STORE_PATH, EMBEDDING_MODEL
import logging

logger = logging.getLogger(__name__)

chroma_client = chromadb.PersistentClient(path=MEMORY_STORE_PATH)
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)


def get_or_create_collection():
    """Get existing collection or create a new one"""
    logger.info(f"Getting or creating collection: {COLLECTION_NAME}")
    return chroma_client.get_or_create_collection(
        name=COLLECTION_NAME, embedding_function=ef
    )
