import os
from src.llama import llama

# Use localhost for CI/local testing, ollama for Docker containers
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL = "llama3.2:1b" # Find available models here https://ollama.com/library

if __name__ == "__main__":
    llama = llama(OLLAMA_HOST, MODEL)
    llama.check_and_pull_model()

    prompt = "What is the capital of France?"
    response = llama.generate_response(prompt)
    print(response if response else "No response generated.")

    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path and response:
        with open(summary_path, "a") as f:
            f.write(response)