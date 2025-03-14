import requests
import os
import json

# OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
OLLAMA_HOST="http://ollama:11434"
MODEL = "llama3.2:1b"  # Change this to the model you want to use

def check_and_pull_model(ollama_host, model_name):

    try:
        # Get the list of available models from Ollama
        response = requests.get(f"{ollama_host}/api/tags")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        tags_data = response.json()
        available_models = [model['name'] for model in tags_data['models']]

        # Check if the model is in the list
        if model_name in available_models:
            print(f"Model '{model_name}' is already available in Ollama.")
            return

        # If the model is not available, pull it
        print(f"Model '{model_name}' not found. Pulling from Ollama...")
        data = json.dumps({"name": model_name})
        response = requests.post(f"{ollama_host}/api/pull", data=data, stream=True)
        response.raise_for_status()

        # Print the stream
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                print(decoded_line)

        print(f"Model '{model_name}' pulled successfully.")

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Ollama: {e}")
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing Ollama response: {e}")


def generate_response(prompt):
    response = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json={"model": MODEL, "prompt": prompt}
    )

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    response_data = response.text
    print(response_data)

    return response.text

def test():
    response = requests.get(f"{OLLAMA_HOST}")
    print(response.status_code)

if __name__ == "__main__":
    # check_and_pull_model(OLLAMA_HOST, MODEL)
    # test()
    prompt = "Hello, can you read this?"
    result = generate_response(prompt)
    # print(result)


# curl POST http://ollama:11434/v1/pull -d '{"name": "llama2"}'