from chunker import chunk_text
from clean import clean_text
import pandas as pd
import nltk
from transformers import AutoTokenizer

# download NLTK tokenizer
nltk.download("punkt")

# initialize PubMedBERT tokenizer
# tokenizer = AutoTokenizer.from_pretrained(
#     "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract"
# )

# initialize BioBert
tokenizer = AutoTokenizer.from_pretrained(
    "dmis-lab/biobert-base-cased-v1.1")


# load dataset
df = pd.read_csv("medquad.csv")

# rename columns for consistency
df = df.rename(columns={
    "Question": "question",
    "Answer": "answer",
    "Focus": "focus_area",
    "Type": "question_type",
    "URL": "source"
})

# drop nulls
df.dropna(subset=["question", "answer"], inplace=True)

# clean question/answer text
df["question"] = df["question"].apply(clean_text)
df["answer"] = df["answer"].apply(clean_text)

# Remove rows where answer has 0 tokens
df = df[df["answer"].apply(lambda x: len(
    tokenizer.encode(x, add_special_tokens=False)) > 0)]

# initialize storage
chunked_rows = []
question_counter = 1  # 1-based index for each Q&A

# process each row
for idx, row in df.iterrows():
    question_text = row["question"]
    answer_text = row["answer"]

    # chunk question and answer
    # question_chunks = chunk_text(question_text, tokenizer=tokenizer)
    # answer_chunks = chunk_text(answer_text, tokenizer=tokenizer)
    question_chunks = chunk_text(question_text)
    answer_chunks = chunk_text(answer_text)

    # add question chunk(s) as separate rows for fallback search
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

    # add answer chunks (with filter to remove chunks > 400 tokens)
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

# create DataFrame
df_chunks = pd.DataFrame(chunked_rows)

# cleanup
df_chunks = df_chunks.dropna(subset=["answer_chunk", "question_chunk"])
df_chunks["focus_area"] = df_chunks["focus_area"].fillna("unknown")
df_chunks = df_chunks[df_chunks["answer_chunk"].str.strip() != ""]

# save output
# df_chunks.to_csv("preprocessed_chunksPMB.csv", index=False)
df_chunks.to_csv("preprocessed_chunksBB.csv", index=False)

# print summary
print("Chunking completed.")
print("Sample:")
print(df_chunks.head())
