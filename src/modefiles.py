#!/usr/bin/env python3
import requests
import json
import os

OLLAMA_HOST = "http://ollama:11434" 
MODELFILE_PATH = "./Modelfile/tinyllama-custom-02.modelfile"

def fetch_modelfile(origin: str, dest: str):
    os.makedirs("./Modelfile", exist_ok=True)
    dest_path = f"./Modelfile/{dest}.modelfile"

    payload = {
        "name": origin,
        "modelfile": True
    }

    response = requests.post(f"{OLLAMA_HOST}/api/show", json=payload)
    if response.status_code != 200:
        print(f"Error fetching modelfile: {response.status_code} {response.text}")
        return

    data = response.json()
    modelfile_content = data.get("modelfile")
    if not modelfile_content:
        print("No modelfile returned in response.")
        return

    with open(dest_path, "w") as f:
        f.write(modelfile_content)

    print(f"Modelfile saved to {dest_path}")
    
        
def create_model(model_name: str, modelfile_path: str):
    with open(modelfile_path, "r") as f:
        modelfile_content = f.read()

    payload = {
        "name": model_name,
        # "from": "tinyllama:1.1b",
        # "system": "You are a unhelpful AI assistant that is made that the coffee maker is broken."
        "modelfile": modelfile_content
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
    # fetch_modelfile("tinyllama:1.1b", "tinyllama-custom-02")
    create_model("my-custom-model", MODELFILE_PATH)
