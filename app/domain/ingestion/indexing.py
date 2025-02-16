import uuid
from typing import List

from langchain_chroma import Chroma
from langchain_core.documents import Document as LangchainDocument

from app.utils.configs import client, embeddings  # Import tuyệt đối

def create_collection(collection_name:str)->bool:
    """
    Create ChromaDB collection
    Returns:
        str: collection name
    """
    try:
        collection = client.get_or_create_collection(name=collection_name)
        print(f"✅ Collection '{collection_name}' đã được tạo!")
        return True
    except Exception as e:
        print(e)


def ingest_data(collection_name: str, chunks: List[LangchainDocument]) -> str:
    """
    Ingest data into collection.
    Args:
        collection_name (str): Name of ChromaDB collection
        chunks (List[LangchainDocument]): List of LangchainDocuments chunks

    Returns:
        bool: True if collection was successfully ingested else False
    """
    try:
        # Init Vector store
        vectorstore = Chroma(
            client=client,
            collection_name=collection_name,
            embedding_function=embeddings
        )
        # add document
        vectorstore.add_documents(chunks)
        return collection_name
    except Exception as e:
        print(e)