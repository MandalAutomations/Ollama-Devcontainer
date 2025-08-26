# pip install requests pillow
import requests, base64
from io import BytesIO
from PIL import Image
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.llama import llama

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
    r.raise_for_status()
    return r.json().get("response", "")

if __name__ == "__main__":
    print(vision_describe("img/image.png", model="llava"))  # or "qwen2.5-vl"
