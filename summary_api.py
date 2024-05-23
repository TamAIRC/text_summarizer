from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from summary_book import SummaryBook
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdfFile' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['pdfFile']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        summarizer = SummaryBook()
        size_summary = 20  # Example summary size
        is_page = False   # Example format
        summary = summarizer.summary_book(file_path, size_summary, is_page)
        #kết quả trả về từ tóm tắt đang là null nên đọc và trả về nội dung tóm tắt được lưu trong file
        with open("./output/noidung_tomtat1.txt", "r", encoding="utf-8") as file:
            content = file.read()
        return jsonify({'summary': content})
        # return jsonify({'summary': summary})
    else:
        return jsonify({"error": "Invalid file type"})
 

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=5555,threaded=True)
