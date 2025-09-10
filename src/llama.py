import requests, base64
import os
import json
from PIL import Image
from io import BytesIO
import re

class llama: 
    def __init__(self, host, model=None, embedding_model=None): 
        self.model = model
        self.embedding_model = embedding_model
        self.host = host
        if embedding_model is None:
            self.embedding_model = model
            
        if model is not None:
            self.check_and_pull_model(self.model)
        if embedding_model is not None and embedding_model != model:
            self.check_and_pull_model(self.embedding_model)

    def get_all_models(self):
        """ Get a list of all models available in Ollama"""
        try:
            response = requests.get(f"{self.host}/api/tags")
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            tags_data = response.json()
            available_models = [model['name'] for model in tags_data['models']]
            return available_models

        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama: {e}")
            return []
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error parsing Ollama response: {e}")
            return []
        
    def check_and_pull_model(self, model=None):
        """ Check if a model is available in Ollama, if not pull it """
        try:
            available_models = self.get_all_models()

            if model in available_models:
                print(f"Model '{model}' is already available in Ollama.")
                return

            print(f"Model '{model}' not found. Pulling from Ollama...")
            data = json.dumps({"name": model})
            response = requests.post(f"{self.host}/api/pull", data=data, stream=True)
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')

            print(f"Model '{model}' pulled successfully.")

        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama: {e}")
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error parsing Ollama response: {e}")

    def remove_all_models(self):
        """ Remove all models from Ollama """
        try:
            available_models = self.get_all_models()

            for model_name in available_models:
                self.remove_model(model_name)

            print("All models removed successfully.")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Error removing all models: {e}")
            return False
        
    def remove_model(self, model_name):
        """ Remove a model from Ollama """
        try:
            response = requests.delete(f"{self.host}/api/delete", json={"name": model_name})
            response.raise_for_status()
            
            print(f"Model '{model_name}' removed successfully.")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Error removing model '{model_name}': {e}")
            return False

    def generate_response(self, prompt):
        """ Generate a response from the model """
        response = requests.post(
            f"{self.host}/api/generate",
            json={"model": self.model, "prompt": prompt},
            stream=True
        )

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None

        response_text = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                try:
                    response_json = json.loads(decoded_line)
                    response_text += response_json.get("response", "")
                    if response_json.get("done", False):
                        break
                except json.JSONDecodeError:
                    print(f"Error decoding JSON: {decoded_line}")

        return response_text

    def img_to_b64(self, path):
        img = Image.open(path).convert("RGB")
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=90)
        return base64.b64encode(buf.getvalue()).decode("utf-8")

    def vision_describe(self, path, prompt):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "images": [self.img_to_b64(path)]
        }
        r = requests.post(
            f"{self.host}/api/generate",
            json=payload,
            stream=True
        )
        r.status_code == 200 or print("Error:", r.text)
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

    def create_embedding(self, text: str):
        """ Create an embedding from the text using the embedding model """
        try:
            resp = requests.post(
                f"{self.host}/api/embeddings",
                json={"model": self.embedding_model, "prompt": text},
                timeout=60
            )
        except requests.RequestException as e:
            print(f"Network error creating embedding: {e}")
            return None

        if resp.status_code != 200:
            print(f"Error creating embedding: {resp.status_code} {resp.text}")
            return None

        try:
            data = resp.json()
        except json.JSONDecodeError:
            print(f"Invalid JSON in embedding response: {resp.text[:200]}")
            return None

        embedding = data.get("embedding")
        if not isinstance(embedding, list):
            print(f"Unexpected embedding payload: {data}")
            return None

        return embedding