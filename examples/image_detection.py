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
    prompt = """
        Describe this image briefly, then output strict JSON with objects.
        Close the Json and do not add. Return only the json and no other formatting. Dont add```json '...':
        { 'type': '', 'label': '', 'color': '', 'size': '', 'position': [] }
        Make sure the json is valid.
    """
    description = llama_client.vision_describe(image, prompt).strip()
    try:
        description = description.replace("'", '"')
        objects_list = json.loads(description)
        
        for obj in objects_list:
            print(f"Type: {obj['type']}, Label: {obj['label']}, Color: {obj['color']}, Size: {obj['size']}, Position: {obj['position']}")
            
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Raw description: {description}")

  