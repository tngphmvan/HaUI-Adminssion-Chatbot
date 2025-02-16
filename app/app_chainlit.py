import os
import time
from typing import List
from uuid import uuid4
import re

import chainlit as cl
from chainlit.input_widget import Switch
from groq import AsyncGroq
from openai import AsyncOpenAI
from langchain.retrievers import MergerRetriever
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever

from app.domain.retrieval.vectorstores import get_vectorstore
from utils.configs import client as chroma_client
from langchain.chains import HypotheticalDocumentEmbedder

API_URL = "http://127.0.0.1:8080/query"


client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    # base_url="https://api.deepseek.com"
)
# client = AsyncGroq(
#     api_key=os.getenv("GROQ_API_KEY"),
# )


@cl.on_chat_start
async def start():
    collection_names = chroma_client.list_collections()
    setting = await cl.ChatSettings([
        Switch(id=collection_name, label=collection_name)
        for collection_name in collection_names
    ]).send()
    cl.user_session.set("session_id", str(uuid4()))


@cl.on_settings_update
async def setup_agent(settings):
    """Cập nhật các collection đã chọn và khởi tạo RAG chain."""
    selected_collections = [name for name, enabled in settings.items() if enabled]
    cl.user_session.set("selected_collections", selected_collections)

    if not selected_collections:
        return

    # Khởi tạo retriever
    retrievers = MergerRetriever(
        retrievers=[
            get_vectorstore(collection_name).as_retriever(search_type="mmr", search_kwargs={"score_threshold": 0.8}) for
            collection_name in selected_collections]
    )
    cl.user_session.set("retrievers", retrievers)

    # Tạo chuỗi xử lý RAG
    # question_answer_chain = create_stuff_documents_chain(llm, get_rag_prompt_template())
    # rag_chain = create_retrieval_chain(retrievers, question_answer_chain)
    # memory = ConversationBufferWindowMemory(k=5)
    #
    # def get_session_history(_):
    #     return memory.chat_memory  # Trả về lịch sử chat
    #
    # conversational_rag_chain = RunnableWithMessageHistory(
    #     rag_chain,
    #     get_session_history,
    #     input_messages_key="input",
    #     history_messages_key="chat_history",
    #     output_messages_key="answer",
    # )
    #
    # # Lưu chain vào session
    # cl.user_session.set("conversational_rag_chain", conversational_rag_chain)
    # print(f"🔄 RAG pipeline initialized for collections: {selected_collections}")


@cl.on_message
async def main(message: cl.Message):
    """Xử lý truy vấn và sinh câu trả lời."""
    selected_collections = cl.user_session.get("selected_collections", [])
    retrievers: VectorStoreRetriever = cl.user_session.get("retrievers")
    session_id = cl.context.session.id

    if not selected_collections:
        await cl.Message(content="❌ Bạn chưa chọn collection nào! Hãy chọn ít nhất một collection.").send()
        return

    start = time.time()
    retrieved_docs = retrievers.invoke(message.content)

    stream = await client.chat.completions.create(
        # model="deepseek-r1-distill-llama-70b",
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": ("""
            # Bạn là một Chatbot thông tin quy chế đào tạo Đại học chuyên nghiệp của trường Đại học Công nghiệp Hà Nội.

            # Ràng buộc:
            # Nếu bạn không biết câu trả lời, hãy hỏi thêm.
            # Chỉ thảo luận các vấn đề liên quan đến quy chế đào tạo Đại học của trường Đại học Công nghiệp Hà Nội.
            # KHÔNG LÀM CÁC HÀNH ĐỘNG KHÁC NHƯ VIẾT MÃ, GIẢI TOÁN, LÀM THƠ,...
            # Đối với những thông tin cần cập nhật theo thời gian thực, chỉ hướng dẫn, không xin thêm thông tin.

            # Chỉ sử dụng Bối cảnh sau:
            """)},
            {"role": "system", "content": str([doc.page_content for doc in retrieved_docs])},
            {"role": "user", "content": message.content},
            *cl.chat_context.to_openai()
        ],
        stream=True
    )
    text_elements = []  # type: List[cl.Text]

    # Step hiển thị tài liệu nguồn
    async with cl.Step(name="Source Documents") as source_step:
        source_text = "\n\n".join([f"**source_{i}:** \n {doc.page_content}" for i, doc in enumerate(retrieved_docs)])
        await source_step.stream_token(source_text)

    thinking = False
    async with cl.Step(name="Thinking") as thinking_step:
        final_answer = cl.Message(content="")

        async for chunk in stream:
            delta = chunk.choices[0].delta

            if delta.content == "<think>":
                thinking = True
                continue

            if delta.content == "</think>":
                thinking = False
                thought_for = round(time.time() - start)
                thinking_step.name = f"Thought for {thought_for}s"
                await thinking_step.update()
                continue
            if thinking:
                await thinking_step.stream_token(delta.content)
            else:
                await final_answer.stream_token(str(delta.content))
    await final_answer.send()
    cl.chat_context.add(final_answer)

    # if retrieved_docs:
    #     for source_idx, source_doc in enumerate(retrieved_docs):
    #         source_name = f"source_{source_idx}"
    #         # Create the text element referenced in the message
    #         text_elements.append(
    #             cl.Text(content=source_doc.page_content, name=source_name)
    #         )
    #     source_names = [text_el.name for text_el in text_elements]
    #     source = cl.Message(content="", elements=text_elements)
    #     if source_names:
    #         source.content += f"\nSources: {', '.join(source_names)}"
    #     else:
    #         source.content += "\nNo sources found"






