import ollama

EMBEDDING_MODEL = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'

VECTOR_DB = []

# Load dataset from a text file
dataset = []
with open("cat-facts.txt", "r") as file:
    dataset = file.readlines()
    print(f"Loaded {len(dataset)} entries.")

# Function to add a chunk to the vector database
def add_chunk_to_database(chunk):
    embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)['embeddings'][0]
    VECTOR_DB.append((chunk, embedding))

# Populate the vector database
for i, chunk in enumerate(dataset):
    add_chunk_to_database(chunk)
    print(f"Added chunk {i+1}/{len(dataset)} to vector database.")

