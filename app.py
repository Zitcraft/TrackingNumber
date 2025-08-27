from flask import Flask, request, jsonify
import pytesseract
from pdf2image import convert_from_path
import tempfile
import shutil
import uuid
import requests
import concurrent.futures

app = Flask(__name__)

# Cấu hình Tesseract và Poppler
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Đường dẫn tesseract trên Linux
poppler_path = "/usr/bin"  # Đường dẫn poppler-utils trên Linux

# API nhận URL PDF và trả về kết quả OCR
@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    data = request.json
    pdf_url = data.get('pdf_url')
    
    if not pdf_url:
        return jsonify({"error": "PDF URL is required"}), 400
    
    # Download PDF
    pdf_path = download_pdf(pdf_url)
    if not pdf_path:
        return jsonify({"error": "Failed to download PDF"}), 400
    
    # Chạy OCR và trả về kết quả
    result = run_ocr(pdf_path)
    return jsonify({"tracking_number": result})

def download_pdf(url):
    # Tải file PDF từ Google Drive
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        temp_dir = tempfile.mkdtemp()
        unique_name = f"temp_{uuid.uuid4().hex}.pdf"
        temp_pdf = os.path.join(temp_dir, unique_name)
        with open(temp_pdf, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        return temp_pdf
    else:
        return None

def run_ocr(pdf_path):
    # Chạy OCR trên file PDF
    try:
        pages = convert_from_path(pdf_path, poppler_path=poppler_path)
        page = pages[0]
        crop_box = (180, 878, 580, 1028)  # Cắt ảnh
        cropped = page.crop(crop_box)
        text = pytesseract.image_to_string(cropped, lang='eng')
        return text.strip()
    except Exception as e:
        return f"Error processing PDF: {e}"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
