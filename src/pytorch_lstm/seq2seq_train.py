import random
import pandas as pd

import torch
import torch.nn as nn
import torch.optim as optim

try:
    from config.config import DEVICE
    from src.pytorch_lstm.helpers import preprocess_text

except ImportError:
    from helpers import add_path_init, preprocess_text

    add_path_init()
    from config import DEVICE


# Định nghĩa Encoder
class Encoder(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(Encoder, self).__init__()
        self.hidden_size = hidden_size
        self.embedding = nn.Embedding(input_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size)

    def forward(self, input, hidden):
        embedded = self.embedding(input).view(1, 1, -1)
        output = embedded
        output, hidden = self.gru(output, hidden)
        return output, hidden

    def initHidden(self):
        return torch.zeros(
            1, 1, self.hidden_size, device=DEVICE
        )  # Sử dụng DEVICE ở đây


# Định nghĩa Decoder
class Decoder(nn.Module):
    def __init__(self, hidden_size, output_size):
        super(Decoder, self).__init__()
        self.hidden_size = hidden_size
        self.embedding = nn.Embedding(output_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size)
        self.out = nn.Linear(hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input, hidden):
        output = self.embedding(input).view(1, 1, -1)
        output = nn.functional.relu(output)
        output, hidden = self.gru(output, hidden)
        output = self.softmax(self.out(output[0]))
        return output, hidden

    def initHidden(self):
        return torch.zeros(
            1, 1, self.hidden_size, device=DEVICE
        )  # Sử dụng DEVICE ở đây


# Xây dựng từ điển
class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {0: "SOS", 1: "EOS"}
        self.n_words = 2  # Count SOS and EOS

    def addSentence(self, sentence):
        for word in sentence.split(" "):
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1


# Định nghĩa token bắt đầu (Start Of Sentence)
SOS_token = 0

# Định nghĩa token kết thúc (End Of Sentence)
EOS_token = 1


# Hàm huấn luyện mô hình
def train(
    input_tensor,
    target_tensor,
    encoder,
    decoder,
    encoder_optimizer,
    decoder_optimizer,
    criterion,
    max_length=10,
):
    encoder_hidden = encoder.initHidden().to(DEVICE)

    encoder_optimizer.zero_grad()
    decoder_optimizer.zero_grad()

    input_length = input_tensor.size(0)
    target_length = target_tensor.size(0)

    loss = 0

    # Chuyển target_tensor sang DEVICE
    target_tensor = target_tensor.to(DEVICE)

    for ei in range(input_length):
        encoder_output, encoder_hidden = encoder(
            input_tensor[ei].to(DEVICE), encoder_hidden
        )

    decoder_input = torch.tensor([[SOS_token]], device=DEVICE)

    decoder_hidden = encoder_hidden

    for di in range(target_length):
        decoder_output, decoder_hidden = decoder(decoder_input, decoder_hidden)
        topv, topi = decoder_output.topk(1)
        decoder_input = topi.squeeze().detach()

        loss += criterion(decoder_output, target_tensor[di])
        if decoder_input.item() == EOS_token:
            break

    loss.backward()

    encoder_optimizer.step()
    decoder_optimizer.step()

    return loss.item() / target_length


def save_model(encoder, decoder, encoder_optimizer, decoder_optimizer, filename):
    try:
        state = {
            "encoder_state_dict": encoder.state_dict(),
            "decoder_state_dict": decoder.state_dict(),
            "encoder_optimizer_state_dict": encoder_optimizer.state_dict(),
            "decoder_optimizer_state_dict": decoder_optimizer.state_dict(),
        }
        torch.save(state, filename)
        return True
    except Exception as e:
        print(f"Error saving model: {e}")
        return False


def load_model(encoder, decoder, encoder_optimizer, decoder_optimizer, filename):
    state = torch.load(filename)
    encoder.load_state_dict(state["encoder_state_dict"])
    decoder.load_state_dict(state["decoder_state_dict"])
    encoder_optimizer.load_state_dict(state["encoder_optimizer_state_dict"])
    decoder_optimizer.load_state_dict(state["decoder_optimizer_state_dict"])


# Hàm chuyển đổi chuỗi thành tensor
def indexesFromSentence(lang, sentence):
    return [lang.word2index[word] for word in sentence.split(" ")]


def tensorFromSentence(lang, sentence):
    indexes = indexesFromSentence(lang, sentence)
    indexes.append(EOS_token)
    return torch.tensor(indexes, dtype=torch.long, device=DEVICE).view(
        -1, 1
    )  # Chuyển tensor sang DEVICE


def main():

    data_link = "./dataset/data_train_test.csv"
    df = pd.read_csv(data_link)

    # print(df)
    df["fulltext"] = df["fulltext"].apply(preprocess_text)
    df["summary"] = df["summary"].apply(preprocess_text)

    input_lang = Lang("fulltext")
    output_lang = Lang("summary")

    for index, row in df.iterrows():
        input_lang.addSentence(row["fulltext"])
        output_lang.addSentence(row["summary"])

    def tensorsFromPair(pair):
        input_tensor = tensorFromSentence(input_lang, pair[0])
        target_tensor = tensorFromSentence(output_lang, pair[1])
        return (input_tensor, target_tensor)

    # Định nghĩa tham số
    hidden_size = 256
    # Khởi tạo mô hình và bộ tối ưu hóa
    print("Khởi tạo mô hình và bộ tối ưu hóa")
    encoder = Encoder(input_lang.n_words, hidden_size).to(DEVICE)
    decoder = Decoder(hidden_size, output_lang.n_words).to(DEVICE)
    encoder_optimizer = optim.Adam(encoder.parameters(), lr=0.01)
    decoder_optimizer = optim.Adam(decoder.parameters(), lr=0.01)
    criterion = nn.NLLLoss()
    # print(f"encoder:{encoder}")
    # print(f"decoder:{decoder}")
    # print(f"encoder_optimizer:{encoder_optimizer}")
    # print(f"decoder_optimizer:{decoder_optimizer}")
    pairs = []
    for index, row in df.iterrows():
        pairs.append((row["fulltext"], row["summary"]))
    # Huấn luyện mô hình
    print("Huấn luyện mô hình")
    # n_iters = 10000
    n_iters = 1000
    for iter in range(1, n_iters + 1):
        print(f"iter:{iter}")
        training_pair = tensorsFromPair(random.choice(pairs))
        input_tensor = training_pair[0]
        target_tensor = training_pair[1]

        loss = train(
            input_tensor,
            target_tensor,
            encoder,
            decoder,
            encoder_optimizer,
            decoder_optimizer,
            criterion,
        )
        print(f"loss:{loss}")

    print("Lưu mô hình")

    saved_successfully = save_model(
        encoder, decoder, encoder_optimizer, decoder_optimizer, "seq2seq_model.pth"
    )

    if saved_successfully:
        print("Model saved successfully.")
    else:
        print("Failed to save model.")
    # load_model(encoder, decoder, encoder_optimizer, decoder_optimizer, 'seq2seq_model.pth')


def load_and_use_model(data_link):
    # Định nghĩa tham số
    hidden_size = 256
    MAX_LENGTH = 80
    # Load dữ liệu
    df = pd.read_csv(data_link)
    df["fulltext"] = df["fulltext"].apply(preprocess_text)
    df["summary"] = df["summary"].apply(preprocess_text)

    # Khởi tạo ngôn ngữ và chuẩn bị dữ liệu
    input_lang = Lang("fulltext")
    output_lang = Lang("summary")

    for index, row in df.iterrows():
        input_lang.addSentence(row["fulltext"])
        output_lang.addSentence(row["summary"])

    # Load mô hình đã được lưu
    encoder = Encoder(input_lang.n_words, hidden_size).to(DEVICE)
    decoder = Decoder(hidden_size, output_lang.n_words).to(DEVICE)
    encoder_optimizer = optim.Adam(encoder.parameters(), lr=0.01)
    decoder_optimizer = optim.Adam(decoder.parameters(), lr=0.01)
    loaded_successfully = load_model(
        encoder, decoder, encoder_optimizer, decoder_optimizer, "./seq2seq_model.pth"
    )

    if not loaded_successfully:
        print("Failed to load the model.")
        return

    # Lấy một cặp dữ liệu ngẫu nhiên từ dataframe để kiểm tra mô hình
    test_pair = random.choice(list(zip(df["fulltext"], df["summary"])))
    test_input_sentence, test_target_sentence = test_pair

    # Chuyển đổi câu input thành tensor
    input_tensor = tensorFromSentence(input_lang, test_input_sentence)
    # Dự đoán đầu ra sử dụng mô hình đã được load
    with torch.no_grad():
        encoder_hidden = encoder.initHidden().to(DEVICE)
        for ei in range(input_tensor.size(0)):
            encoder_output, encoder_hidden = encoder(
                input_tensor[ei].to(DEVICE), encoder_hidden
            )

        decoder_input = torch.tensor([[SOS_token]], device=DEVICE)
        decoder_hidden = encoder_hidden
        decoded_words = []
        for di in range(MAX_LENGTH):
            decoder_output, decoder_hidden = decoder(decoder_input, decoder_hidden)
            topv, topi = decoder_output.data.topk(1)
            if topi.item() == EOS_token:
                decoded_words.append("<EOS>")
                break
            else:
                decoded_words.append(output_lang.index2word[topi.item()])

            decoder_input = topi.squeeze().detach()

        decoded_sentence = " ".join(decoded_words)
        print("Input sentence:", test_input_sentence)
        print("Target sentence:", test_target_sentence)
        print("Decoded sentence:", decoded_sentence)


if __name__ == "__main__":
    data_link = "./dataset/data_train_test.csv"
    load_and_use_model(data_link)
    # main()