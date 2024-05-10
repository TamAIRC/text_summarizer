import json

# def generate_table_of_contents(text):
#     table_of_contents = []

#     lines = text.split("\n")

#     for line in lines:
#         # Kiểm tra nếu dòng không trống
#         if line.strip():
#             # Nếu dòng bắt đầu bằng một chữ số
#             if line.strip()[0].isdigit() or line.strip()[0] == ",":
#                 level = line.count(".")
#                 title = line.strip()[line.index(" ") + 1 :]
#                 table_of_contents.append({"title": title})
#             else:
#                 # Nếu không có dấu chấm, gán cấp độ là 1
#                 title = line.strip()
#                 table_of_contents.append({"title": title})

#     return table_of_contents


def generate_table_of_contents(text):
    table_of_contents = []

    for line in text.split("\n"):
        # Kiểm tra nếu dòng không trống
        if line.strip():
            # Xác định cấp độ và tiêu đề
            if line.strip()[0].isdigit() or line.strip()[0] == ",":
                level = line.count(".")
                title = line.strip()[line.index(" ") + 1 :]
            else:
                # Nếu không có dấu chấm, gán cấp độ là 1
                level = 1
                title = line.strip()

            table_of_contents.append({"level": level, "title": title})

    return table_of_contents


def build_toc_structure(table_of_contents):
    toc_structure = []
    stack = [toc_structure]

    for item in table_of_contents:
        # Adjust the stack size if needed
        while len(stack) > item["level"]:
            stack.pop()

        # Get the current chapter from the top of the stack
        current_chapter = stack[-1]

        if item["level"] == 1:
            # Append a new chapter at the top level
            new_chapter = {"title": item["title"], "subsections": []}
            current_chapter.append(new_chapter)
            stack.append(new_chapter["subsections"])
        else:
            # Append a new section to the current chapter
            new_section = {"title": item["title"], "subsections": []}
            current_chapter.append(new_section)
            stack.append(new_section["subsections"])
    for item in toc_structure:
        remove_empty_subsections(item)
    return toc_structure


def remove_empty_subsections(section):
    if "subsections" in section:
        section["subsections"] = [
            subsection for subsection in section["subsections"] if subsection
        ]
        for subsection in section["subsections"]:
            remove_empty_subsections(subsection)


file_path = r"D:\Product\text_summarizer\datasets\data_text\book\table_of_contents.txt"
with open(file_path, "r", encoding="utf-8") as file:
    table_of_contents_text = file.read()

table_of_contents = generate_table_of_contents(table_of_contents_text)


formatted_toc = build_toc_structure(table_of_contents)
formatted_json = json.dumps(formatted_toc, indent=4, ensure_ascii=False)
print(formatted_json)
