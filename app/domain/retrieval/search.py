"""
This module contains a class for performing semantic search on Qdrant.
"""
from langchain_core.vectorstores import VectorStoreRetriever

from api.logging_theme import setup_logger
from domain.retrieval.vectorstores import VectorStore


class SearchEngine:
    """
    This class contains functions for performing semantic search on Qdrant.
    """
    def __init__(self, collection_name: str, k: int = 5):
        self.collection_name = collection_name
        self.k = k
        self.logger = setup_logger(__name__)

    def semantic_search(self) -> VectorStoreRetriever:
        """
        Perform semantic search on Qdrant.

        Returns:
            VectorStoreRetriever: A retriever configured for semantic similarity search.
        """
        try:
            vectorstore = VectorStore(collection_name=self.collection_name).get_vectorstore()
            self.logger.info(f"Retrieved vectorstore successfully created for collection {self.collection_name} with k={self.k}")
        except Exception as e:
            self.logger.error(f"Error retrieving vectorstore for collection {self.collection_name}: {e}")
            raise ValueError(f"Error retrieving vectorstore for collection {self.collection_name}: {e}")

        try:
            return vectorstore.as_retriever(search_kwargs={"k": self.k})
        except Exception as e:
            self.logger.error(f"Error creating retriever for collection {self.collection_name} with k={self.k}: {e}")
            raise ValueError(f"Error creating retriever for collection {self.collection_name} with k={self.k}: {e}")