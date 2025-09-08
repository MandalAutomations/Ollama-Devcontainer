import requests
import os
import json

class llama: 
    def __init__(self, host, model=None, emdedding_model=None): 
        self.model = model
        self.emdedding_model = emdedding_model
        self.host = host
        if emdedding_model is None:
            self.emdedding_model = model
            
        if model is not None:
            self.check_and_pull_model(self.model)
        if emdedding_model is not None and emdedding_model != model:
            self.check_and_pull_model(self.emdedding_model)

    def check_and_pull_model(self, model=None):

        try:
            response = requests.get(f"{self.host}/api/tags")
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            tags_data = response.json()
            available_models = [model['name'] for model in tags_data['models']]

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


    def generate_response(self, prompt):
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

    def create_embedding(self, text: str):

        try:
            resp = requests.post(
                f"{self.host}/api/embeddings",
                json={"model": self.emdedding_model, "prompt": text},
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