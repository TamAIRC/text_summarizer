import re

def assign_levels(lines, config=("Phần", "Chương", "Chapter")):
    def get_level(text):
        if len(text) == 0:
            return 0
        text_check = text[:12].replace(' ', '')
        if (
            "." not in text_check
            or text_check.count(".") == 1
            or any(text_check.startswith(c) for c in config)
            or re.match(r'^\d+(\s|.)', text_check)
        ):
            return 1

        elif text_check.count(".") == 2 or re.match(r'^\d+\.\d+(\s|.)', text_check):
            return 2

        elif text_check.count(".") == 3 or re.match(r'^\d+\.\d+\.\d+(\s|.)', text_check):
            return 3
        else:
            return 0

    def fix_numbering(lines):
        corrected_lines = []
        for line in lines:
            corrected_line = re.sub(r'(\d+)\s(\d+)', r'\1.\2', line)
            corrected_line = re.sub(r'(\d+)\s(\d+)\s(\d+)', r'\1.\2.\3', corrected_line)
            corrected_lines.append(corrected_line)
        return corrected_lines

    def merge_lines(lines):
        merged_lines = []
        i = 0
        while i < len(lines):
            if i + 1 < len(lines) and get_level(lines[i]) == 1 and get_level(lines[i + 1]) == 0:
                merged_lines.append(lines[i] + ' ' + lines[i + 1])
                i += 2
            else:
                merged_lines.append(lines[i])
                i += 1
        return merged_lines

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

        # Build subtree for the current node
        next_index = index + 1
        non_empty_subsections = []
        while next_index < len(lines):
            next_line = lines[next_index]
            next_level = get_level(next_line)
            if next_level == 0 or next_level <= current_level:
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

    # Fix numbering and merge lines
    lines = fix_numbering(lines)
    lines = merge_lines(lines)

    # Build tree from lines array
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

# Danh sách mục lục trích xuất được với các lỗi OCR
table_of_contents_lines = [
    'MỞ ĐẢO', 'CHƯƠNG 1 CÁC KHÁI NIỆM', '1.1. Các định nghĩa', 
    '1 2. Vòng đời của việc kiểm nghiệm (testing life cycle)', 
    '13. Phân loại kiểm nghiệm', '1.4. Sự tương quan giữa các công đoạn xây dụng phần mềm và loại kiểm', 
    'nghiệm Mô hình chữ V', '1.5. Sơ lượt các kỹ thuật và công đoạn kiểm nghiệm', 
    'CHƯƠNG 2 KIÊM CHỨNG VÀ XÁC NHẬN (V V)', '2.1. Kiểm chứng và hợp lệ hoá', 
    '2.1.1. Tổ chức việc kiểm thử phần mềm', '2.1.2. Chiến lược kiểm thử phần mềm', 
    '2.1.3. Tiêu chuẩn hoàn thành kiểm thử', '2.2. Phát triển phần mềm phòng sạch (cleanroom software development)', 
    '2.2.1. Nghệ thuật của việc gỡ rồi', '2.2.2. Tiến trình gỡ lỗi', '2.2.3. Xem xét tâm lý', 
    '2.2.4. Cách tiếp cận gỡ lỗi', 'CHƯƠNG 3 KIỂM THỬ PHẢN MÈM', '3.1. Quá trình kiểm thử', 
    '3.2. Kiểm thử hệ thống', '3.3. Kiểm thử tích hợp', '3.4 Kiểm thử phát hành', 
    '3.5. Kiểm thử hiệu năng', '3.6. Kiểm thử thành phân', '3.7. Kiểm thử giao diện', 
    '3.8. Thiết kế trường hợp thử (Test case design)', '3.9. Tự động hóa kiểm thử (Test automation)', 
    'CHƯƠNG 4 CÁC PHƯƠNG PHÁP KIÊM THỬ', '4.1. Phương pháp white-box', '4.2. Phương pháp black-box', 
    'CHƯƠNG 5 KIÊM THỬ TÍCH HỢP', '5.1. Tích hợp trên xuống', '5.2. Tích hợp dưới lên', 
    '5.3', '5.4 Gợi ý về việc kiểm thử tích hợp', '5.5 Lập tài liệu về kiểm thử tích hợp', 
    'CHƯƠNG 6 KỸ NGHỆ ĐỘ TIN CẬY PHẢN MÈM', '6.1. - Giới thiệu', '6.2. Xác nhận tính tin cậy', 
    '6.2.1. Sơ thảo hoạt động', '6.2.2. Dự đoán tính tin cậy', '6.3. Đảm bảo tính an toàn', 
    '6.3.1. Những luận chứng về tính an toàn', '6.3.2. Đảm bảo quy trình', 
    '6.3.3. Kiểm tra tính an toàn khi thực hiện', '6.4. Các trường hợp an toàn và tin cậy được'
]

# Sử dụng function assign_levels để tạo cây mục lục
table_of_contents = assign_levels(table_of_contents_lines)

# In ra cây mục lục
import json
print(json.dumps(table_of_contents, indent=2, ensure_ascii=False))
