import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.llama import llama

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
EMBEDDING_MODEL = "granite-embedding:30m" # Find available models here https://ollama.com/library

if __name__ == "__main__":
    llama = llama(OLLAMA_HOST)
    all_models = llama.get_all_models()
    
    for model in all_models:
        print(model)
