from langchain_chroma import Chroma
from app.utils.configs import embeddings, client


def get_vectorstore(collection_name: str) -> Chroma:
    """Kết nối ChromaDB với collection cụ thể."""
    return Chroma(
        # persist_directory=r"D:\ThucTap\ThucTap\HaUI-Adminssion-Chatbot\app\models\app\chroma_db",
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings
    )