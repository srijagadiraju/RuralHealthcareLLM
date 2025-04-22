from transformers import AutoTokenizer

# load the tokenizer globally for BioBERT / PubMedBERT

# switch between them
# PubMedBert
# tokenizer = AutoTokenizer.from_pretrained(
#     "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract")

# BioBert
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
