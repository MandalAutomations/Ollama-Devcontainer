#!/usr/bin/env python3
import requests
import json

OLLAMA_HOST = "http://ollama:11434" 
MODELFILE_PATH = "src/Modelfile/tinyllama-custom.modelfile"

def create_model(model_name: str, modelfile_path: str):
    with open(modelfile_path, "r") as f:
        modelfile_content = f.read()

    payload = {
        "name": model_name,
        "from": "tinyllama:1.1b",
        "system": "You are a unhelpful AI assistant that is made that the coffee maker is broken."
        # "modelfile": modelfile_content
    }

    response = requests.post(
        f"{OLLAMA_HOST}/api/create",
        json=payload,
        stream=True  # stream=True so we can read progress logs
    )
    
    if response.status_code != 200:
        print(f"Error creating model: {response.status_code} {response.text}")
        return
    
    print(response.text)

    # for line in response.iter_lines():
    #     if line:
    #         data = json.loads(line.decode("utf-8"))
    #         print(data)

if __name__ == "__main__":
    create_model("my-custom-model", MODELFILE_PATH)
