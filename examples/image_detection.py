# pip install requests pillow
import requests, base64
from io import BytesIO
from PIL import Image
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.llama import llama
import json

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
MODEL = "llava"
llama = llama(OLLAMA_HOST, MODEL)

def img_to_b64(path: str) -> str:
    img = Image.open(path).convert("RGB")
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def vision_describe(path: str, model: str = "llava") -> str:
    payload = {
        "model": model,
        "prompt": (
            "Describe this image briefly, then output strict JSON with objects:\n"
            '{ "objects": [ { "name": "<object>", "attributes": ["..."] } ] }'
        ),
        "images": [img_to_b64(path)]
    }
    r = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json=payload,
        stream=True
    )
    response_text = ""
    for line in r.iter_lines():
        if line:
            try:
                data = json.loads(line.decode("utf-8"))
                response_text += data.get("response", "")
                if data.get("done", False):
                    break
            except json.JSONDecodeError as e:
                print("Bad JSON line:", line, e)
    
    return response_text

if __name__ == "__main__":
    image="img/image.png"
    description = vision_describe(image, model="llava")
    print(description)
