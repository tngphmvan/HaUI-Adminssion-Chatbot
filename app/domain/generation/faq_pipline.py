"""
This module contains the FAQSearcher class which is responsible for searching FAQ answers using semantic search.
"""
from api.logging_theme import setup_logger
from domain.generation.prompt_templates import val_faq_prompt
from domain.retrieval.search import SearchEngine
from schemas.faq_val_model import EvalFAQ
from utils.configs import llm


class FAQSearcher:
    """
    This class contains functions for searching FAQ answers using semantic search.
    """
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.logger = setup_logger(__name__)

    async def search_faq(self, question: str) -> str | None:
        """Search for FAQ answers using semantic search and validate relevance.

        Args:
            question (str): The user's question

        Returns:
            str | None: Answer if found and relevant, None otherwise
        """
        try:
            # Get most relevant FAQ
            retriever = SearchEngine(collection_name="faq", k=1).semantic_search()
            docs = await retriever.ainvoke(question)

            if not docs:
                return None

            # Validate relevance using structured output
            structured_llm = llm.with_structured_output(EvalFAQ)
            validation_input = val_faq_prompt.format(
                question=question,
                retrieved_document=docs[0]
            )

            result = await structured_llm.ainvoke(validation_input)

            if result.is_relevant:
                # Get answer from vectorstore metadata
                return docs[0].metadata["answer"]

            return None

        except Exception as e:
            self.logger.error(f"An error occurred in search_faq: {e}")
            return None