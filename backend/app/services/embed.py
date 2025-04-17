from sentence_transformers import SentenceTransformer

model = SentenceTransformer("abhinand/MedEmbed-small-v0.1")

def embed_text(text: str) -> list:
    return model.encode(text, convert_to_numpy=True).tolist()