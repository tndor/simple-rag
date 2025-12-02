import ollama

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

EMBEDDING_MODEL = 'nomic-embed-text'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'

VECTOR_DB = Chroma(
    embedding_function=OllamaEmbeddings(model=EMBEDDING_MODEL),
    persist_directory="./vector_db"
)

# Example retrieval
input_query = input("Ask me a question: ")
results = VECTOR_DB.similarity_search_with_score(input_query)

# Construct the prompt for the language model
instruction_prompt = f'''You are a helpful chatbot.
Use only the following pieces of context to answer the question. The information
given will be about monsters called RAGMonsters. Don't make up any new information:
{'\n'.join([f' - {chunk.page_content}' for chunk, similarity in results])}
'''
"""
UNCOMMENT FOR CHUNK DEBUGGING

print("\nDEBUG -- Retrieved Chunks:")
for chunck, similarity in results:
    print(f"Similarity: {similarity:.4f} | Content: {chunck.page_content}...")
"""

# Stream the response from the language model
stream = ollama.chat(
  model=LANGUAGE_MODEL,
  messages=[
    {'role': 'system', 'content': instruction_prompt},
    {'role': 'user', 'content': input_query},
  ],
  stream=True,
)

# print the response from the chatbot in real-time
print('Chatbot response:')
for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)
