import json

from unidecode import unidecode


# Hàm để tìm vị trí của tiêu đề trong nội dung
def find_title_index(title, content):
    return content.find(title)


def split_content_by_toc(content, toc):
    copy_content = unidecode(content)
    chapters = []
    for i in range(len(toc)):
        title = unidecode(toc[i]["title"])
        start_index = find_title_index(title, copy_content)
        next_title = unidecode(toc[i + 1]["title"]) if i < len(toc) - 1 else None
        end_index = (
            len(content)
            if next_title is None
            else find_title_index(next_title, copy_content)
        )
        chapters.append(content[start_index:end_index].strip())
        content = content[:start_index] + content[end_index:]  # Xoá phần đã cắt
        copy_content = copy_content[:start_index] + copy_content[end_index:]
    return chapters


if __name__ == "__main__":
    # Đọc nội dung từ tệp content.txt
    content_path = r"D:\Product\text_summarizer\datasets\data_text\book\content.txt"
    with open(content_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Đọc mục lục từ tệp toc_structure.json
    menu_path = r"D:\Product\text_summarizer\datasets\data_text\book\toc_structure.json"
    with open(menu_path, "r", encoding="utf-8") as file:
        toc = json.load(file)
    # Phân chia nội dung thành các chương dựa trên mục lục
    chapters = split_content_by_toc(content, toc)

    # In ra số lượng chương và một số ví dụ
    print("Số lượng chương:", len(chapters))
    # for i in range(min(3, len(chapters))):
    #     print("\nChương {}: {}".format(i + 1, chapters[i]))

    # Nếu bạn muốn lưu các chương vào các tệp riêng, bạn có thể làm như sau:
    for i, chapter in enumerate(chapters):
        with open("chapter_{}.txt".format(i + 1), "w", encoding="utf-8") as file:
            file.write(chapter)
