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
table_of_contents_lines = [
    "MỞ ĐẢO",
    "CHƯƠNG 1 CÁC KHÁI NIỆM",
    "1.1. Các định nghĩa",
    "1 2. Vòng đời của việc kiểm nghiệm (testing life cycle)",
    "13. Phân loại kiểm nghiệm",
    "1.4. Sự tương quan giữa các công đoạn xây dụng phần mềm và loại kiểm",
    "nghiệm Mô hình chữ V",
    "1.5. Sơ lượt các kỹ thuật và công đoạn kiểm nghiệm",
    "CHƯƠNG 2 KIÊM CHỨNG VÀ XÁC NHẬN (V V)",
    "2.1. Kiểm chứng và hợp lệ hoá",
    "2.1.1. Tổ chức việc kiểm thử phần mềm",
    "2.1.2. Chiến lược kiểm thử phần mềm",
    "2.1.3. Tiêu chuẩn hoàn thành kiểm thử",
    "2.2. Phát triển phần mềm phòng sạch (cleanroom software development)",
    "2.2.1. Nghệ thuật của việc gỡ rồi",
    "2.2.2. Tiến trình gỡ lỗi",
    "2.2.3. Xem xét tâm lý",
    "2.2.4. Cách tiếp cận gỡ lỗi",
    "CHƯƠNG 3 KIỂM THỬ PHẢN MÈM",
    "3.1. Quá trình kiểm thử",
    "3.2. Kiểm thử hệ thống",
    "3.3. Kiểm thử tích hợp",
    "3.4 Kiểm thử phát hành",
    "3.5. Kiểm thử hiệu năng",
    "3.6. Kiểm thử thành phân",
    "3.7. Kiểm thử giao diện",
    "3.8. Thiết kế trường hợp thử (Test case design)",
    "3.9. Tự động hóa kiểm thử (Test automation)",
    "CHƯƠNG 4 CÁC PHƯƠNG PHÁP KIÊM THỬ",
    "4.1. Phương pháp white-box",
    "4.2. Phương pháp black-box",
    "CHƯƠNG 5 KIÊM THỬ TÍCH HỢP",
    "5.1. Tích hợp trên xuống",
    "5.2. Tích hợp dưới lên",
    "5.3",
    "5.4 Gợi ý về việc kiểm thử tích hợp",
    "5.5 Lập tài liệu về kiểm thử tích hợp",
    "CHƯƠNG 6 KỸ NGHỆ ĐỘ TIN CẬY PHẢN MÈM",
    "6.1. - Giới thiệu",
    "6.2. Xác nhận tính tin cậy",
    "6.2.1. Sơ thảo hoạt động",
    "6.2.2. Dự đoán tính tin cậy",
    "6.3. Đảm bảo tính an toàn",
    "6.3.1. Những luận chứng về tính an toàn",
    "6.3.2. Đảm bảo quy trình",
    "6.3.3. Kiểm tra tính an toàn khi thực hiện",
    "6.4. Các trường hợp an toàn và tin cậy được",
]
import json
import re

try:
    from config.config_text import LV1_KEYWORDS
except:
    from helpers import add_path_init

    add_path_init()
    from config_text import LV1_KEYWORDS


def assign_levels(lines, config=LV1_KEYWORDS):
    def get_level(text):
        if len(text) == 0:
            return 0
        text_check = text[:12]
        text_check.lower()
        if (
            "." not in text_check
            or text_check.count(".") == 1
            or any(text_check.startswith(c) for c in config)
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
    # table_of_contents = muc_luc.split("\n")

    result = assign_levels(table_of_contents_lines)
    # print(result)
    formatted_json = json.dumps(result, indent=2, ensure_ascii=False)
    print(formatted_json)
    # Lưu kết quả vào một tệp JSON
    with open("toc_structure.json", "w", encoding="utf-8") as json_file:
        json.dump(result, json_file, indent=2, ensure_ascii=False)

    print("Kết quả đã được lưu vào tệp 'toc_structure.json'.")
