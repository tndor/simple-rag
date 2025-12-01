# Simple RAG Project

This project is a minimal implementation of Retrieval-Augmented
Generation (RAG), following the Hugging Face tutorial "Make Your Own
RAG". It focuses on understanding the fundamentals of RAG rather than
building a production system.

## Project Purpose

The goal of this project is to understand the core mechanics behind RAG:

1.  How raw text is converted into embeddings (numerical vectors).
2.  How the system calculates similarity scores to retrieve the most
    relevant chunks.
3.  How the retrieved chunks are passed to an LLM to improve answers.

This project emphasizes these foundations rather than tooling,
frameworks, or scaling.

## How RAG Works (In This Project)

1.  Documents are split into chunks.
2.  Each chunk is converted into a vector using an embedding model.
3.  At query time:
    -   The user question is embedded.
    -   Cosine similarity is computed between the query vector and all
        chunk vectors.
    -   The top-k most similar chunks are selected.
4.  These retrieved chunks are provided as context for the language
    model to generate an answer.

Understanding embeddings and similarity calculations is the main purpose
of this project.

## Setup

Install dependencies:

    pip install ollama

Pull models locally (example models used in the tutorial):

    ollama pull hf.co/CompendiumLabs/bge-base-en-v1.5-gguf
    ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF

## Running the Project

Start the RAG chatbot:

    python rag.py

## Key Learning Takeaways

-   Embeddings represent text in a way that allows numerical comparison.
-   Similarity search (cosine similarity) determines which pieces of
    text matter.
-   RAG improves accuracy by grounding responses in retrieved data.
-   The retrieval step is vector math; understanding it is essential
    before using advanced libraries.

## Reference

Original tutorial: https://huggingface.co/blog/ngxson/make-your-own-rag
