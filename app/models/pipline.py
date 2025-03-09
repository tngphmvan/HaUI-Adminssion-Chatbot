"""
This module contains functions for managing the pipeline.
"""
from api.logging_theme import setup_logger
from domain.generation.faq_pipline import FAQSearcher
from domain.generation.rag_pipeline import RAGPipeline


class Pipline:
    """
    This class contains functions for managing the pipeline.
    """
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.logger = setup_logger(__name__)

    async def stream_rag_response(self, question: str, session_id: str):
        """Stream RAG response to the user's question.

        Args:
            question (str): The user's question.
            session_id (str): The session ID.

        Returns:
            str: The response to the user's question.
        """
        # Search for FAQ answers
        try:
            # Search for FAQ answers
            faq_answer = await FAQSearcher(collection_name="faq").search_faq(question)
        except Exception as e:
            self.logger.error("Error occurred while searching FAQ: %s", e, exc_info=True)
            yield "An error occurred while processing your question.\n"
            return

        if faq_answer:
            yield f"FAQ Answer: {faq_answer}\n"
            return

        try:
            # Get RAG retrieval chain
            rag_chain = RAGPipeline(collection_name=self.collection_name).conversational_chain()
        except Exception as e:
            self.logger.error("Error occurred while creating RAG retrieval chain: %s", e, exc_info=True)
            yield "An error occurred while processing your question.\n"
            return

        try:
            # Stream response

            async for chunk in rag_chain.astream({"input": question}, config={"configurable": {"conversation_id": session_id}}):
                if "answer" in chunk:
                    yield chunk["answer"]
                    self.logger.debug(chunk["answer"])

        except Exception as e:
            self.logger.error("Error occurred during streaming response: %s", e, exc_info=True)
            yield "An error occurred while processing the streaming response.\n"
