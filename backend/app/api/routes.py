from fastapi import APIRouter
from app.services.qdrant_ops import client, create_medical_collection, upload_qa_points
import pandas as pd
from qdrant_client.http.models import PointStruct
from app.services.embed import embed_text
from uuid import uuid5, NAMESPACE_DNS
from app.services.retrieval import retrieve_chunks
from app.services.generator import generate_answer

router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "pong"}
  
@router.get("/check-qdrant")
def check_qdrant():
    status = client.get_collections()
    return {"collections": status}

@router.get("/init-qdrant")
def init_qdrant():
    create_medical_collection()
    return {"status": "collection created"}

@router.post("/upload-sample")
def upload_sample_chunks(limit: int = None, offset: int = 0, batch_size: int = 100):
    df = pd.read_csv("dataset/preprocessed_chunksPMB.csv")

    if limit is not None:
        df = df[offset:offset + limit]
    else:
        df = df[offset:]

    points = []
    total = len(df)

    for idx, (_, row) in enumerate(df.iterrows(), start=1):
        question = row["question_chunk"]
        answer = row["answer_chunk"]
        text = f"Q: {question.strip()} A: {answer.strip()}"
        vector = embed_text(text)

        point = PointStruct(
            id=str(uuid5(NAMESPACE_DNS, row["chunk_id"])),
            vector=vector,
            payload={
                "question": question,
                "answer": answer,
                "focus_area": row["focus_area"],
                "source": row["source"],
                "type": "qa",
                "question_index": int(row["question_index"]),
                "chunk_index": int(row["chunk_index"]),
                "total_chunks": int(row["total_chunks"])
            }
        )
        points.append(point)

        # Upload in batches
        if len(points) == batch_size or idx == total:
            upload_qa_points(points)
            print(f"✅ Uploaded {offset + idx} rows so far...")
            points = []

    return {"status": "success", "uploaded": total}

@router.get("/search")
def semantic_search(query: str, limit: int = 5):
    results = retrieve_chunks(query, limit)
    return {
        "query": query,
        "results": [
            {
                "score":   r["score"],
                "question": r["question"],
                "answer":   r["answer"],
                "focus_area": r["focus_area"],
                "source": r["source"]
            }
            for r in results
        ]
    }

@router.get("/count-rows")
def count_uploaded_rows():
    result = client.count(collection_name="medical_chunks", exact=True)
    return {"total_uploaded": result.count}

@router.get("/uploaded-chunk-ids")
def get_uploaded_chunk_ids(limit: int = 10000):
    result = client.scroll(
        collection_name="medical_chunks",
        limit=limit,
        with_payload=False
    )
    return {
        "uploaded_ids": [point.id for point in result[0]],
        "count": len(result[0])
    }

@router.get("/generate-answer")
def get_generated_answer(query: str, top_k: int = 5):

    # 1) Retrieve semantic hits
    records = retrieve_chunks(query, top_k)

    # 2) Extract raw answer chunks from those hits
    raw_chunks = [r["answer"] for r in records]

    # 3) Take the top 3 for context
    context_chunks = raw_chunks[:3]

    # 4) Generate the final answer
    generated = generate_answer(query, context_chunks)

    return {
        "query": query,
        "generated_answer": generated,
        "context_used": context_chunks,
        "retrieval_scores": [r["score"] for r in records],
        "sources": [r["source"] for r in records]
    }
