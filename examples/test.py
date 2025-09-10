import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.llama import llama

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
EMBEDDING_MODEL = "granite-embedding:30m"  # Find available models here https://ollama.com
llama_client = llama(OLLAMA_HOST, EMBEDDING_MODEL)

if __name__ == "__main__":
   all = llama_client.get_available_models()
   print("All models:", all)