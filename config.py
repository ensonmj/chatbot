import os

whatapp_verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN")
whatapp_token = os.getenv("WHATSAPP_TOKEN")

model = os.getenv("RAG_MODEL", "qwen2:0.5b")
data_path = os.getenv("RAG_DATA_PATH", "./info.txt")

contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""

# qa_system_prompt = "You're an assistant who's good at {ability}"
qa_system_prompt = """You are an assistant for question-answering tasks. \
Use the following pieces of retrieved context to answer the question. \
If you don't know the answer, just say that you don't know. \
Use three sentences maximum and keep the answer concise.\

{context}"""