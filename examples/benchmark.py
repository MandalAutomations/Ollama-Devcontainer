import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.llama import llama

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
MODEL = None #"llama3.2:1b" # Find available models here https://ollama.com/library
EMBEDDING_MODEL = "embeddinggemma:latest" # Find available models here https://ollama.com/library

models = [
    # "llama3.2:1b",
    # "gemma3:270m",
    # "tinyllama:latest",
]

embedding_models = [
    "nomic-embed-text:v1.5",
    "nomic-embed-text:137m-v1.5-fp16",
    "granite-embedding:30m",
    "granite-embedding:278m",
    "snowflake-arctic-embed:22m",
    "mxbai-embed-large:latest",
    "tinyllama:latest"
]

# Example prompts for benchmarking
prompts = [
    "What is the capital of France?",
    "Explain the theory of relativity.",
    "Summarize the plot of Hamlet.",
    "Translate 'hello' to Spanish.",
    "List three uses for a paperclip.",
    "Describe the process of photosynthesis.",
    "Who wrote 'Pride and Prejudice'?",
    "What is the boiling point of water in Celsius?",
    "Write a haiku about the ocean.",
    "What are the main causes of climate change?",
    "Convert 100 USD to euros.",
    "Name the largest planet in our solar system.",
    "What is the Pythagorean theorem?",
    "Give a brief history of the Internet.",
    "What is the chemical symbol for gold?"
]

def print_to_csv(data, filename="data/benchmark_results.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'a') as f:
        f.write(f"{data}\n")

def benchmark_generation(llama_client, prompts):
    times = []
    for prompt in prompts:
        start = time.time()
        _ = llama_client.generate_response(prompt)
        elapsed = time.time() - start
        times.append(elapsed)

    avg_time = sum(times) / len(times)
    result=f"{llama_client.model},{avg_time:.2f}"
    print_to_csv(result)

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
    result=f"{llama_client.embedding_model},{avg_time:.2f},{dim}"
    print_to_csv(result)

if __name__ == "__main__":

    llama_client = llama(OLLAMA_HOST)
    print_to_csv("Model,avg_response_time(s),Dimensions")

    for model in models:
        llama_client = llama(OLLAMA_HOST, model=model)
        print("Benchmarking response generation for model:", model)
        benchmark_generation(llama_client, prompts)
        
    for embedding_model in embedding_models:
        llama_client = llama(OLLAMA_HOST, embedding_model=embedding_model)
        print("Benchmarking embedding creation for model:", llama_client.embedding_model)
        benchmark_embedding(llama_client, prompts)
