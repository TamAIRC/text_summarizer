from preprocessing import process_text, process_after
# from preprocessing import processed_text
import numpy as np
from nltk.cluster.util import cosine_distance
from operator import itemgetter
import time

def pagerank(A, eps=0.0001, d=0.85, max_iter=1000):
    P = np.ones(len(A)) / len(A)
    iter_count = 0
    while iter_count < max_iter:
        new_P = np.ones(len(A)) * (1 - d) / len(A) + d * A.T.dot(P)
        delta = abs(new_P - P).sum()
        if delta <= eps:
            return new_P
        P = new_P
        iter_count += 1
    print("Warning: PageRank algorithm did not converge within {} iterations.".format(max_iter))
    return new_P


def build_similarity_matrix(sentences):
    S = np.zeros((len(sentences), len(sentences)))

    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:
                continue

            S[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2])

    # Normalize the rows to ensure no division by zero
    for idx in range(len(S)):
        row_sum = S[idx].sum()
        if row_sum != 0:
            S[idx] /= row_sum

    return S


def sentence_similarity(sent1, sent2):
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]

    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    for w in sent1:
        vector1[all_words.index(w)] += 1

    for w in sent2:
        vector2[all_words.index(w)] += 1

    return 1 - cosine_distance(vector1, vector2)


def textrank(sentences, top_n=3):
    S = build_similarity_matrix(sentences)
    sentence_ranks = pagerank(S)

    # Sort the sentence ranks
    ranked_sentence_indexes = [item[0] for item in sorted(enumerate(sentence_ranks), key=lambda item: -item[1])]
    selected_sentences = sorted(ranked_sentence_indexes[:top_n])
    # Collect the selected sentences
    summary = [sentences[i] for i in selected_sentences]
    return summary

def summarize_text(text, percent):
    sentences = process_text(text)
    num_sentences = int(len(sentences) * (percent / 100))
    summary_sentences = textrank(sentences, top_n=num_sentences)
    summary = ' '.join([' '.join(sentence) for sentence in summary_sentences])
    
    return summary
your_text_here = """
Năm học 2022 - 2023, Chương trình Giáo dục phổ thông 2018 bắt đầu thực hiện triển khai với lớp 3 ở cấp Tiểu học. Chương trình mới chuyển từ cách tiếp cận nội dung sang cách tiếp cận năng lực nhằm phát triển phẩm chất và năng lực người học. Đó là cách tiếp cận không những đòi hỏi học sinh nắm vững những kiến thức, kĩ năng cơ bản mà còn chú trọng yêu cầu vận dụng kiến thức, kĩ năng vào thực hành, giải quyết các tình huống trong học tập và cuộc sống; tính chất và kết quả hoạt động cũng phụ thuộc rất nhiều vào hứng thú, niềm tin, đạo đức… của người học. Chính vì vậy, khi triển khai Chương trình mới, các vấn đề liên quan đến nội dung giáo dục, phương pháp và hình thức tổ chức hoạt động giáo dục, phương pháp đánh giá kết quả giáo dục cũng có nhiều đổi mới. Sự đổi mới nhiều mặt của chương trình và sách giáo khoa đặt ra các yêu cầu mới đối với nhà trường, giáo viên và học sinh. Kết quả khảo sát, điều tra thực trạng dạy học theo Chương trình, Sách giáo khoa 2018 ở một số trường tiểu học của nhiều tỉnh thành trên cả nước cho thấy bên cạnh những cố gắng của các nhà trường trong việc đổi mới quản lí giáo dục theo hướng tiếp cận giáo dục phẩm chất, năng lực người học vẫn còn nhiều bất cập trong việc thực hiện mục tiêu giáo dục toàn diện nói chung và mục tiêu Chương trình Giáo dục phổ thông mới nói riêng. Trong Chương trình Giáo dục phổ thông 2018, môn Toán có nhiệm vụ trang bị cho học sinh học vấn Toán học phổ thông, cơ bản, hình thành và phát triển các năng lực và phẩm chất Toán học, phát triển tư duy, cách suy nghĩ và giải quyết vấn đề; chuẩn bị cho học sinh hiểu rõ hơn về thế giới mà họ đang sống, giúp họ thích ứng, tham gia tích cực và thành công vào xu thế phát triển, đổi mới, sáng tạo của thời đại. Ở cấp Tiểu học, việc triển khai dạy học môn Toán lớp 3 đã được triển khai bước sang năm thứ hai. Thực tế triển khai cũng có không ít những thuận lợi và khó khăn cần được nghiên cứu đề xuất các giải pháp nâng cao hiệu quả dạy học trong giai đoạn tiếp theo. Vì vậy, chúng tôi thực hiện nghiên cứu triển khai dạy học môn Toán lớp 3 theo Chương trình Giáo dục phổ thông 2018 nhằm phân tích, xác định, lí giải những thuận lợi và khó khăn trong quá trình dạy học, từ đó đề xuất giải pháp kịp thời, giúp nâng cao hiệu quả dạy học theo Chương trình và Sách giáo khoa mới.
"""
# Example usage:
summary = summarize_text(your_text_here, 50)  
print(summary)
# with open("summary10.txt", "w", encoding="utf-8") as f_summary, open("time10.txt", "w", encoding="utf-8") as f_time:
#     for text in processed_text:
#         num_sentences = len(text) // 10  # Số lượng câu được chọn là nửa số câu của đoạn văn bản
#         start_time = time.time()  # Thời điểm bắt đầu tính thời gian
#         summary = process_after(textrank(text, top_n=num_sentences))  # Chỉ định top_n là nửa số câu
#         end_time = time.time()    # Thời điểm kết thúc tính thời gian

#         # Tính thời gian chênh lệch và lưu vào file time.txt
#         elapsed_time = end_time - start_time
#         f_time.write(f"{elapsed_time}\n")

#         # Lưu summary vào file summary.txt
#         f_summary.write(''.join(summary) + '\n')

# sentences = []
# for text in processed_text:
#     sentences.append(process_after(textrank(text)))
# for _ in sentences:
#     print(_)

