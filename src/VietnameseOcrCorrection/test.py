from tool.predictor import Predictor
import time
from tool.utils import extract_phrases

weight_path = "./weights/seq2seq_0.pth"
# weight_path = "./weights/transformer_0.pth"
model_predictor = Predictor(device="cpu", model_type="seq2seq", weight_path=weight_path)
p = "Tren cơsở kếT qua kiem tra hien trang, Tòa an nhân dân tối cao xẻm xét, lap phương án sắp xếp lại, xử lý \
    các cơ sở nhà, đất thuộc phám vi Quả lý, gửi lấy ý kiến của Ủy ban nhân dân cấp tỉnh nơi co nha, đất."
outs = model_predictor.predict(p.strip(), NGRAM=6)
print(outs)
