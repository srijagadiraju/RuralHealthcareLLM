import google.generativeai as genai
from app.core.config import GEMINI_API_KEY

# Set API key
genai.configure(api_key=GEMINI_API_KEY)

# Load model
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_answer(query: str, context_chunks: list) -> str:
    context = "\n".join(context_chunks)
    prompt = (
        "You are a helpful medical assistant. "
        "Answer the following question using only the provided context. "
        "Ignore boilerplate and irrelevant information. "
        "If the context does not contain enough information, say that you are not sure based on the current data.\n\n"
        f"Context:\n{context}\n\n"
        f"Question:\n{query}\n\n"
        "Answer:"
    )

    response = model.generate_content(prompt)
    return response.text.strip()
