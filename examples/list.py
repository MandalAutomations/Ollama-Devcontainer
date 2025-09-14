import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.llama import llama

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
EMBEDDING_MODEL = "granite-embedding:30m" # Find available models here https://ollama.com/library

if __name__ == "__main__":
    llama = llama(OLLAMA_HOST)
    llama.remove_model("tinyllama:1.1b")
    print(llama.get_all_models())
    
    
    # llama.remove_all_models()
    
    # print(llama.get_all_models())
