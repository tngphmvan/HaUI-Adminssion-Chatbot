"""Define Ingestion Pipeline"""

import uuid
from typing import List, Any

from langchain_core.documents.base import Document as LangchainDocument

from app.domain.ingestion.chunking import table_chunking, title_chunking
from app.domain.ingestion.docx_parsing import read_docx
from app.domain.ingestion.indexing import ingest_data, create_collection


def ingest(collection_name: str, file_path: str, source: str) -> List[Any] | None:
    """

    Args:
        collection_name:
        file_path:
        source:

    Returns:

    """
    markdown_content, text_content, table_content = read_docx(file_path)

    res: List[Any] = []

    for table in table_content:
        for chunk in table_chunking(table):
            res.append(
                LangchainDocument(page_content=chunk,
                                  metadata={"heading": "table", "id": str(uuid.uuid4()), "source": source}))

    for chunk in title_chunking(markdown_content):
        chunk.metadata["id"] = str(uuid.uuid4())
        chunk.metadata["source"] = source
        res.append(chunk)

    try:
        ingest_data(collection_name=collection_name, chunks=res)
        return res
    except Exception as e:
        print(e)