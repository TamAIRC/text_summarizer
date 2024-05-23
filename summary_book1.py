import re
import time
from config.config_text import (
    CHAPTER_KEYWORD,
    CHAPTER_KEYWORD_NUMBER,
    CHAPTER_LV1,
    LV1_KEYWORDS,
    VI_TEXT_LOWERCASE,
    VI_TEXT_UPPERCASE,
)
from pdf2image import convert_from_path
from config import config
import pytesseract
from src.extract_menu.assign_levels import assign_levels
from src.ocr.ocr_image import detect_line_word, crop_box
from src.ocr.pdf_to_img import pdf_to_image_np
from src.step3_chapter_division.chapter_division import split_content_by_toc
from src.text_rank.text_rank import summarize_text
from src.VietnameseOcrCorrection.config import LINK_MODEL_SEQ2SEQ
from src.VietnameseOcrCorrection.tool.predictor import Predictor
from tools.save_step import save_crop_image, save_menu_to_txt


def load_model():
    pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_LINK


# Get total number of pages in PDF
def get_pdf_page_count(file_path):
    return len(convert_from_path(file_path))


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
    if is_page:
        return int(round(size_sumary * word_in_page))
    return int(round(book_size * size_sumary / 100 * word_in_page))


def is_table_of_contents(text, chapter_lv1):
    text = text.lower()
    lines = text.split("\n")
    # Kiểm tra xem có ít nhất một dòng bắt đầu bằng số hoặc từ khóa
    for line in lines:
        if line.strip().startswith(chapter_lv1):
            return True
    # Kiểm tra xem có ít nhất một dòng chứa các tiêu đề có độ sâu lồng nhau không
    for i in range(len(lines)):
        if lines[i].strip().startswith(chapter_lv1):
            for j in range(i + 1, min(i + 4, len(lines))):
                if lines[j].strip().startswith(tuple(CHAPTER_KEYWORD_NUMBER)):
                    return True
    return False


def clear_text(text):
    SAVE_KEY_REGEX_PATTERN = re.compile(
        r"[^a-zA-Z0-9\s\t\.\,{}()\-/{}]".format(
            re.escape(VI_TEXT_LOWERCASE),
            re.escape(VI_TEXT_UPPERCASE),
        )
    )
    text = SAVE_KEY_REGEX_PATTERN.sub(" ", text)
    text = re.sub(r"\t|\n", " ", text)
    text = re.sub(r"\.{2,}", "", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r" \.", ".", text)
    text = text.rstrip()
    return text
    # text = re.sub(r"\t|\n|\s{2,}|\.{2,}", " ", text)
    # text = re.sub(r" \.", ".", text).strip()
    # return text


def correct_text(text):
    model_predictor = Predictor(
        device="cpu",
        model_type="seq2seq",
        weight_path=LINK_MODEL_SEQ2SEQ,
    )
    outs = model_predictor.predict(text.strip(), NGRAM=6)
    return outs


# Extract table of contents from pages
def extract_table_of_contents(list_page):
    # Kết hợp danh sách LV1_KEYWORDS và CHAPTER_KEYWORD

    last_toc_page, table_of_contents = None, []
    for i, page in enumerate(list_page):
        lines_rects = detect_line_word(page, is_menu=True)
        is_menu = 0
        page_content = []

        for j, line in enumerate(lines_rects):
            # save_crop_image(page, line, f"line_{i}_{j}")
            roi = crop_box(page, line)
            text_line = pytesseract.image_to_string(roi, lang="vie")

            if len(text_line) != 0:
                text_line = clear_text(text_line)
                text_line = text_line.rstrip(".")

                if is_table_of_contents(text_line, CHAPTER_LV1):
                    is_menu += 1

                page_content.append(text_line)

        if is_menu == 0 or is_menu < (len(lines_rects) - 5):
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
            text_line = pytesseract.image_to_string(roi, lang="vie").strip()
            text_line = clear_text(text_line)
            text += text_line + " "

    return text


def sumary_book(book_link, size_sumary, is_page=True):
    load_model()

    text_sumary = "Nội dung tóm tắt"
    # print(text_sumary)
    # Step 1
    print("Step 1 ---------------------------------------------------------------")
    pages_np = pdf_to_image_np(book_link)
    #len_pages = len(pages_np)
    # words_to_summarize = determine_summary_size(len_pages, size_sumary, is_page)
    # print(pages_np)
    # numbers_page_use_check_menu = round(len_pages * 0.2)
    numbers_page_use_check_menu = 5

    list_page_check_menu = pages_np[:numbers_page_use_check_menu]
    # list_page_check_menu = pages_np
 ###############################  
    print("Step 2 ---------------------------------------------------------------")

    last_toc_page, table_of_contents = extract_table_of_contents(list_page_check_menu)
    # save_menu_to_txt(table_of_contents, file_path="./output/menu1.txt")
    table_of_contents = assign_levels(table_of_contents)
    save_menu_to_txt(table_of_contents, file_path="./output/menu2.txt")
    print("Step 3 ---------------------------------------------------------------")
    pages_np_content = pages_np[last_toc_page:]

    # OCR nội dung sách
    content_book = ocr_content(pages_np_content)
    # print(content_book)
########################
    print("Step 4 ---------------------------------------------------------------")
    chapter_content = split_content_by_toc(content_book, table_of_contents)
    print(chapter_content)
    print("Step 5 ---------------------------------------------------------------")
    summarize_all = ""
    for i, chapter_content_item in enumerate(chapter_content):
        percent = 20
        chapter_summarize = summarize_text(chapter_content_item, percent)
        # summarize_all.append(chapter_summarize)
        summarize_all += "Chapter " + str(i) + ": " + chapter_summarize + "\n"

    with open("./output/noidung_tomtat.txt", "w", encoding="utf-8") as file:
        file.write(summarize_all)
    return text_sumary


def main():
    # book_link = "./datasets/book_test/Bup-Sen-xanh.pdf"
    book_link = "./datasets/book_test/book_kiemthuvadambaochatluongPM-1-10.pdf"
    # book_link = "./datasets/book_test/Bup-Sen-xanh-1-10.pdf"
    size_sumary = 20
    # Tóm tắt page - True | format % - False
    is_page = False
    sumary_book(book_link, size_sumary, is_page)
    return


if __name__ == "__main__":
    main()
