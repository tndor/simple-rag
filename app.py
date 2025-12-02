import os
import ollama
from flask import Flask, render_template, request, jsonify
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

app = Flask(__name__)

# --- CONFIGURATION ---
DB_PATH = "./vector_db"
EMBEDDING_MODEL = "nomic-embed-text"
CHAT_MODEL = "hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF"
SYSTEM_PROMPT = """You are the RAGMonsters Wiki Copilot. 
Use the following context to answer the user's question about monsters.
If the answer is not in the context, say you don't know. 
IT IS VERY IMPORTANT THAT YOU ONLY USE THE PROVIDED CONTEXT TO ANSWER THE QUESTION.
Keep answers concise and formatted nicely (you can use Markdown).
"""

print(f"Connecting to Vector Database at {DB_PATH}...")
if not os.path.exists(DB_PATH):
    print(f"WARNING: Database path '{DB_PATH}' not found. Did you run dataset.py?")

vector_db = Chroma(
    persist_directory=DB_PATH,
    embedding_function=OllamaEmbeddings(model=EMBEDDING_MODEL)
)
print("Database connected.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Fetch top 3 relevant chunks
    results = vector_db.similarity_search_with_score(user_input, k=6)
    
    # Extract text from chunks
    context_text = "\n\n".join([doc.page_content for doc, _score in results])

    # 2. Augment Prompt
    full_prompt = f"Context:\n{context_text}\n\nQuestion: {user_input}"

    # 3. Generate Response via Ollama
    # We use stream=False here for a simpler HTTP response, 
    try:
        response = ollama.chat(
            model=CHAT_MODEL,
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': full_prompt}
            ]
        )
        ai_message = response['message']['content']
        
        return jsonify({
            "response": ai_message,
            "context_used": [doc.metadata.get('source', 'Unknown') for doc, _score in results]
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)