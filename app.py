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

def question_filtering(question):
    FILTERING_PROMT = """You are a router. Return a JSON object with one key 'category'.
    
    Definitions:
    - "SPECIFIC": Questions about one specific monster, or a specific attribute (biome, weight, weakness) of a single entity.
    - "BROAD": Questions asking for lists, aggregations, summaries of multiple monsters, or general knowledge.

    Examples:
    User: "List all monsters in RAGMonsters."
    Assistant: { "category": "BROAD" }

    User: "What are the weaknesses of Flameburst?"
    Assistant: { "category": "SPECIFIC" }

    User: "In what biome do Flamebursts live?"
    Assistant: { "category": "SPECIFIC" }

    User: "Show me all rare monsters."
    Assistant: { "category": "BROAD" }

    User: "How heavy is a Psyforge?"
    Assistant: { "category": "SPECIFIC" }
    
    Classify the following question:
    """
    
    try:
        # Temperature 0: Forces the model to pick the most likely token (deterministic)
        response = ollama.chat(
            model=CHAT_MODEL,
            messages=[
                {'role': 'system', 'content': FILTERING_PROMT},
                {'role': 'user', 'content': question}
            ],
            format='json',
            options={
                "temperature": 0,
                "seed": 42
            }
        )

        import json
        answer_json = json.loads(response['message']['content'])
        category = answer_json.get('category', 'SPECIFIC').upper()
        
        if category not in ['SPECIFIC', 'BROAD']:
            return 'SPECIFIC' # Fallback
            
        return category

    except Exception as e:
        print(f"Error during question filtering: {e}")
        category = "SPECIFIC"

    return category

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Retrieve Relevant Context
    filtering_category = question_filtering(user_input)
    print(f"Question categorized as: {filtering_category}")

    if filtering_category == "BROAD":
        results = vector_db.similarity_search_with_score(user_input, k=20)
    elif filtering_category == "SPECIFIC":
        results = vector_db.similarity_search_with_score(user_input, k=3)
    
    # Extract text from chunks
    context_text = "\n\n".join([doc.page_content for doc, _score in results])

    # Debug Context
    print(f"Context Retrieved:\n{context_text}\n--- End of Context ---\n")

    # Augment Prompt
    full_prompt = f"Context:\n{context_text}\n\nQuestion: {user_input}"

    # Generate Response via Ollama
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