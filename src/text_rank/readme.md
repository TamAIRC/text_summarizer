# Text summarization with text rank

## Preprocessing

**Remove Extra Spaces**: This function removes any extra spaces within the text.
Replace Punctuation: Punctuation marks such as ;, !, :, @, and _ are replaced with periods (.).

**Keep Vietnamese Letters and Numbers**: This function keeps only Vietnamese letters, digits, whitespace, and periods in the text, removing any other characters.

**Get List of Sentences**: Split the text into sentences and tokenize each sentence using the ViTokenizer from pyvi library. Then convert each sentence to lowercase and split it into words. Only sentences longer than 35 characters are considered.

**Process Text**: Apply the above preprocessing steps to the input document and return a list of processed sentences.

**Process After**: Reconstruct the processed sentences into a coherent text format by joining words within each sentence and adding periods at the end of each sentence.


## TextRank

**Build Similarity Matrix**: Calculate the similarity between each pair of sentences in the input document. This similarity is computed using cosine similarity between the vector representations of the sentences.

**PageRank Algorithm****: Apply the PageRank algorithm to the similarity matrix to determine the importance score (rank) of each sentence. PageRank is an algorithm used to rank web pages in Google Search, but it can also be applied to ranking sentences.

**Sort Sentences by Rank**: Sort the sentences based on their PageRank scores in descending order to identify the most important sentences.

**Select Top Sentences**: Select the top N sentences with the highest PageRank scores to form the summary. The value of N can be determined based on a predetermined percentage of the total number of sentences or a fixed number of sentences.

**Generate Summary**: Reconstruct the selected sentences into a coherent summary by joining them together.

## Setup

# Run

```
streamlit run app.py
```

or

```
python text_rank.py
```


## Sửa các đường dẫn sau để sử dụng text_rank.py
- sửa sys.path text_rank/preprocessing
- sửa sys.pth VietnameseOcrCorrection/predictor
