import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import FastEmbedSparse

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"), api_key=api_key)

spare_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")

llm = ChatOpenAI(
    model=os.getenv("OPENAI_CHAT_MODEL"),
    temperature=1.3,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=api_key,
)

