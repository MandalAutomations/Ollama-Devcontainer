import requests
import os
import json


class llama: 
    def __init__(self, host, model): 
        self.model = model
        self.host = host

    def check_and_pull_model(self):

        try:
            response = requests.get(f"{self.host}/api/tags")
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            tags_data = response.json()
            available_models = [model['name'] for model in tags_data['models']]

            if self.model in available_models:
                print(f"Model '{self.model}' is already available in Ollama.")
                return

            print(f"Model '{self.model}' not found. Pulling from Ollama...")
            data = json.dumps({"name": self.model})
            response = requests.post(f"{self.host}/api/pull", data=data, stream=True)
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')

            print(f"Model '{self.model}' pulled successfully.")

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

        print(response_text)
        return response_text
