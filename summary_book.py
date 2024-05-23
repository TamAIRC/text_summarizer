import re
from config.config_text import (
    CHAPTER_KEYWORD,
    CHAPTER_KEYWORD_NUMBER,
    CHAPTER_LV1,
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

class SummaryBook:
    def __init__(self):
        self.load_model()

    def load_model(self):
        pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_LINK

    def get_pdf_page_count(self, file_path):
        return len(convert_from_path(file_path))

    def determine_summary_size(self, book_size, size_sumary, is_page=True, word_in_page=400):
        if is_page:
            return int(round(size_sumary * word_in_page))
        return int(round(book_size * size_sumary / 100 * word_in_page))

    def is_table_of_contents(self, text, chapter_lv1):
        text = text.lower()
        lines = text.split("\n")
        for line in lines:
            if line.strip().startswith(chapter_lv1):
                return True
        for i in range(len(lines)):
            if lines[i].strip().startswith(chapter_lv1):
                for j in range(i + 1, min(i + 4, len(lines))):
                    if lines[j].strip().startswith(tuple(CHAPTER_KEYWORD_NUMBER)):
                        return True
        return False

    def clear_text(self, text):
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

    def correct_text(self, text):
        model_predictor = Predictor(
            device="cpu",
            model_type="seq2seq",
            weight_path=LINK_MODEL_SEQ2SEQ,
        )
        outs = model_predictor.predict(text.strip(), NGRAM=6)
        return outs

    def extract_table_of_contents(self, list_page):
        last_toc_page, table_of_contents = None, []
        for i, page in enumerate(list_page):
            lines_rects = detect_line_word(page, is_menu=True)
            is_menu = 0
            page_content = []

            for j, line in enumerate(lines_rects):
                roi = crop_box(page, line)
                text_line = pytesseract.image_to_string(roi, lang="vie")

                if len(text_line) != 0:
                    text_line = self.clear_text(text_line)
                    text_line = text_line.rstrip(".")

                    if self.is_table_of_contents(text_line, CHAPTER_LV1):
                        is_menu += 1

                    page_content.append(text_line)

            if is_menu == 0 or is_menu < (len(lines_rects) - 5):
                continue
            else:
                last_toc_page = i + 1
                table_of_contents += page_content

        return last_toc_page, table_of_contents

    def ocr_content(self, list_page):
        text = ""

        for page in list_page:
            lines_rects = detect_line_word(page)

            for line in lines_rects:
                roi = crop_box(page, line)
                text_line = pytesseract.image_to_string(roi, lang="vie").strip()
                text_line = self.clear_text(text_line)
                text += text_line + " "

        return text

    def summary_book(self, book_link, size_sumary, is_page=True):
        text_sumary = "Nội dung tóm tắt"
        pages_np = pdf_to_image_np(book_link)
        numbers_page_use_check_menu = 5

        list_page_check_menu = pages_np[:numbers_page_use_check_menu]
        last_toc_page, table_of_contents = self.extract_table_of_contents(list_page_check_menu)
        table_of_contents = assign_levels(table_of_contents)
        save_menu_to_txt(table_of_contents, file_path="./output/menu2.txt")
        pages_np_content = pages_np[last_toc_page:]

        content_book = self.ocr_content(pages_np_content)
        chapter_content = split_content_by_toc(content_book, table_of_contents)

        summarize_all = ""
        for i, chapter_content_item in enumerate(chapter_content):
            percent = 20
            chapter_summarize = summarize_text(chapter_content_item, percent)
            summarize_all += "Chapter " + str(i) + ": " + chapter_summarize + "\n"

        with open("./output/noidung_tomtat1.txt", "w", encoding="utf-8") as file:
            file.write(summarize_all)
        return text_sumary

if __name__ == "__main__":
    book_link = "./datasets/book_test/book_kiemthuvadambaochatluongPM-1-10.pdf"
    size_sumary = 20
    is_page = False
    summarizer = SummaryBook()
    summarizer.summary_book(book_link, size_sumary, is_page)
