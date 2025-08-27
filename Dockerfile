FROM python:3.10-slim

# Cài đặt các thư viện hệ thống cần thiết (ví dụ Poppler)
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt thư viện Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy mã nguồn vào container
COPY . /app
WORKDIR /app

# Chạy ứng dụng Flask
CMD ["python", "app.py"]
