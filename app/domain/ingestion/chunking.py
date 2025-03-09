"""
Chunking module for chunking text and table data from .docx files.
"""

from io import BytesIO
from pathlib import Path
from typing import List

from docling.datamodel.base_models import DocumentStream, InputFormat
from docling.document_converter import DocumentConverter, WordFormatOption
from docling_core.transforms.chunker import HierarchicalChunker
from fastapi import UploadFile, File
from langchain_core.documents.base import Document as LangchainDocument

from api.logging_theme import setup_logger


class ChunkProcessor:
    """
    Define Chunk Processor
    """

    def __init__(self):
        self.all_chunks: List[LangchainDocument] = []
        self.logger = setup_logger(__name__)

    async def chunking(self, file: UploadFile = File(...)) -> List[LangchainDocument]:
        """
        Chunking for text and table asynchronously
        Args:
            file (UploadFile): file to chunk

        Returns:
            list: list of chunks

        Raises:
            ValueError: If file type is not supported or processing fails
        """

        if not file:
            self.logger.error("No files provided for chunking")
            raise ValueError("No files provided for chunking")

        self.logger.info(f"Processing file: {file.filename}")

        if not file.filename:
            self.logger.error("Empty filename detected")
            raise ValueError("Empty filename detected")

        file_extension = Path(file.filename).suffix.lower()
        if file_extension != '.docx':
            self.logger.error(f"Unsupported file type: {file_extension}. Only .docx files are supported")
            raise ValueError(f"Unsupported file type: {file_extension}. Only .docx files are supported")

        # Create task async for file

        buf = BytesIO(await file.read())
        source = DocumentStream(name=file.filename, stream=buf)
        pipline_options = WordFormatOption()
        coverter = DocumentConverter(
            format_options={
                InputFormat.DOCX: WordFormatOption(pipline_options=pipline_options)
            }
        )
        doc = coverter.convert(source=source).document
        chunker = HierarchicalChunker()
        chunk_iter = chunker.chunk(doc)
        chunks = [
            LangchainDocument(
                page_content=chunker.serialize(chunk=chunk),
                metadata={"file_path": file.filename}
            )
            for chunk in chunk_iter
        ]

        # Store all chunks
        self.all_chunks.extend(chunks)
        self.logger.info(f"Chunking completed successfully. Total chunks: {len(self.all_chunks)}")
        return self.all_chunks
