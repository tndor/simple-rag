# **Simple Local RAG (Retrieval-Augmented Generation)**

This project implements a local RAG system using **Python**, **LangChain**, **ChromaDB**, and **Ollama**. It allows you to chat with your own Markdown notes without sending data to the cloud.

## **Features**

* **Privacy-First**: Runs entirely locally using Ollama.  
* **Vector Database**: Uses ChromaDB for persistent storage of embeddings.  
* **Custom Knowledge**: Ingests .md files from a local directory.  
* **Lightweight**: Optimized for local hardware using efficient embedding models (nomic-embed-text) and small LLMs (e.g., Llama 3.2 1B).

## **Prerequisites**

1. **Python 3.10+** installed.  
2. [**Ollama**](https://ollama.com/) installed and running.

## **Setup & Installation**

### **1\. Clone or Download the Project**

Ensure your project structure looks like this:

    simple-rag/  
    ├── dataset/           \# Put your .md files here  
    │   ├── flameburst.md  
    │   └── ...  
    ├── dataset.py         \# Script to create the vector database  
    ├── rag.py             \# Script to chat with your data  
    ├── requirements.txt   \# Dependencies  
    └── README.md

### **2\. Install Python Dependencies**

Create a virtual environment and install the required libraries:

#### Create virtual environment  

    python3 \-m venv .venv

#### Activate it  

    source .venv/bin/activate  \# On Windows: .venv\\Scripts\\activate

#### Install libraries  

    pip install langchain-community langchain-chroma langchain-ollama ollama

### **3\. Pull Ollama Models**

You need to download the specific models used in the code. Run these commands in your terminal:

#### 1\. The Embedding Model (Critical for retrieval)  

    ollama pull nomic-embed-text

#### 2\. The Chat Model (The "Brain")  
#### You can use llama3.2, llama3.1, or the 1B version for speed

    ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF

**Note:** If you change the model names in the code, ensure you ollama pull the matching name.

## **Usage**

### **Step 1: Build the Database**

Whenever you add new .md files to the dataset/ folder, you must rebuild the database.

    python dataset.py

*Expected Output:* Database created at ./vector\_db

### **Step 2: Chat with Your Data**

Run the retrieval script to ask questions.

    python rag.py

*Enter your query when prompted. The system will search your local notes and generate an answer based **only** on the context found.*

## **Configuration**

You can adjust these variables in dataset.py and rag.py to customize performance:

* **EMBEDDING\_MODEL**: Defaults to 'nomic-embed-text'. Must match a model pulled in Ollama.  
* **chunk\_size**: (In dataset.py) How large the text snippets are (default 500).  
* **chunk\_overlap**: (In dataset.py) Overlap between snippets to preserve context (default 100).

## **Troubleshooting**

Q: The AI is hallucinating or not finding my new files.  
A: This is usually a "Zombie Database" issue.

1. Delete the ./vector\_db folder manually.  
2. Run python dataset.py again to force a fresh rebuild.  
3. Ensure your file extensions are lowercase .md (Linux is case-sensitive).

Q: "Model not found" error.  
A: Ensure the EMBEDDING\_MODEL string in your Python code exactly matches the output of ollama list in your terminal. Do not use HuggingFace URLs (e.g., hf.co/...) directly with Ollama.

## Reference

Original tutorial: https://huggingface.co/blog/ngxson/make-your-own-rag

Dataset: https://github.com/LostInBrittany/RAGmonsters