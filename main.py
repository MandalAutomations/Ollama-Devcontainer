import os
from src.llama import llama

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
MODEL = "llama3.2:1b" # Find available models here https://ollama.com/library

if __name__ == "__main__":
    llama = llama(OLLAMA_HOST, MODEL)
    llama.check_and_pull_model()

    while True:
        prompt = input("Enter your prompt: ")
        if prompt.lower() in ["exit", "quit"]:
            break
        response = llama.generate_response(prompt)
        print(response if response else "No response generated.")