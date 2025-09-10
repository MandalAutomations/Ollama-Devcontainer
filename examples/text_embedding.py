import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.llama import llama

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
EMBEDDING_MODEL = "granite-embedding:30m" # Find available models here https://ollama.com/library

if __name__ == "__main__":
    llama = llama(OLLAMA_HOST, embedding_model=EMBEDDING_MODEL)

    text = "Hello World"
    embedding = llama.create_embedding(text)

    if embedding:
        print("Embedding created successfully.")
        print(embedding[0:5])  # Print first 5 dimensions of the embedding
    else:
        print("Failed to create embedding.")
    
