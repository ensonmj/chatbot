from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore

# from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


def get_retriever():
    # Load, chunk and index the contents of the blog to create a retriever.
    loader = TextLoader("info.txt")
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    vectorstore = InMemoryVectorStore.from_documents(
        documents=splits, embedding=OllamaEmbeddings(model="qwen2:0.5b")
    )
    # vectorstore = Chroma.from_documents(documents=splits, embedding=OllamaEmbeddings(model="qwen2:0.5b"))

    return vectorstore.as_retriever()
