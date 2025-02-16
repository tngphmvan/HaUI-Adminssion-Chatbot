from typing import List
from app.domain.retrieval.vectorstores import get_vectorstore
from langchain_chroma import Chroma
from langchain_core.documents import Document as LangchainDocument
from langchain_core.vectorstores import VectorStoreRetriever
from app.utils.configs import embeddings


def semantic_search(query: str, collection_name: str, k: int = 5) -> List[LangchainDocument]:
    """Tìm kiếm ngữ nghĩa trên ChromaDB."""
    vectorstore = get_vectorstore(collection_name)

    results: List[LangchainDocument] = vectorstore.similarity_search(query, k=k)

    return results

def multiple_semantic_search(query: str, collection_names: List[str], k: int = 5) -> VectorStoreRetriever:
    """Tìm kiếm trên nhiều collection và trả về Retriever thay vì danh sách Document."""
    all_documents = []

    for collection_name in collection_names:
        vectorstore = get_vectorstore(collection_name)
        results = vectorstore.similarity_search(query, k=k)
        all_documents.extend(results)

    # Tạo vectorstore từ danh sách tài liệu
    vectorstore = Chroma.from_documents(all_documents, embeddings)

    return vectorstore.as_retriever()  # Trả về retriever thay vì danh sách Document

