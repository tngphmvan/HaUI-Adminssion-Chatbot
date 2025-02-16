"""Chunking for table and text"""

from typing import List

from langchain_core.documents.base import Document as LangchainDocument
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter


def table_chunking(table_markdown: str, chunk_size: int = 1500) -> list:
    """
    Chunking for table
    Args:
        table_markdown (str): Markdown table
        chunk_size (str): length of each chunk

    Returns:
        list: list of chunks
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=0,  # Advoid duplicate data
        separators=["\n\n", "\n", " "]  # keep the row
    )
    lines = table_markdown.split("\n")
    header = lines[0] + '\n' + lines[1]
    chunks = splitter.split_text(table_markdown)
    return [header + "\n" + chunk for i, chunk in enumerate(chunks)]


def title_chunking(text: str, chunk_size: int = 1500, chunk_overlap: int = 500) -> List[LangchainDocument]:
    """
        Chunking for text
    Args:
        text (str): text to split
        chunk_size (str): length of each chunk
        chunk_overlap (str): length of overlap between chunks

    Returns:
        list: list of chunks
    """
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3")
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on, strip_headers=False)
    md_header_splits = markdown_splitter.split_text(text)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    splits = text_splitter.split_documents(md_header_splits)

    return splits

