# from nltk.tokenize import sent_tokenize

# # use sentence tokenization or sliding window to chunk long answers


# def chunk_text(text, chunk_size=300, overlap=50):
#     sentences = sent_tokenize(text)
#     chunks = []
#     current_chunk = []
#     current_length = 0

#     for sentence in sentences:
#         sentence_length = len(sentence.split())
#         if current_length + sentence_length > chunk_size:
#             chunks.append(" ".join(current_chunk))
#             current_chunk = current_chunk[-overlap:]
#             current_length = sum(len(s.split()) for s in current_chunk)
#         current_chunk.append(sentence)
#         current_length += sentence_length

#     if current_chunk:
#         chunks.append(" ".join(current_chunk))

#     return chunks

# from nltk.tokenize import word_tokenize

# # use sentence tokenization or sliding window to chunk long answers


# def chunk_text(text, chunk_size=400, overlap=75):
#     """
#     Splits the input text into overlapping chunks based on tokens (words).

#     Args:
#         text (str): The input answer text to chunk.
#         chunk_size (int): Number of tokens per chunk.
#         overlap (int): Number of overlapping tokens between chunks.

#     Returns:
#         List[str]: A list of token-based overlapping text chunks.
#     """
#     words = text.split()  # Approximate tokenization using whitespace
#     chunks = []

#     start = 0
#     while start < len(words):
#         end = min(start + chunk_size, len(words))
#         chunk = words[start:end]
#         chunks.append(" ".join(chunk))
#         start += chunk_size - overlap  # Slide the window

#     return chunks

# use commonly used tokenizer to check token size
# also chunk questions -- if user asks a question, we can just give the full output of that question (RAG will search questions first but if no match, it will fallback to known answers)
# after using tokenizer, check if questions are longer than 400 and chunk that
# do not remove short answers

# import tiktoken


# def chunk_text(text, tokenizer=None, chunk_size=400, overlap=75):
#     """
#     Splits input text into overlapping token chunks using tiktoken.

#     Args:
#         text (str): Input text to chunk.
#         tokenizer: A tiktoken tokenizer instance.
#         chunk_size (int): Max tokens per chunk.
#         overlap (int): Number of tokens to overlap between chunks.

#     Returns:
#         List[str]: List of text chunks.
#     """
#     if tokenizer is None:
#         tokenizer = tiktoken.get_encoding(
#             "cl100k_base")  # default OpenAI tokenizer

#     tokens = tokenizer.encode(text)
#     chunks = []

#     start = 0
#     while start < len(tokens):
#         end = min(start + chunk_size, len(tokens))
#         chunk = tokens[start:end]
#         decoded_chunk = tokenizer.decode(chunk)
#         chunks.append(decoded_chunk)
#         start += chunk_size - overlap

#     return chunks


from transformers import AutoTokenizer

# Load the tokenizer globally for BioBERT / PubMedBERT
# You can switch between them by changing the model name below
# tokenizer = AutoTokenizer.from_pretrained(
#     "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract")

tokenizer = AutoTokenizer.from_pretrained(
    "dmis-lab/biobert-base-cased-v1.1")


def chunk_text(text, chunk_size=400, overlap=75):
    """
    Splits input text into overlapping token chunks using a HuggingFace tokenizer.

    Args:
        text (str): Input text to chunk.
        chunk_size (int): Max tokens per chunk.
        overlap (int): Number of overlapping tokens between chunks.

    Returns:
        List[str]: List of text chunks.
    """
    tokens = tokenizer.encode(text, add_special_tokens=False)
    chunks = []

    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        token_chunk = tokens[start:end]
        decoded_chunk = tokenizer.decode(token_chunk)
        chunks.append(decoded_chunk)
        start += chunk_size - overlap

    return chunks
