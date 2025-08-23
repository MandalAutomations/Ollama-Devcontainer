import os
import sys
from src.llama import llama

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
MODEL = "llama3.2:1b" # Find available models here https://ollama.com/library

if __name__ == "__main__":
    llama = llama(OLLAMA_HOST, MODEL)

    text = "Hello World"
    embedding = llama.create_embedding(text)

    if embedding:
        print("Embedding created successfully.")
        print(embedding)
    else:
        print("Failed to create embedding.")
