# ls = [1, 2, 3, 4, 5]
# print(ls[2:])
import json
import re

def remove_empty_subsections(section):
    if "subsections" in section:
        # Check if the current section has subsections
        if not section["subsections"]:
            # If it doesn't have subsections, remove the key
            del section["subsections"]
        else:
            # If it has subsections, recursively call this function for each subsection
            for subsection in section["subsections"]:
                remove_empty_subsections(subsection)

def fix_table_of_contents(table_of_contents):
    toc_data = []
    current_chapter = None

    for line in table_of_contents:
        # Tìm số đầu tiên trong dòng
        match = re.match(r"^(\d+(\.\d+)*)?\s*(.*)", line.strip())
        if match:
            # print("menu",match.group(1).split(".") if match.group(1) else "ok")
            # Nếu có số, xác định cấp độ và tiêu đề
            level = len(match.group(1).split(".")) if match.group(1) else 1
            title = match.group(3)

            # Nếu không có số, tự động gán cấp độ 1
            if not match.group(1):
                level = 1

            # Chuyển đổi số 1 thành cấp độ 1 và tạo mới một chương
            if level == 1:
                # current_chapter = title
                # toc_data.append({"title": title.lstrip(". "), "subsections": []})
                current_chapter = {"title": title.lstrip(". "), "subsections": []}
                toc_data.append(current_chapter)
            # Nếu không có số, tự động chuyển thành cấp độ 2
            elif current_chapter:
                # Thêm mục vào cấp độ phù hợp
                # current_section = toc_data[-1]["subsections"]
                current_section = current_chapter["subsections"]
                # toc_data[-1]["subsections"].append({"title": title})
                if level == 2:
                        current_section.append({"title": title.lstrip(". "), "subsections": []})
                elif level == 3:
                    current_section[-1]["subsections"].append({"title": title.lstrip(". ")})
    # Xóa key "subsections" nếu không có subsections
    for item in toc_data:
        remove_empty_subsections(item)

        
    return toc_data


table_of_contents = open(
    r"D:\Product\text_summarizer\datasets\data_text\book\table_of_contents.txt",
    encoding="utf-8",
)

# Sử dụng hàm parse_table_of_contents để chuyển đổi mục lục thành cấu trúc JSON
fixed_toc_json = fix_table_of_contents(table_of_contents)
fixed_toc_json_str = json.dumps(fixed_toc_json, indent=4, ensure_ascii=False)
print(fixed_toc_json_str)
