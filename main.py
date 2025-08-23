import os
import sys
from src.llama import llama

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
MODEL = "llama3.2:1b" # Find available models here https://ollama.com/library

if __name__ == "__main__":
    llama = llama(OLLAMA_HOST, MODEL)
    llama.check_and_pull_model()

    prompt = sys.argv[1] if len(sys.argv) > 1 else None
    
    if prompt:
        response = llama.generate_response(prompt)
        print(response if response else "No response generated.")
    else:
        while True:
            prompt = input("Enter a prompt (or 'exit' to quit): ")
            if prompt.lower() == "exit":
                break
            response = llama.generate_response(prompt)
            print(response if response else "No response generated.")
