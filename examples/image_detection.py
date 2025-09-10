import requests, base64
from io import BytesIO
from PIL import Image
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.llama import llama
import json

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
MODEL = "moondream:latest"
llama_client = llama(OLLAMA_HOST, MODEL)

if __name__ == "__main__":
    image="img/image.png"
    description = llama_client.vision_describe(image)
    print("Description:", description)