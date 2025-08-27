# Sử dụng image Python 3.10-slim làm base image
FROM python:3.10-slim

# Cài đặt các thư viện hệ thống cần thiết (Poppler và Tesseract)
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt và cài đặt các thư viện Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn vào container
COPY . /app

# Đặt thư mục làm việc
WORKDIR /app

# Chạy ứng dụng Flask
CMD ["python", "app.py"]
