"""
This module contains functions to ingest data into Qdrant collection.
"""
from typing import List

from langchain_core.documents import Document as LangchainDocument
from langchain_qdrant import QdrantVectorStore, RetrievalMode

from api.logging_theme import setup_logger
from utils.configs import embeddings, spare_embeddings

class IngestionPipeline:
    """
    Define Ingestion Pipeline
    """
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.logger = setup_logger(__name__)

    async def ingest_data(self, chunks: List[LangchainDocument]):
        """
        Ingest data into collection.
        Args:
            chunks (List[LangchainDocument]): List of LangchainDocuments chunks

        Returns:
            bool: True if collection was successfully ingested else False
        """
        try:
            # Init Vector store
            await QdrantVectorStore.afrom_documents(
                documents=chunks,
                embedding=embeddings,
                sparse_embedding=spare_embeddings,
                url="http://qdrant:6333/",
                prefer_grpc=True,
                collection_name=self.collection_name,
                retrieval_mode=RetrievalMode.HYBRID
            )
            self.logger.info(f"Successfully ingest into Qdrant collection: {self.collection_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error ingesting data into Qdrant collection: {str(e)}")
            raise ValueError(f"Error ingesting data into Qdrant collection: {str(e)}")