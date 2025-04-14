from chunker import chunk_text
from clean import clean_text
import pandas as pd
import nltk
nltk.download("punkt")


# load the dataset using pandas and inspect key columns
df = pd.read_csv("medquad.csv")

# rename for convenience if needed
df = df.rename(columns={
    "Question": "question",
    "Answer": "answer",
    "Focus": "focus_area",
    "Type": "question_type",
    "URL": "source"
})

# drop null or empty rows
df.dropna(subset=["question", "answer"], inplace=True)
df = df[df["answer"].str.strip().astype(bool)]

# clean text -- remove HTML, newlines, extra whitespace, convert to lowercase
df["question"] = df["question"].apply(clean_text)
df["answer"] = df["answer"].apply(clean_text)

# filter out very short answers (<10 words) -- filter out answers that lack enough context for RAG retrieval
df = df[df["answer"].apply(lambda x: len(x.split()) >= 10)]

# create chunked dataframe --store chunks in a new DataFrame
chunked_rows = []

for _, row in df.iterrows():
    answer_chunks = chunk_text(row["answer"])
    for chunk in answer_chunks:
        chunked_rows.append({
            "question": row["question"],
            "answer_chunk": chunk,
            "focus_area": row.get("focus_area", ""),
            "source": row.get("source", "")
        })

df_chunks = pd.DataFrame(chunked_rows)

# clean up edge cases
df_chunks = df_chunks.dropna(subset=["answer_chunk"])
df_chunks["focus_area"] = df_chunks["focus_area"].fillna("unknown")

# save final output
df_chunks.to_csv("preprocessed_chunks.csv", index=False)

# basic stats
print("Focus Area Distribution:")
print(df_chunks["focus_area"].value_counts())
