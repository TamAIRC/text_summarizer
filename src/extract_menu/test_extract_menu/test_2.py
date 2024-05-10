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

    lines = text.split("\n")

    for line in lines:
        # Kiểm tra nếu dòng không trống
        if line.strip():
            # Nếu dòng bắt đầu bằng một chữ số
            if line.strip()[0].isdigit() or line.strip()[0] == ",":
                level = line.count(".")
                title = line.strip()[line.index(" ") + 1 :]
                table_of_contents.append({"level": level, "title": title})
            else:
                # Nếu không có dấu chấm, gán cấp độ là 1
                title = line.strip()
                table_of_contents.append({"level": 1, "title": title})

    return table_of_contents


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


def build_toc_structure(table_of_contents):
    toc_structure = []

    for item in table_of_contents:
        if item["level"] == 1:
            toc_structure.append({"title": item["title"], "subsections": []})
            current_chapter = toc_structure[-1]
        elif item["level"] == 2:
            current_chapter["subsections"].append(
                {"title": item["title"], "subsections": []}
            )
            current_section = current_chapter["subsections"][-1]
        elif item["level"] == 3:
            current_section["subsections"].append({"title": item["title"]})
    for item in toc_structure:
        remove_empty_subsections(item)
    return toc_structure


file_path = r"D:\Product\text_summarizer\datasets\data_text\book\table_of_contents.txt"
with open(file_path, "r", encoding="utf-8") as file:
    table_of_contents_text = file.read()

table_of_contents = generate_table_of_contents(table_of_contents_text)


formatted_toc = build_toc_structure(table_of_contents)
formatted_json = json.dumps(formatted_toc, indent=4, ensure_ascii=False)
print(formatted_json)
