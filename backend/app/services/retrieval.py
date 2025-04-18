from app.services.embed import embed_text
from app.services.qdrant_ops import client

def retrieve_chunks(query: str, top_k: int = 5):
    """
    Returns a list of dicts with keys:
      - score
      - question
      - answer
      - focus_area
      - ...any other payload fields
    """
    vec = embed_text(f"Q: {query.strip()} A:")
    hits = client.search(
        collection_name="medical_chunks",
        query_vector=vec,
        limit=top_k,
        with_payload=True
    )
    records = []
    for hit in hits:
        rec = {
            "score": hit.score,
            **hit.payload    # this spreads question, answer, focus_area, etc.
        }
        records.append(rec)
    return records
