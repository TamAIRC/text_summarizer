import os
import cv2
from src.ocr.ocr_image import crop_box


def save_crop_image(image, box, image_name, output_dir="./output/line"):
    os.makedirs(output_dir, exist_ok=True)

    roi = crop_box(image, box)
    # Đặt tên cho tệp tin ảnh
    filename = os.path.join(output_dir, f"{image_name}.jpg")

    # Lưu ảnh vào tệp tin
    cv2.imwrite(filename, roi)


def save_menu_to_txt(menu, file_path="./output/menu.txt"):
    with open(file_path, "w", encoding="utf-8") as file:
        for item in menu:
            title = item.get("title", "")
            subsections = item.get("subsections", [])
            file.write(title + "\n")
            for subsection in subsections:
                sub_title = subsection.get("title", "")
                file.write("\t" + sub_title + "\n")


table_of_contents = [
    {"title": "MỞ ĐẢU"},
    {"title": "CHƯƠNG 1 CÁC KHÁI NIỆM", "subsections": [{"title": "Các định nghĩa"}]},
    {"title": "Vòng đời của việc kiểm nghiệm (testing life cycle)"},
    {
        "title": "Phân loại kiểm nghiệm",
        "subsections": [
            {"title": "Sự tương quan giữa các công đoạn xây dụng phần mềm và loại kiểm"}
        ],
    },
    {
        "title": "nghiệm Mô hình chữ V",
        "subsections": [{"title": "Sơ lượt các kỹ thuật và công đoạn kiểm nghiệm"}],
    },
    {
        "title": "CHƯƠNG 2 KIÊM CHỨNG VÀ XÁC NHẬN (V V)",
        "subsections": [
            {
                "title": "Kiểm chứng và hợp lệ hoá",
                "subsections": [{"title": "Tổ chức việc kiểm thử phần mềm"}],
            },
            {
                "title": "Chiến lược kiểm thử phần mềm",
                "subsections": [{"title": "Tiêu chuẩn hoàn thành kiểm thử"}],
            },
            {
                "title": "Phát triển phần mềm phòng sạch (cleanroom software development)",
                "subsections": [
                    {"title": "Nghệ thuật của việc gỡ rồi"},
                    {"title": "Tiến trình gỡ lỗi"},
                    {"title": "Xem xét tâm lý"},
                    {"title": "Cách tiếp cận gỡ lỗi"},
                ],
            },
        ],
    },
    {
        "title": "CHƯƠNG 3 KIỂM THỬ PHẢN MÈM",
        "subsections": [
            {"title": "Quá trình kiểm thử"},
            {"title": "Kiểm thử hệ thống"},
            {"title": "Kiểm thử tích hợp"},
        ],
    },
    {
        "title": "Kiểm thử phát hành",
        "subsections": [
            {"title": "Kiểm thử hiệu năng"},
            {"title": "Kiểm thử thành phân"},
            {"title": "Kiểm thử giao diện"},
        ],
    },
    {
        "title": "Thiết kế trường hợp thử (Test case design)",
        "subsections": [{"title": "Tự động hóa kiểm thử (Test automation)"}],
    },
    {
        "title": "CHƯƠNG 4 CÁC PHƯƠNG PHÁP KIÊM THỬ",
        "subsections": [
            {"title": "Phương pháp white-box"},
            {"title": "Phương pháp black-box"},
        ],
    },
    {
        "title": "CHƯƠNG 5 KIÊM THỬ TÍCH HỢP",
        "subsections": [
            {"title": "Tích hợp trên xuống"},
            {"title": "Tích hợp dưới lên"},
        ],
    },
    {"title": ""},
    {"title": "Gợi ý về việc kiểm thử tích hợp"},
    {"title": "Lập tài liệu về kiểm thử tích hợp"},
    {
        "title": "CHƯƠNG 6 KỸ NGHỆ ĐỘ TIN CẬY PHẢN MÈM",
        "subsections": [
            {"title": "- Giới thiệu"},
            {
                "title": "Xác nhận tính tin cậy",
                "subsections": [
                    {"title": "Sơ thảo hoạt động"},
                    {"title": "Dự đoán tính tin cậy"},
                ],
            },
            {
                "title": "Đảm bảo tính an toàn",
                "subsections": [
                    {"title": "Những luận chứng về tính an toàn"},
                    {"title": "Đảm bảo quy trình"},
                    {"title": "Kiểm tra tính an toàn khi thực hiện"},
                ],
            },
            {"title": "Các trường hợp an toàn và tin cậy được"},
        ],
    },
]
if __name__ == "__main__":
    # Đường dẫn đến tệp văn bản để lưu danh sách mục lục
    file_path = "./output/menu.txt"
    # Lưu danh sách mục lục vào tệp văn bản
    save_menu_to_txt(table_of_contents, file_path)

    print("Danh sách mục lục đã được lưu vào file:", file_path)
