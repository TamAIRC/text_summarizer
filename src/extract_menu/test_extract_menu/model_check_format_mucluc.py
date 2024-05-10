import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Dữ liệu huấn luyện
# Ví dụ: dữ liệu được biểu diễn dưới dạng list của các tuple (văn bản, nhãn)
training_data = [
    ("MỤC LỤC", "toc"),
    ("1.1. Giới thiệu chung về Khung kiến trúc Chính phủ điện tử", "lever2"),
    ("Chương 1: Giới thiệu", "lever1"),
    ("Chương 1. Giới thiệu", "lever1"),
    ("2.1. Hiện trạng triển khai ứng dụng CNTT tại Thông tấn xã Việt Nam", "lever2"),
    ("Chương 2: Công nghệ thông tin", "lever1"),
    ("Chương 2. Công nghệ thông tin", "lever1"),
    # Thêm dữ liệu khác vào đây
]

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(
    [data[0] for data in training_data],
    [data[1] for data in training_data],
    test_size=0.2,
    random_state=42,
)

# Vector hóa văn bản sử dụng CountVectorizer
vectorizer = CountVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Huấn luyện mô hình SVM
clf = SVC(kernel="linear")
clf.fit(X_train_vectorized, y_train)

# Đánh giá mô hình trên tập kiểm tra
y_pred = clf.predict(X_test_vectorized)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
