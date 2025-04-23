"""
This module contains functions to setup RAG pipeline.
"""

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory, ConfigurableFieldSpec
from langchain_openai import ChatOpenAI

from api.logging_theme import setup_logger
from domain.generation.prompt_templates import qa_prompt
from domain.retrieval.search import SearchEngine
from utils.configs import llm
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder




class RAGPipeline:
    """
    This class contains functions to set up RAG pipeline.
    """
    def __init__(self, collection_name: str, llm_instance: ChatOpenAI = llm):
        """
        Initialize the RAGPipeline with a collection name.

        Args:
            collection_name (str): The name of the collection to use for retrieval.
        """
        self.collection_name = collection_name
        self.logger = setup_logger(__name__)
        self.llm = llm_instance

    def create_qa_chain(self, llm_instance: ChatOpenAI, prompt: ChatPromptTemplate):
        """
        Create a question-answer chain using the provided language model and prompt.

        Args:
            llm_instance (ChatOpenAI): The language model to use.
            prompt (ChatPromptTemplate): The prompt template for the QA chain.

        Returns:
            create_stuff_documents_chain: The created QA chain.
        """
        try:
            return create_stuff_documents_chain(llm_instance, prompt)
        except Exception as error:
            self.logger.error("Error creating QA chain: %s", error, exc_info=True)
            raise

    def create_rag_chain(self, qa_chain):
        """
        Create a retrieval-augmented generation (RAG) chain using the QA chain.

        Args:
            qa_chain: The question-answer chain to use for document processing.

        Returns:
            RetrievalQAChain: A chain that combines retrieval and question-answering.
        """
        try:
            return create_retrieval_chain(
                SearchEngine(collection_name=self.collection_name, k=10).semantic_search(),
                qa_chain
            )
        except Exception as error:
            self.logger.error("Error creating RAG retrieval chain: %s", error, exc_info=True)
            raise

    def setup_conversation_memory(self, window_size: int = 5):
        """
        Setup conversation memory with specified window size.

        Args:
            window_size (int): The size of the conversation window. Defaults to 5.

        Returns:
            function: A function that returns the chat memory.
        """
        memory = ConversationBufferWindowMemory(k=window_size)

        def get_session_history(_):
            """
            Get the session history.

            Args:
                _ (Any): Unused parameter required by the API.

            Returns:
                ChatMessageHistory: The chat memory history.
            """
            return memory.chat_memory

        return get_session_history

    def conversational_chain(self, promptTemplate: str) -> RunnableWithMessageHistory:
        """
        Create a retrieval-augmented generation chain with conversational memory.

        Returns:
            RunnableWithMessageHistory: An instance containing the conversational RAG chain.
        """
        try:
            qa_chain = self.create_qa_chain(self.llm, self.create_qa_prompt(promptTemplate))
            rag_chain = self.create_rag_chain(qa_chain)
            get_session_history = self.setup_conversation_memory()
            chain = RunnableWithMessageHistory(
                # RunnableLambda(lambda x: rag_chain.astream(x)),
                rag_chain,
                get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history",
                output_messages_key="answer",
                history_factory_config=[
                    ConfigurableFieldSpec(
                        id="conversation_id",
                        annotation=str,
                        name="Conversation ID",
                        description="Unique identifier for the conversation.",
                        default="",
                        is_shared=True,
                    ),
                ]
            )
            return chain
        except Exception as error:
            self.logger.error("Error setting up conversational chain: %s", error, exc_info=True)
            raise ValueError("Error setting up conversational chain")

    def create_qa_prompt(self, system_prompt: str) -> ChatPromptTemplate:
        """
        Create a QA prompt template from a given system prompt.

        Args:
            system_prompt (str): The system prompt string.

        Returns:
            ChatPromptTemplate: The created QA prompt template.
        """
        return ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )