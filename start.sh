#!/bin/bash

# Wait for Ollama to wake up
echo "Waiting for Ollama..."
until curl -s "$OLLAMA_HOST/api/tags" > /dev/null; do sleep 2; done

# If grep fails (model not found), the command after || runs
curl -s "$OLLAMA_HOST/api/tags" | grep -q "nomic-embed-text" || \
  curl -X POST "$OLLAMA_HOST/api/pull" -d '{"name": "nomic-embed-text"}'

curl -s "$OLLAMA_HOST/api/tags" | grep -q "Llama-3.2-1B" || \
  curl -X POST "$OLLAMA_HOST/api/pull" -d '{"name": "hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF"}'

# Build Database if volume is empty
if [ -z "$(ls -A /app/vector_db)" ]; then
  echo "Building Vector DB..."
  python dataset.py
fi

# Start App
python app.py