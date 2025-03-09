"""
This module contains functions to connect to Qdrant with a specific collection.
"""
from langchain_qdrant import QdrantVectorStore, RetrievalMode

from api.logging_theme import setup_logger
from utils.configs import embeddings, spare_embeddings


class VectorStore:
    """
    This class contains functions to connect to Qdrant with a specific collection.
    """
    def __init__(self, collection_name):
        self.logger = setup_logger(__name__)
        self.collection_name: str = collection_name


    def get_vectorstore(self) -> QdrantVectorStore:
        """
        Connect to Qdrant with a specific collection.

        Args:

        Returns:
            QdrantVectorStore: The connected Qdrant vector store.
        """
        try:
            self.logger.info(f"Connecting to Qdrant collection: {self.collection_name}")
            vectorstore = QdrantVectorStore.from_existing_collection(
                collection_name=self.collection_name,
                url="http://localhost:6333/",
                prefer_grpc=True,
                embedding=embeddings,
                retrieval_mode=RetrievalMode.HYBRID,
                sparse_embedding=spare_embeddings
            )
            self.logger.info("Successfully connected to Qdrant collection")
            return vectorstore
        except Exception as e:
            self.logger.error(f"Failed to connect to Qdrant collection: {e}")
            raise
