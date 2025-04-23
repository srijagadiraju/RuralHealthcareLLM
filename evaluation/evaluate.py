"""
Compute Precision@k  and  semantic-groundedness for RAG outputs.

Groundedness = at least one sentence in the generated answer
               is semantically similar (cos ≥ 0.55) to one of the
               retrieved context chunks.
"""

import json, re, argparse, pathlib, numpy as np
from sentence_transformers import SentenceTransformer

# -------- config --------
RESP_FILE       = pathlib.Path("responses.json")
K               = 5           # top-k chunks to inspect
SIM_THRESHOLD   = 0.55        # cosine threshold for “supported”
MODEL_NAME      = "all-MiniLM-L6-v2"
# ------------------------

print("🔹 loading embedding model …")
emb_model = SentenceTransformer(MODEL_NAME)

def cos_sim(v1, v2):
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

def evaluate(resp_path=RESP_FILE, top_k=K):
    data = json.loads(pathlib.Path(resp_path).read_text())

    p_at_k, grounded_flags = [], []

    for d in data:
        if d.get("error"):          # skip failed API calls
            continue

        query     = d["query"].lower()
        answer    = d["generated_answer"]
        chunks    = d["context_used"][:top_k]

        # ---------- Precision@k ----------
        relevant = sum(any(tok in c.lower() for tok in query.split())
                       for c in chunks)
        p_at_k.append(relevant / max(1, len(chunks)))

        # ---------- Groundedness ----------
        # embed chunks once
        chunk_vecs = emb_model.encode(chunks, convert_to_numpy=True,
                                      show_progress_bar=False)
        # split answer into sentences (~heuristic)
        sentences  = [s.strip() for s in re.split(r"[.!?]\s+", answer) if s.strip()]
        sent_vecs  = emb_model.encode(sentences, convert_to_numpy=True,
                                      show_progress_bar=False) if sentences else []

        grounded = False
        for sv in sent_vecs:
            if any(cos_sim(sv, cv) >= SIM_THRESHOLD for cv in chunk_vecs):
                grounded = True
                break
        grounded_flags.append(int(grounded))

    # ------------- report -------------
    print("\n=== Evaluation ===")
    n = len(p_at_k)
    print(f"Queries evaluated : {n}")
    print(f"Precision@{top_k:<2}     : {sum(p_at_k)/n: .2f}")
    print(f"Groundedness Acc. : {sum(grounded_flags)/n: .2f}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="responses.json")
    ap.add_argument("--k",   type=int, default=K)
    args = ap.parse_args()
    evaluate(args.file, args.k)
