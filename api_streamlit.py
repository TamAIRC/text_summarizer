import streamlit as st
import os
from werkzeug.utils import secure_filename
from summary_book import SummaryBook
import fitz  # PyMuPDF
import base64

st.set_page_config(layout="wide")

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def displayPDF(file):
    # Mở file từ đường dẫn file
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Nhúng PDF vào HTML
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf">'

    # Hiển thị File
    st.markdown(pdf_display, unsafe_allow_html=True)

def main():
    st.title('Tóm Tắt Sách')

    uploaded_file = st.file_uploader("Chọn một file PDF", type="pdf")

    if uploaded_file is not None:
        if allowed_file(uploaded_file.name):
            file_path = os.path.join(UPLOAD_FOLDER, secure_filename(uploaded_file.name))
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())

            col1, col2 = st.columns([1, 1])

            with col1:
                displayPDF(file_path)

            with col2:
                size_summary = st.slider("Kích thước tóm tắt (%):", min_value=1, max_value=100, value=20)

                if st.button('Tóm tắt'):
                    summarizer = SummaryBook()
                    is_page = False   # Định dạng mẫu
                    summary = summarizer.summary_book(file_path, size_summary, is_page)
                    # Đọc nội dung tóm tắt từ file và trả về
                    with open("./output/noidung_tomtat1.txt", "r", encoding="utf-8") as file:
                        content = file.read()
                    st.text_area("Nội dung tóm tắt", content, height=200)
                    # st.text_area("Nội dung tóm tắt", summary, height=200) # Nếu bạn muốn trả về tóm tắt tính toán
        else:
            st.error("File không hợp lệ. Vui lòng chọn file PDF.")

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    main()
