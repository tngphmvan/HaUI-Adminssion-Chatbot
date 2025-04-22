"""
This module contains the IngestionManager class, which is responsible for managing the ingestion of documents into the Qdrant collection.
"""
from typing import List, Any

from fastapi import UploadFile, File
from langchain_core.documents.base import Document as LangchainDocument

from api.logging_theme import setup_logger
from domain.ingestion.chunking import ChunkProcessor
from domain.ingestion.docx_parsing import DocxParser
from domain.ingestion.indexing import IngestionPipeline


class IngestionManager:
    """
    Object-oriented manager for document ingestion.
    """
    def __init__(self, collection_name: str, header_rows: int):
        self.collection_name = collection_name
        self.logger = setup_logger(__name__)
        self.header_rows = header_rows

    async def ingest(self, file: UploadFile = File(...)) -> (bool, list):
        """
        Ingests documents from uploaded files into the specified collection.

        Args:
            file (UploadFile): List of uploaded files.

        Returns:
            Any: Result of the ingestion process.
        """
        chunks: List[LangchainDocument] = await ChunkProcessor().chunking(file, header_rows=self.header_rows)
        try:
            status, ids = await IngestionPipeline(collection_name=self.collection_name).ingest_data(chunks=chunks)
            self.logger.info("Ingestion of documents into collection successfully")
            return status, ids
        except Exception as e:
            self.logger.error(f"Error ingesting data into Qdrant collection {e}")
            raise ValueError(f"Error ingesting data into Qdrant collection {e}")

    async def ingest_faq(self, file: UploadFile = File(...)) -> Any:
        """
        Ingests FAQ documents from uploaded files into the specified collection.

        Args:
            file (UploadFile): List of uploaded files.

        Returns:
            Any: Result of the ingestion process.
        """
        chunks: List[LangchainDocument] = await DocxParser().faq_parsing(file)
        try:
            status, ids = await IngestionPipeline(collection_name=self.collection_name).ingest_data(chunks=chunks)
            self.logger.info(f"Ingestion of faq into collection successfully")
            return status, ids
        except Exception as e:
            self.logger.error(f"Error ingesting FAQ data into Qdrant collection {e}")
            raise ValueError(f"Error: {e}")