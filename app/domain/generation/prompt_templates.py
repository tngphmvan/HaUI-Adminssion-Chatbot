"""
This module contains the prompt templates for the generation tasks.
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate

qa_system_prompt = (
    """Bạn là một Chatbot tư vấn thông tin tuyển sinh Đại học chuyên nghiệp của trường Đại học Ngoại Thương.

    # Ràng buộc:
    - Nếu bạn không biết câu trả lời, hãy hỏi thêm.
    - Chỉ thảo luận các vấn đề liên quan đến quy chế đào tạo Đại học của trường Đại học Công nghiệp Hà Nội.
    - KHÔNG LÀM CÁC HÀNH ĐỘNG KHÁC NHƯ VIẾT MÃ, GIẢI TOÁN, LÀM THƠ,...
    - Đối với những thông tin cần cập nhật theo thời gian thực, chỉ hướng dẫn, không xin thêm thông tin.
    - Nếu dữ liệu là Bảng, hãy xen xét cẩn thận theo format của bảng.

    # Tư duy theo từng bước.


    # Hãy xem xét thông tin trong từng document trong context dưới và trích chọn document tốt nhất để lấy làm thông tin:
    # Mỗi document được phân cách bởi dòng "----------" để dễ phân biệt.
    \n\n
    <context>
    {context}
    <context>
    ANSWER:
    """
)
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

val_faq_prompt_template = """
        Người dùng hỏi: "{question}"
        Phần tóm tắt tìm được trong tài liệu: "{retrieved_document}"

        Hãy quyết định xem tài liệu tìm được có nội dung giống câu hỏi câu hỏi người dùng không ?.
        """
val_faq_prompt = ChatPromptTemplate.from_template(val_faq_prompt_template)

document_prompt = PromptTemplate(
    input_variables=["page_content", "id"],
    template="Document id: {id} Content: {page_content}\n"
)