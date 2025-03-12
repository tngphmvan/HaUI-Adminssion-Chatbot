FROM python:3.11-slim-bookworm

WORKDIR /app

# Sao chép file requirements.txt vào container
COPY requirements.txt .

# Cài đặt các gói từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt