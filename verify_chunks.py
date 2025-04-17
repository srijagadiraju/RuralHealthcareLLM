import pandas as pd
from transformers import AutoTokenizer

# Load the original and preprocessed datasets
original_df = pd.read_csv("medquad.csv")
preprocessed_df = pd.read_csv("preprocessed_chunksBB.csv")

# Initialize PubMedBERT tokenizer
# tokenizer = AutoTokenizer.from_pretrained(
#     "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract")

tokenizer = AutoTokenizer.from_pretrained(
    "dmis-lab/biobert-base-cased-v1.1")


# Compute token lengths for original answers
original_df["original_token_length"] = original_df["answer"].apply(
    lambda x: len(tokenizer.encode(str(x), add_special_tokens=False))
)

# Compute token lengths for preprocessed answer chunks
preprocessed_df["answer_token_length"] = preprocessed_df["answer_chunk"].apply(
    lambda x: len(tokenizer.encode(str(x), add_special_tokens=False))
)

# Function to print token stats


def print_token_stats(df, token_col, label):
    print(f"\nToken Length Stats ({label}):")
    print(f"Total entries: {len(df)}")
    print(f"Chunks with 0 tokens: {(df[token_col] == 0).sum()}")
    print(f"Chunks with < 5 tokens: {(df[token_col] < 5).sum()}")
    print(f"Chunks with < 100 tokens: {(df[token_col] < 100).sum()}")
    print(f"Chunks with < 200 tokens: {(df[token_col] < 200).sum()}")
    print(f"Chunks with < 300 tokens: {(df[token_col] < 300).sum()}")
    print(f"Chunks with == 400 tokens: {(df[token_col] == 400).sum()}")
    print(f"Chunks with > 400 tokens (INVALID): {(df[token_col] > 400).sum()}")

    print("\nDescriptive Statistics:")
    print(df[token_col].describe())


# Show stats for original answers
print_token_stats(original_df, "original_token_length", "Original medquad.csv")

# Show stats for preprocessed answer chunks
print_token_stats(preprocessed_df, "answer_token_length",
                  "Preprocessed preprocessed_chunksPMB.csv")
