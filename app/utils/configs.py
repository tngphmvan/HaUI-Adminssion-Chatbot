import os

from chromadb import PersistentClient
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=api_key)

client = PersistentClient()