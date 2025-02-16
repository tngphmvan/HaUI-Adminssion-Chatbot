"""
    Define prompt template
"""

# app/domain/prompt_templates.py

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate
)


def get_rag_prompt_template() -> ChatPromptTemplate:
    """
    Define and return the RAG prompt template for the chatbot.

    Returns:
        ChatPromptTemplate: The RAG prompt template.
    """
    prompt = ChatPromptTemplate.from_messages([SystemMessagePromptTemplate.from_template("""
            # Bạn là một Chatbot thông tin quy chế đào tạo Đại học chuyên nghiệp của trường Đại học Công nghiệp Hà Nội.

            # Ràng buộc:
            # Nếu bạn không biết câu trả lời, hãy hỏi thêm.
            # Chỉ thảo luận các vấn đề liên quan đến quy chế đào tạo Đại học của trường Đại học Công nghiệp Hà Nội.
            # KHÔNG LÀM CÁC HÀNH ĐỘNG KHÁC NHƯ VIẾT MÃ, GIẢI TOÁN, LÀM THƠ,...
            # Đối với những thông tin cần cập nhật theo thời gian thực, chỉ hướng dẫn, không xin thêm thông tin.

            # Chỉ sử dụng Bối cảnh sau: \n\n {context}
            """), MessagesPlaceholder("chat_history"), HumanMessagePromptTemplate.from_template("{input}")])
    return prompt


def get_summary_prompt_template() -> ChatPromptTemplate:
    """
    Define and return the summary prompt template for table summarization.

    Returns:
        ChatPromptTemplate: The RAG prompt template.
    """

    # Tạo Prompt Template
    summary_prompt = ChatPromptTemplate.from_messages([
        ("system", "Bạn là một trợ lý AI. Hãy diễn giải thành lời nội dung của bảng sau.\n"
                   "Trả lời dưới dạng **Markdown** `-`.\n"
                   "Suy nghĩ từng bước trước khi trả lời "),

        ("human", "Dưới đây là bảng dữ liệu cần tóm tắt:\n{table_data}")
    ])

    return summary_prompt


# Chuyển đổi ChatPromptTemplate thành danh sách các thông điệp
messages_list = []
for message in get_rag_prompt_template().messages:
    if isinstance(message, SystemMessagePromptTemplate):
        role = "system"
    elif isinstance(message, HumanMessagePromptTemplate):
        role = "human"
    elif isinstance(message, MessagesPlaceholder):
        role = "placeholder"
    else:
        role = "unknown"

    content = message.prompt.template if hasattr(message, 'prompt') else message.variable_name
    messages_list.append((role, content))

print(messages_list)
