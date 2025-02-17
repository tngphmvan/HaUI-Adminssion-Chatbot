# Sử dụng Python làm base image
FROM python:3.11-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép tệp requirements.txt vào container
COPY requirements.txt .

# Cài đặt các thư viện Python cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Mở các cổng cần thiết
EXPOSE 8501 8000
