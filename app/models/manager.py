"""
This module contains functions for managing Qdrant collections.
"""
from typing import List, Optional

from api.logging_theme import setup_logger
from langchain_qdrant.qdrant import QdrantVectorStore


class Manager:
    """
    This class contains functions for managing Qdrant collections.
    """
    def __init__(self, collection_name: str):
        """
        Initialize the Manager with a collection name.

        Args:
            collection_name (str): The name of the Qdrant collection to manage.
        """
        self.collection_name = collection_name
        self.logger = setup_logger(__name__)

    def delete(self, ids: Optional[List[str]] = None) -> bool:
        """
        Delete documents from a Qdrant collection by their IDs.

        Args:
            ids (Optional[List[str]]): List of document IDs to delete. If None, no documents will be deleted.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            self.logger.info(f"Connecting to Qdrant collection: {self.collection_name}")
            vector_store = QdrantVectorStore.from_existing_collection(
                collection_name=self.collection_name,
                url="http://qdrant:6333/", 
                prefer_grpc=True
            )

            self.logger.info(f"Deleting documents with IDs: {ids}")
            vector_store.delete(ids=ids)
            self.logger.info("Documents deleted successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting documents from collection {self.collection_name}: {e}", exc_info=True)
            return False
