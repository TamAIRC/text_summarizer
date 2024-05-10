# Mục lục có cấu trúc:
muc_luc = """
MỤC LỤC
Mục đích và phạm vi áp dụng kiến trúc Chính phủ điện tử TTXVN.
1.1. Giới thiệu chung về Khung kiến trúc Chính phủ điện tử
1.2. Sự cần thiết xây dựng Kiến trúc Chính phủ điện tử tại Thông tấn xã Việt Nam
1.3. Mục đích và phạm vi áp dụng
Hiện trạng hệ thống Công nghệ thông tin và Chính phủ điện tử tại Thông tấn xã Việt Nam
2.1. Hiện trạng triển khai ứng dụng CNTT tại Thông tấn xã Việt Nam
2.2. Các hệ thống ứng dụng CNTT của TTXVN.
2.2.1. Hệ thống tác nghiệp phục vụ sản xuất thông tin
2.2.2. Các ứng dụng của Hệ thống kỹ thuật sản xuất tin truyền hình
2.2.3. Hệ thống phục vụ quản lý hành chính nhà nước
2.2.4. Trung tâm dữ liệu.
2.2.5. Hệ thống đảm bảo an toàn thông tin.
2.3. Hiện trạng triển khai CPĐT tại TTXVN
2.3.1. Khung kiến trúc CPĐT Việt Nam
2.3.2. Đánh giá
Định hướng Kiến trúc Chính phủ điện tử Thông tấn xã Việt Nam
3.1. Chức năng, nhiệm vụ của TTXVN.
3.2. Cơ cấu tổ chức TTXVN
3.3. Tầm nhìn, định hướng phát triển Chính phủ điện tử TTXVN
Các nguyên tắc xây dựng kiến trúc Chính phủ điện tử TTXVN
Kiến trúc Chính phủ điện tử Thông tấn xã Việt Nam
5.1. Sơ đồ tổng thể Kiến trúc Chính phủ điện tử TTXVN
5.2. Người sử dụng
5.3. Kênh truy cập
5.4. Dịch vụ cổng thông tin điện tử.
5.5. Dịch vụ công trực tuyến (Dịch vụ thông tin)
5.6. Ứng dụng và cơ sở dữ liệu
5.7. Các dịch vụ chia sẻ và tích hợp
5.7.1. Nền tảng tích hợp dịch vụ CPĐT (LGSP).
5.7.2. Nền tảng dịch vụ dùng chung
5.7.3 Nền tảng tích hợp ứng dụng
5.7.4. Các dịch vụ tích hợp và liên thông dữ liệu
5.8. Các nguyên tắc, yêu cầu trong việc triển khai các thành phần trong Kiến trúc CPĐT TTXVN
5.8.1. Nguyên tắc
5.8.2. Yêu cầu về nghiệp vụ
5.8.3. Yêu cầu về kỹ thuật
6. Lộ trình/kế hoạch/nguồn kinh phí triển khai các thành phần trong kiến trúc
6.1. Lộ trình triển khai kiến trúc Chính phủ điện tử TTXVN
6.2. Kế hoạch triển khai
6.3. Kinh phí thực hiện.
Tổ chức triển khai Kiến trúc Chính phủ điện tử TTXVN
7.1. Công tác chỉ đạo triển khai kiến trúc CPĐT TTXVN
7.2. Công tác quản lý, giám sát, duy trì Kiến trúc CPĐT TTXVN
7.3. Trách nhiệm của đơn vị chuyên trách CNTT (Trung tâm Tin học)
,.4. Trách nhiệm của các đơn vị trong TTXVN
7.5. Trách nhiệm của các ban quản lý
7.5.1. Trách nhiệm của Ban Kế hoạch - Tài chính.
7.5.z. Trách nhiệm của Văn phòng TTXVN
7.5.3. Trách nhiệm của Ban Tổ chức - Cán bộ
"""
import json
import re


def assign_levels(lines, config=("Phần", "Chương", "Chapter")):
    def get_level(text):
        if len(text) == 0:
            return 0
        text_check = text[:12]
        if (
            "." not in text_check
            or text_check.count(".") == 1
            or text_check.startswith(config)
            or text_check.startswith(("{}. ", "{} "))
        ):
            return 1

        elif text_check.count(".") == 2 or text_check.startswith(("{}.{}. ", "{}.{} ")):
            return 2

        elif text_check.count(".") == 3 or text_check.startswith(
            ("{}.{}.{}. ", "{}.{}.{} ")
        ):
            return 3
        else:
            return 0

    def build_tree(lines, index):
        if index >= len(lines):
            return None

        current_line = lines[index].rstrip(".")
        current_level = get_level(current_line)
        if current_level == 0:
            return None
        if "." in current_line:
            current_text = current_line.split(". ", 1)[-1]
            current_text = re.sub(r"^\d+(\.\d+)*\s*", "", current_text)
        else:
            current_text = current_line

        node = {"title": current_text.strip()}

        # Xây dựng cây con của nút hiện tại
        next_index = index + 1
        non_empty_subsections = []
        while next_index < len(lines):
            next_line = lines[next_index]
            next_level = get_level(next_line)
            if next_level == 0:
                break
            if next_level <= current_level:
                break

            child_node = build_tree(lines, next_index)
            if child_node and child_node["title"]:
                non_empty_subsections.append(child_node)
                next_index += count_child_nodes(child_node) + 1
            else:
                break

        if non_empty_subsections:
            node["subsections"] = non_empty_subsections

        return node

    def count_child_nodes(node):
        count = 0
        if "subsections" in node:
            for child in node["subsections"]:
                count += 1 + count_child_nodes(child)
        return count

    # Xây dựng cây từ mảng dòng
    tree = []
    index = 0
    while index < len(lines):
        node = build_tree(lines, index)
        if node:
            tree.append(node)
            index += count_child_nodes(node) + 1
        else:
            index += 1

    return tree


if __name__ == "__main__":
    # Gọi hàm detect_table_of_contents để nhận diện format mục lục
    table_of_contents = muc_luc.split("\n")

    result = assign_levels(table_of_contents)
    # print(result)
    formatted_json = json.dumps(result, indent=2, ensure_ascii=False)
    print(formatted_json)
