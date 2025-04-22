"""
Chunking module for chunking text and table data from .docx files.
"""

from io import BytesIO
from pathlib import Path
from typing import List

from fastapi import UploadFile, File
from langchain_core.documents.base import Document as LangchainDocument
from unstructured.chunking.title import chunk_by_title
from unstructured.partition.docx import partition_docx

from api.logging_theme import setup_logger
from domain.ingestion.docx_parsing import DocxParser


class ChunkProcessor:
    """
    Define Chunk Processor
    """

    def __init__(self):
        self.all_chunks: List[LangchainDocument] = []
        self.logger = setup_logger(__name__)

    def chunk_table(self, table_content: str, table_description: str, header_rows: int = 1, chunk_size: int = 10,
                    page_number: int = 0) -> List[LangchainDocument]:
        """
        Chunk a table by keeping the header rows and adding chunks of data rows.
        
        Args:
            table_content (str): TSV-formatted table content
            table_description (str): Description of the table
            header_rows (int): Number of rows to treat as header
            chunk_size (int): Number of data rows per chunk
            page_number (int): Page number of the document where the table appears
            
        Returns:
            List[LangchainDocument]: List of chunks as LangchainDocument objects
        """
        table_chunks = []

        # Split the TSV content into rows
        rows = table_content.strip().split('\n')

        # Check if there are enough rows for headers
        if len(rows) <= header_rows:
            # If table is too small, just return it as a single chunk
            return [LangchainDocument(
                page_content=f"Miêu tả nội dung bảng: {table_description}\n{table_content}",
                metadata={"page_number": page_number, "content_type": "table"}
            )]

        # Extract header rows
        headers = rows[:header_rows]
        header_content = '\n'.join(headers)

        # Get data rows
        data_rows = rows[header_rows:]

        # Create chunks with header + chunk_size data rows
        for i in range(0, len(data_rows), chunk_size):
            chunk_data_rows = data_rows[i:i + chunk_size]
            chunk_content = f"{header_content}\n" + '\n'.join(chunk_data_rows)

            table_chunks.append(LangchainDocument(
                page_content=f"Miêu tả nội dung bảng: {table_description}\n{chunk_content}",
                metadata={
                    "page_number": page_number,
                    "content_type": "table",
                    "chunk_index": i // chunk_size,
                    "total_chunks": (len(data_rows) + chunk_size - 1) // chunk_size
                }
            ))

        return table_chunks

    async def chunking(self, file: UploadFile = File(...), header_rows: int = 1,
                       table_chunk_size: int = 10) -> List[LangchainDocument]:
        """
        Chunking for text and table asynchronously
        Args:
            file (UploadFile): file to chunk
            header_rows (int): Number of rows to treat as header in tables
            table_chunk_size (int): Number of data rows per table chunk

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
        doc_parser = DocxParser()
        elements = partition_docx(
            file=buf,
            infer_table_structure=True,
        )

        # Process text chunks
        chunks_text = [
            LangchainDocument(
                page_content=chunk.text,
                metadata={
                    "page_number": chunk.metadata.page_number,
                    "content_type": "text"
                }
            )
            for chunk in chunk_by_title([element for element in elements if element.metadata.text_as_html is None],
                                        max_characters=512, combine_text_under_n_chars=0, overlap=100,
                                        overlap_all=True)
        ]

        # Process table chunks
        chunks_table = []
        for i, element in enumerate(elements):
            if element.metadata.text_as_html is not None:
                # Get table description from previous element if available
                table_description = elements[i - 1].text if i > 0 else ""

                # Convert table to TSV format
                table_tsv = doc_parser.convert_table_to_tsv_string(str(element.metadata.text_as_html))

                # Chunk the table
                table_chunks = self.chunk_table(
                    table_tsv,
                    table_description,
                    header_rows=header_rows,
                    chunk_size=table_chunk_size,
                    page_number=element.metadata.page_number
                )

                chunks_table.extend(table_chunks)

        # Store all chunks
        self.all_chunks.extend(chunks_text)
        self.all_chunks.extend(chunks_table)
        self.logger.info(f"Chunking completed successfully. Total chunks: {len(self.all_chunks)}")
        return self.all_chunks

