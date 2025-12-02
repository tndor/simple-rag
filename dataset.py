import ollama

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

EMBEDDING_MODEL = 'nomic-embed-text'

DIRECTORY_PATH = "./dataset"
DB_PATH = "./vector_db"

def create_vector_database():
    # Load documents from the specified directory
    print("loading documents from directory...")

    loader = DirectoryLoader(
        DIRECTORY_PATH,
        glob="**/*.md",
        loader_cls=TextLoader
    )
    docs = loader.load()

    if not docs:
        print("No markdown files found.")
        return

    print(f"Loaded {len(docs)} documents.")

    for doc in docs:
        print(f"   Embedding file: {doc.metadata['source']}")

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # Characters per chunk
        chunk_overlap=50 # Overlap to maintain context between chunks
    )
    chunks = text_splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")


    # Create or load the vector database
    print("Creating or loading vector database...")
    embedding_model = OllamaEmbeddings(
        model=EMBEDDING_MODEL
    )

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=DB_PATH
    )

    print(f"Database created at {DB_PATH}.")

if __name__ == "__main__":
    create_vector_database()