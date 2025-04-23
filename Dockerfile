FROM python:3.11-slim-bookworm

WORKDIR /app

# Cài đặt các gói cần thiết
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Sao chép file requirements.txt vào container
COPY requirements.txt .

# Cài đặt các gói từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ code vào container
COPY ./app /app

# Tạo thư mục cho Qdrant
RUN mkdir -p /app/qdrant_data

# Expose port
EXPOSE 8000

# Command để chạy ứng dụng
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "info", "--workers", "4"]