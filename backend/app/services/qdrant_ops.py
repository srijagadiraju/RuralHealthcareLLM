from qdrant_client import QdrantClient
from app.core.config import QDRANT_URL, QDRANT_API_KEY

from qdrant_client.http.models import VectorParams, Distance

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

def create_medical_collection():
    # Step 1: Create/recreate the collection with 768-dim PubMedBERT vectors
    client.recreate_collection(
        collection_name="medical_chunks",
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

    # Step 2: Create indexes for fields you'll filter on
    client.create_payload_index(
        collection_name="medical_chunks",
        field_name="focus_area",
        field_schema="keyword"
    )

    client.create_payload_index(
        collection_name="medical_chunks",
        field_name="source",
        field_schema="keyword"
    )

    client.create_payload_index(
        collection_name="medical_chunks",
        field_name="type",
        field_schema="keyword"
    )

    client.create_payload_index(
        collection_name="medical_chunks",
        field_name="question_index",
        field_schema="integer"
    )

    print("✅ Qdrant collection 'medical_chunks' created with indexes.")

def upload_qa_points(points: list):
    client.upsert(collection_name="medical_chunks", points=points)