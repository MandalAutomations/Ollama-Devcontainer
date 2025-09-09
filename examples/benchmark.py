import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.llama import llama

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
MODEL = None #"llama3.2:1b" # Find available models here https://ollama.com/library
EMBEDDING_MODEL = "embeddinggemma:latest" # Find available models here https://ollama.com/library

# Example prompts for benchmarking
prompts = [
    "What is the capital of France?",
    "Explain the theory of relativity.",
    "Summarize the plot of Hamlet.",
    "Translate 'hello' to Spanish.",
    "List three uses for a paperclip."
]

def benchmark_generation(llama_client, prompts):
    times = []
    for prompt in prompts:
        start = time.time()
        _ = llama_client.generate_response(prompt)
        elapsed = time.time() - start
        times.append(elapsed)

    avg_time = sum(times) / len(times)
    print(f"Average generation time: {avg_time:.2f} seconds")

def benchmark_embedding(llama_client, prompts):
    times = []
    dim=0
    for prompt in prompts:
        start = time.time()
        embed = llama_client.create_embedding(prompt)
        elapsed = time.time() - start
        times.append(elapsed)
        dim = len(embed) if embed else 0

    avg_time = sum(times) / len(times)
    print(f"Average embedding time: {avg_time:.2f} seconds")
    print(f"Embedding dimension: {dim}")

if __name__ == "__main__":
    llama_client = llama(OLLAMA_HOST, model=MODEL, embedding_model=EMBEDDING_MODEL)
    if MODEL is not None:
        print("Benchmarking response generation for model:", MODEL)
        benchmark_generation(llama_client, prompts)
    if EMBEDDING_MODEL is not None:
        print("Benchmarking embedding creation for model:", EMBEDDING_MODEL)
        benchmark_embedding(llama_client, prompts)
