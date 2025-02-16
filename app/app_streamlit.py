import streamlit as st
import os
from docx import Document
import time

from app.domain.retrieval.search import semantic_search
from app.models.ingestion import ingest
from app.utils.configs import client


st.set_page_config(layout="wide")
# 👉 Layout 2 cột: Bên trái là tải file, bên phải là hiển thị chunks
col1, col2 = st.columns([2, 3])

# 👉 Cột 1: Quản lý Collection
with col1:
    st.title("📂 Quản lý Dữ Liệu với ChromaDB")

    # 👉 Lấy danh sách collection từ ChromaDB
    collection_names = client.list_collections()

    selected_collection = st.selectbox("🔹 Chọn Collection:", ["Chọn Collection"] + collection_names)

    if selected_collection != "Chọn Collection":
        st.success(f"✅ Đã chọn Collection: **{selected_collection}**")

        # 👉 Lấy dữ liệu từ collection đã chọn
        collection = client.get_collection(selected_collection)
        documents = collection.get()

        if st.button("🗑 Xóa Collection"):
                client.delete_collection(selected_collection)
                st.success(f"✅ Đã xóa collection: {selected_collection}")
                st.rerun()  # Làm mới giao diện

    # 👉 Nhập tên Collection trước khi ingest
    st.subheader("📥 Tải tài liệu lên ChromaDB")
    collection_name = st.text_input("🔹 Nhập tên Collection để lưu dữ liệu:")
    if collection_name in collection_names:
        st.warning("⚠️Tên collection đã tồn tại, vui lòng chọn tên collection khác")
    if not collection_name:
        st.warning("⚠️ Vui lòng nhập tên Collection trước khi tiếp tục.")

    # 👉 Upload file DOCX
    uploaded_file = st.file_uploader("📄 Chọn file DOCX", type=["docx"])

    if uploaded_file and collection_name:
        save_path = os.path.join("uploads", uploaded_file.name)
        os.makedirs("uploads", exist_ok=True)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"📌 File đã được lưu: `{uploaded_file.name}`")

        # 👉 Đọc nội dung file
        doc = Document(save_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        st.text_area("📄 Nội dung file:", text, height=150)

        # 👉 Hiển thị tiến trình ingest
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.text("🔄 Bắt đầu ingest...")

        for percent in range(1, 101, 10):
            progress_bar.progress(percent / 100.0)
            status_text.text(f"⏳ Đang ingest... {percent}%")
            time.sleep(0.3)

        # 👉 Gọi ingest và nhận lại các chunk đã xử lý
        chunks = ingest(collection_name, save_path, uploaded_file.name)

        progress_bar.progress(1.0)
        status_text.text("✅ Hoàn thành ingest!")

        os.remove(save_path)  # Xóa file sau khi xử lý
    # 👉 Nút mở Chainlit
    st.markdown("---")
    if st.link_button("🚀 Mở Chainlit Chatbot", url="http://localhost:8000/"):
        st.success("Chainlit đang chạy... Kiểm tra terminal!")

# 👉 Cột 2: Hiển thị dữ liệu trong Collection hoặc các chunk đã ingest
with col2:
    st.subheader("📜 Dữ liệu trong Collection")

    if selected_collection != "Chọn Collection":
        if documents and "documents" in documents:
            for i, doc in enumerate(documents["documents"]):
                st.markdown(f"**Chunk {i+1}:**")
                st.info(doc)
        else:
            st.warning("⚠️ Collection này chưa có dữ liệu.")

    # 👉 Hiển thị các chunk đã ingest ngay sau khi xử lý
    if uploaded_file and collection_name:
        st.subheader("📜 Các chunk đã lưu:")
        if chunks:
            for i, chunk in enumerate(chunks):
                st.markdown(f"**Chunk {i+1}:**")
                st.info(chunk.page_content)
        else:
            st.warning("⚠️ Không có chunk nào được lưu.")
