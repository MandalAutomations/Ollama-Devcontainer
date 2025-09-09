import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.llama import llama

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
MODEL = "gemma3:1b" # Find available models here https://ollama.com/library

# Example texts to classify
texts = [
    "The stock market crashed yesterday.",
    "The patient was diagnosed with diabetes.",
    "The new movie was a box office hit.",
    "The weather forecast predicts rain tomorrow.",
    "The football team won the championship."
]

categories = ["Finance", "Health", "Entertainment", "Weather", "Sports"]

def classify_text(llama_client, text):
    prompt = f"Classify the following text into one of these categories: {', '.join(categories)}.\nText: {text}\nCategory:"
    response = llama_client.generate_response(prompt)
    return response.strip() if response else "Unknown"

if __name__ == "__main__":
    llama_client = llama(OLLAMA_HOST, model=MODEL)
    for text in texts:
        category = classify_text(llama_client, text)
        print(f"Text: {text}\nPredicted Category: {category}\n")