import re
import time
import cv2
from matplotlib import pyplot as plt
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from pdf2image import convert_from_path
from config import config
from src.extract_menu.assign_levels import assign_levels
from src.ocr.helpers import convert_contours_to_bounding_boxes
from src.ocr.ocr_image import detect_line_word, crop_box, detect_text_area
from src.ocr.pdf_to_img import pdf_to_image_np

import pytesseract

from src.step3_chapter_division.chapter_division import split_content_by_toc
from src.text_rank.text_rank import summarize_text


def load_model():
    pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_LINK
    return


def get_pdf_page_count(file_path):
    # Chuyển đổi tất cả các trang PDF thành hình ảnh
    images = convert_from_path(file_path)
    # Trả về số lượng hình ảnh, tương đương với số trang PDF
    return len(images)


def determine_summary_size(
    book_size: int, size_sumary: int, is_page=True, word_in_page=400
):
    """
    Determine the size of the summary in terms of number of words.

    Parameters:
        book_size (int): Number of pages in the book.
        size_sumary (int): Size of the summary in percentage (if is_page is False) or in pages (if is_page is True).
        is_page (bool): True if size_sumary is in pages, False if size_sumary is in percentage of book size.
        word_in_page (int): Average number of words per page.

    Returns:
        int: Size of the summary in terms of number of words.
    """
    if not is_page:
        w_summarize = book_size * size_sumary / 100 * word_in_page
    else:
        w_summarize = size_sumary * word_in_page
    return int(round(w_summarize))


def is_table_of_contents(text, chapter_lv1):
    # Chuyển đổi văn bản thành chữ thường
    text = text.lower()
    number_markers = ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10."]

    # Tách các dòng văn bản thành từng dòng riêng biệt
    lines = text.split("\n")

    # Kiểm tra xem có ít nhất một dòng bắt đầu bằng số hoặc từ khóa
    for line in lines:
        if line.strip().startswith(chapter_lv1):
            return True

    # Kiểm tra xem có ít nhất một dòng chứa các tiêu đề có độ sâu lồng nhau không
    for i in range(len(lines)):
        if lines[i].strip().startswith(chapter_lv1):
            for j in range(i + 1, min(i + 4, len(lines))):
                if lines[j].strip().startswith(tuple(number_markers)):
                    return True
    return False


def clear_text(text):
    SAVE_KEY_REGEX_PATTERN = re.compile(
        r"[^a-zA-Z0-9\s\t\.\,{}()\-/{}]".format(
            re.escape(
                "ỹáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ"
            ),
            re.escape(
                "ỸÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴĐ"
            ),
        )
    )
    text = SAVE_KEY_REGEX_PATTERN.sub(" ", text)
    text = re.sub(r"\t|\n", " ", text)
    text = re.sub(r"\.{2,}", "", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r" \.", ".", text)
    text = text.rstrip()
    return text


# Tìm kiếm menu của sách


def extract_table_of_contents(list_page):
    # Các từ khóa tiêu đề và số - cho ra config
    title_keywords = ["chương", "phần", "chapter", "hồi"]
    number_chapter = [
        "1.",
        "2.",
        "3.",
        "4.",
        "5.",
        "6.",
        "7.",
        "8.",
        "9.",
        "10.",
        "I",
        "II",
        "III",
        "IV",
        "V",
        "VI",
        "VII",
        "VIII",
        "IX",
        "X",
    ]

    # Kết hợp danh sách title_keywords và number_chapter
    chapter_lv1 = tuple(
        number_chapter
        + [
            "{} {}".format(keyword, num)
            for keyword in title_keywords
            for num in range(1, 11)
        ]
    )

    last_toc_page = None
    table_of_contents = []
    for i, page in enumerate(list_page):
        lines_rects = detect_line_word(page)
        is_menu = 0
        page_content = []

        for line in lines_rects:
            roi = crop_box(page, line)
            text_line = pytesseract.image_to_string(roi, lang="vie")

            if len(text_line) != 0:
                text_line = clear_text(text_line)
                text_line = text_line.rstrip(".")

                if is_table_of_contents(text_line, chapter_lv1):
                    is_menu += 1
                page_content.append(text_line)
        # print(f"lines_rects - is_menu\n{len(lines_rects)}-{is_menu}")
        if is_menu == 0 or is_menu < (len(lines_rects) - 10):
            continue
        else:
            last_toc_page = i + 1
            table_of_contents += page_content

    return last_toc_page, table_of_contents


def ocr_content(list_page):
    text = ""

    for page in list_page:
        lines_rects = detect_line_word(page)

        for line in lines_rects:
            roi = crop_box(page, line)
            text_line = pytesseract.image_to_string(roi, lang="vie")
            text_line = clear_text(text_line)

            text += text_line + " "
    return text


# Vietnamese Ocr Correction - Tham khảo: https://github.com/buiquangmanhhp1999/VietnameseOcrCorrection
def correct_text(text):
    return text


# Trích xuất keyword văn bản
def keyword_text(text):
    key_word = []
    return key_word


# Chia text theo chương
def divide_chapters(book):
    chapter_array = []
    return chapter_array


def sumary_text(text):
    text_sumary = ""
    return text_sumary


def sumary_book(book_link, size_sumary, is_page=True):
    load_model()

    word_in_page = 400
    text_sumary = "Nội dung tóm tắt"

    print("Step 1")
    start_1 = time.time()
    pages_np = pdf_to_image_np(book_link)
    len_pages = len(pages_np)
    words_to_summarize = determine_summary_size(len_pages, size_sumary, is_page)
    end_1 = time.time()
    print(f"time Step 1:{(end_1-start_1):.03f}s")

    print("Step 2")
    # numbers_page_use_check_menu = round(len_pages * 0.2)
    numbers_page_use_check_menu = 10
    print("numbers_page_use_check_menu", numbers_page_use_check_menu)

    start_2 = time.time()

    list_page_check_menu = pages_np[:numbers_page_use_check_menu]

    last_toc_page, table_of_contents = extract_table_of_contents(list_page_check_menu)

    table_of_contents = assign_levels(table_of_contents)

    pages_np_content = pages_np[last_toc_page:]

    # OCR nội dung sách
    print("OCR nội dung sách.")
    content_book = ocr_content(pages_np_content)
    end_2 = time.time()

    print(f"time Step 2:{(end_2-start_2):.03f}s")
    print(f"words_to_summarize:{words_to_summarize}")
    start_3 = time.time()
    chapter_content = split_content_by_toc(content_book, table_of_contents)
    summarize_all = ""
    for i, chapter_content_item in enumerate(chapter_content):
        percent = 20
        chapter_summarize = summarize_text(chapter_content_item, percent)
        # summarize_all.append(chapter_summarize)
        summarize_all += "Chapter " + str(i) + ": " + chapter_summarize + "\n"
    end_3 = time.time()
    print(f"time Step 3:{(end_3-start_3):.03f}s")

    with open("noidung_tomtat.txt", "w", encoding="utf-8") as file:
        file.write(summarize_all)
    return text_sumary


def main():
    # book_link = "./datasets/data_book/Bup-Sen-xanh.pdf"
    book_link = "./datasets/data_book/TTX-Khung CPDT_V01_20180910.pdf"
    size_sumary = 20
    # Tóm tắt page - True | format % - False
    is_page = False
    sumary_book(book_link, size_sumary, is_page)
    # Input
    # Format: PDF
    # Số lượng trang: 51
    # --------------------------------
    # Bước 1: Xác định kích thước tóm tắt và tính toán số từ cần tóm tắt
    # Thời gian thực hiện: ~ 9.8s - 10.6s
    # Lượng từ tóm tắt: 4080 Từ
    # --------------------------------
    # Bước 2: Tìm kiếm mục lục sách và thực hiện OCR
    # 2.1. Tìm kiếm mục lục sách - Lấy 20% số trang tính từ bắt đầu thực hiện tìm kiếm
    # time Step 2:40-50s
    # OCR Nội dung sách
    # time Step 2:200-260s
    # Bước 3: Chia trang sách thành các chương:
    # + Đầu vào:
    #   > Mục lục sách: Thông tin về mục lục của sách.
    #   > Nội dung sách: Nội dung text OCR
    # + Đầu ra:
    #   `Mảng các chương sách`: Trang bắt đầu đến kết thúc của mỗi chương (image numpy).
    # + Thực hiện:
    #   > Dựa vào thông tin từ mục lục, chia trang sách thành các chương tương ứng.
    # + Công nghệ:
    #   > `Xử lý dữ liệu và chuỗi`: Python.
    #   > Có thể sử dụng kỹ thuật phân đoạn văn bản để tách các chương.

    return


if __name__ == "__main__":
    main()
