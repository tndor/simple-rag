RAGMonsters Wiki Copilot (Simple Local RAG)
===========================================

This project implements a local RAG system using **Python**, **Flask**, **LangChain**, **ChromaDB**, and **Ollama**. It allows you to chat with your own Markdown notes via a dark-themed web interface without sending data to the cloud.

Features
--------

-   **Privacy-First**: Runs entirely locally using Ollama.

-   **Web Interface**: A clean, dark-themed chat UI ("RAGMonsters Wiki Copilot").

-   **Vector Database**: Uses ChromaDB for persistent storage of embeddings.

-   **Custom Knowledge**: Ingests `.md` files from a local directory.

-   **Lightweight**: Optimized for local hardware using efficient embedding models (`nomic-embed-text`) and small LLMs (`Llama 3.2 1B`).

Prerequisites
-------------

1.  **Python 3.10+** installed.

2.  [**Ollama**](https://ollama.com/ "null") installed and running.

Setup & Installation
--------------------

### 1\. Clone or Download the Project

Ensure your project structure looks like this:

```
simple-rag/
├── dataset/           # Put your .md files here
│   ├── flameburst.md
│   └── ...
├── templates/         # HTML Frontend
│   └── index.html
├── app.py             # Flask Web Server
├── dataset.py         # Script to create the vector database
├── requirements.txt   # Dependencies
└── README.md

```

### 2\. Install Python Dependencies

Create a virtual environment and install the required libraries:

#### Create virtual environment

```
python3 -m venv .venv

```

#### Activate it

```
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

```

#### Install libraries

```
pip install flask langchain-community langchain-chroma langchain-ollama ollama

```

### 3\. Pull Ollama Models

You need to download the specific models used in the code. Run these commands in your terminal:

#### 1\. The Embedding Model (Critical for retrieval)

```
ollama pull nomic-embed-text

```

#### 2\. The Chat Model (The "Brain")

```
ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF

```

> **Note:** If you change the model names in `app.py` or `dataset.py`, ensure you `ollama pull` the matching name.

Usage
-----

### Step 1: Build the Database

Whenever you add new `.md` files to the `dataset/` folder, you must rebuild the database.

```
python dataset.py

```

*Expected Output:* `Database created at ./vector_db`

### Step 2: Run the App

Start the Flask web server.

```
python app.py

```

Open your web browser and go to: **`http://localhost:5000`**

Configuration
-------------

You can adjust these variables in `dataset.py` and `app.py` to customize performance:

-   **`EMBEDDING_MODEL`**: Defaults to `'nomic-embed-text'`. Must match a model pulled in Ollama.

-   **`chunk_size`**: (In `dataset.py`) How large the text snippets are (default `500`).

-   **`chunk_overlap`**: (In `dataset.py`) Overlap between snippets to preserve context (default `100`).

Troubleshooting
---------------

**Q: The AI is hallucinating or not finding my new files.** **A:** This is usually a "Zombie Database" issue.

1.  Delete the `./vector_db` folder manually.

2.  Run `python dataset.py` again to force a fresh rebuild.

3.  Ensure your file extensions are lowercase `.md` (Linux is case-sensitive).

**Q: "Model not found" error.** **A:** Ensure the `EMBEDDING_MODEL` string in your Python code exactly matches the output of `ollama list` in your terminal. Do not use HuggingFace URLs (e.g., `hf.co/...`) directly with Ollama unless you have pulled them using that exact tag.

Reference
---------

Original tutorial: https://huggingface.co/blog/ngxson/make-your-own-rag

Dataset: https://github.com/LostInBrittany/RAGmonsters