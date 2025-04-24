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

# import google.generativeai as genai
# from app.core.config import GEMINI_API_KEY

# # Set API key
# genai.configure(api_key=GEMINI_API_KEY)

# # Load model
# model = genai.GenerativeModel("gemini-1.5-flash")

# FALLBACK_RESPONSE = "I am not sure based on the current data. Please provide more information about your symptoms, and I will be happy to assist."


# def generate_answer(query: str, context_chunks: list) -> str:
#     context = "\n".join(context_chunks)
#     prompt = (
#         "You are a helpful medical assistant. "
#         "Answer the following question using only the provided context below. "
#         "Do not make anything up. If the context does not contain enough information, respond exactly with:\n"
#         f"\"{FALLBACK_RESPONSE}\"\n\n"
#         f"Context:\n{context}\n\n"
#         f"Question:\n{query}\n\n"
#         "Answer:"
#     )

#     response = model.generate_content(prompt)
#     text = response.text.strip()

#     # # Force consistency even if model adds something after the fallback
#     # if FALLBACK_RESPONSE.lower() in text.lower():
#     #     return FALLBACK_RESPONSE

#     return text
