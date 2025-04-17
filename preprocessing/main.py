# from chunker import chunk_text
# from clean import clean_text
# import pandas as pd
# import nltk
# nltk.download("punkt")


# # load the dataset using pandas and inspect key columns
# df = pd.read_csv("medquad.csv")

# # rename for convenience if needed
# df = df.rename(columns={
#     "Question": "question",
#     "Answer": "answer",
#     "Focus": "focus_area",
#     "Type": "question_type",
#     "URL": "source"
# })

# # drop null or empty rows
# df.dropna(subset=["question", "answer"], inplace=True)
# df = df[df["answer"].str.strip().astype(bool)]

# # clean text -- remove HTML, newlines, extra whitespace, convert to lowercase
# df["question"] = df["question"].apply(clean_text)
# df["answer"] = df["answer"].apply(clean_text)

# # filter out very short answers (<10 words) -- filter out answers that lack enough context for RAG retrieval
# df = df[df["answer"].apply(lambda x: len(x.split()) >= 10)]

# # create chunked dataframe --store chunks in a new DataFrame
# chunked_rows = []

# for _, row in df.iterrows():
#     answer_chunks = chunk_text(row["answer"])
#     for chunk in answer_chunks:
#         chunked_rows.append({
#             "question": row["question"],
#             "answer_chunk": chunk,
#             "focus_area": row.get("focus_area", ""),
#             "source": row.get("source", "")
#         })

# df_chunks = pd.DataFrame(chunked_rows)

# # clean up edge cases
# df_chunks = df_chunks.dropna(subset=["answer_chunk"])
# df_chunks["focus_area"] = df_chunks["focus_area"].fillna("unknown")

# # save final output
# df_chunks.to_csv("preprocessed_chunks.csv", index=False)

# # basic stats
# print("Focus Area Distribution:")
# print(df_chunks["focus_area"].value_counts())

# from chunker import chunk_text
# from clean import clean_text
# import pandas as pd
# import nltk
# from transformers import AutoTokenizer

# # Download NLTK tokenizer (required if using NLTK anywhere else)
# nltk.download("punkt")

# # initialize PubMedBERT
# tokenizer = AutoTokenizer.from_pretrained(
#     "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract")


# # Load the small test dataset
# df = pd.read_csv("medquad.csv")

# # Rename columns for consistency
# df = df.rename(columns={
#     "Question": "question",
#     "Answer": "answer",
#     "Focus": "focus_area",
#     "Type": "question_type",
#     "URL": "source"
# })

# # Drop rows where question or answer is null
# df.dropna(subset=["question", "answer"], inplace=True)

# # Clean the text
# df["question"] = df["question"].apply(clean_text)
# df["answer"] = df["answer"].apply(clean_text)

# # Remove rows where the cleaned answer has 0 tokens
# df = df[df["answer"].apply(lambda x: len(
#     tokenizer.encode(x, add_special_tokens=False)) > 0)]

# # Initialize output list
# chunked_rows = []

# # Chunk each row
# for _, row in df.iterrows():
#     question_chunks = chunk_text(row["question"], tokenizer=tokenizer)
#     answer_chunks = chunk_text(row["answer"], tokenizer=tokenizer)

#     # Add question chunks (with empty answer placeholder)
#     for q_chunk in question_chunks:
#         chunked_rows.append({
#             "question_chunk": q_chunk,
#             "answer_chunk": "",  # blank for now — these will be searched directly
#             "focus_area": row.get("focus_area", ""),
#             "source": row.get("source", "")
#         })

#     # Add answer chunks (with original question context)
#     for a_chunk in answer_chunks:
#         chunked_rows.append({
#             "question_chunk": row["question"],  # original question text
#             "answer_chunk": a_chunk,
#             "focus_area": row.get("focus_area", ""),
#             "source": row.get("source", "")
#         })

# # Create final DataFrame
# df_chunks = pd.DataFrame(chunked_rows)

# # Cleanup edge cases
# df_chunks = df_chunks.dropna(subset=["answer_chunk", "question_chunk"])
# df_chunks["focus_area"] = df_chunks["focus_area"].fillna("unknown")

# # OPTIONAL: Keep only rows where answer_chunk is not empty
# df_chunks = df_chunks[df_chunks["answer_chunk"].str.strip() != ""]

# # Save the processed output
# df_chunks.to_csv("preprocessed_chunksPMB.csv", index=False)

# # Basic inspection
# print("Chunking completed.")
# print("Sample:", df_chunks.head())

from chunker import chunk_text
from clean import clean_text
import pandas as pd
import nltk
from transformers import AutoTokenizer

# Download NLTK tokenizer
nltk.download("punkt")

# initialize PubMedBERT tokenizer
# tokenizer = AutoTokenizer.from_pretrained(
#     "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract"
# )

# initialize BioBert
tokenizer = AutoTokenizer.from_pretrained(
    "dmis-lab/biobert-base-cased-v1.1")


# Load dataset
df = pd.read_csv("medquad.csv")

# Rename columns for consistency
df = df.rename(columns={
    "Question": "question",
    "Answer": "answer",
    "Focus": "focus_area",
    "Type": "question_type",
    "URL": "source"
})

# Drop nulls
df.dropna(subset=["question", "answer"], inplace=True)

# Clean question/answer text
df["question"] = df["question"].apply(clean_text)
df["answer"] = df["answer"].apply(clean_text)

# Remove rows where answer has 0 tokens
df = df[df["answer"].apply(lambda x: len(
    tokenizer.encode(x, add_special_tokens=False)) > 0)]

# Initialize storage
chunked_rows = []
question_counter = 1  # 1-based index for each Q&A

# Process each row
for idx, row in df.iterrows():
    question_text = row["question"]
    answer_text = row["answer"]

    # Chunk question and answer
    # question_chunks = chunk_text(question_text, tokenizer=tokenizer)
    # answer_chunks = chunk_text(answer_text, tokenizer=tokenizer)
    question_chunks = chunk_text(question_text)
    answer_chunks = chunk_text(answer_text)

    # Add question chunk(s) as separate rows for fallback search
    for q_chunk in question_chunks:
        chunked_rows.append({
            "chunk_id": f"question_{question_counter:05}_1",
            "question_index": question_counter,
            "question_chunk": q_chunk,
            "answer_chunk": "",
            "chunk_index": 1,
            "total_chunks": 1,
            "focus_area": row.get("focus_area", ""),
            "source": row.get("source", "")
        })

    # Add answer chunks (with filter to remove chunks > 400 tokens)
    valid_answer_chunks = []
    for i, a_chunk in enumerate(answer_chunks):
        if len(tokenizer.encode(a_chunk, add_special_tokens=False)) <= 400:
            valid_answer_chunks.append(a_chunk)

    total = len(valid_answer_chunks)
    for i, a_chunk in enumerate(valid_answer_chunks):
        chunked_rows.append({
            "chunk_id": f"answer_{question_counter:05}_{i+1}",
            "question_index": question_counter,
            "question_chunk": question_text,
            "answer_chunk": a_chunk,
            "chunk_index": i + 1,
            "total_chunks": total,
            "focus_area": row.get("focus_area", ""),
            "source": row.get("source", "")
        })

    question_counter += 1

# Create DataFrame
df_chunks = pd.DataFrame(chunked_rows)

# Cleanup
df_chunks = df_chunks.dropna(subset=["answer_chunk", "question_chunk"])
df_chunks["focus_area"] = df_chunks["focus_area"].fillna("unknown")
df_chunks = df_chunks[df_chunks["answer_chunk"].str.strip() != ""]

# Save output
df_chunks.to_csv("preprocessed_chunksBB.csv", index=False)

# Print summary
print("Chunking completed.")
print("Sample:")
print(df_chunks.head())
