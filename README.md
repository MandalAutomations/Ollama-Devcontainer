# Ollama Dev Container Template

A ready-to-use development environment template for Python projects with integrated LLM capabilities via Ollama.

## Features

- Pre-configured VS Code Dev Container setup with Docker Compose
- Python 3.10 environment with automatic dependency installation
- Integrated Ollama for LLM inference
- Example code for interacting with Ollama models

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) installed
- [VS Code](https://code.visualstudio.com/) with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

## Getting Started

1. Click "Use this template" to create a new repository from this template
2. Clone your new repository
3. Open in VS Code
4. When prompted, click "Reopen in Container"
5. Wait for the container to build and initialize (this will pull required images and install dependencies)

## Environment Structure

- `.devcontainer/` - Dev Container configuration
- `src/` - Python source code modules
- `examples/` - Example scripts for embeddings, response generation, and image detection
- `requirements.txt` - Python dependencies

## Using Ollama

The template comes with a pre-configured Ollama service and a Python client for interacting with it.

### Available Models

By default, the template is configured to use `gemma3:1b`. You can use any model from the [Ollama Model Library](https://ollama.com/library).

### Example Usage

```python
# Import the Llama client
from src.llama import llama

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
MODEL = "llama3.2:1b" # Find available models here https://ollama.com/library

# Initialize with Ollama host and model
client = llama(OLLAMA_HOST, MODEL)

# Pull the model if not already available
client.check_and_pull_model()

# Generate a response
response = client.generate_response("What is the capital of France?")
```

## Customizing the Environment

### Adding Python Dependencies

Add any required packages to `requirements.txt` and they will be automatically installed when the container starts.

### Using Different Models

Change the model in the relevant example script (e.g., `examples/generate_response_example.py`) by modifying the model name. The template will automatically pull the model if it's not already available.

## Running the Example


## Running Examples

The `main.py` file has been removed. Example functionalities are now provided as separate Python scripts in the `examples/` folder:

- `embedding.py`: Example for generating embeddings
- `generate_response.py`: Example for generating responses
- `image_detection.py`: Example for image detection

To run an example, use:

```bash
python examples/embedding.py
python examples/generate_response.py
python examples/image_detection.py
```

Each script will initialize the specified Ollama model and perform its respective task.

## License

[MIT License](LICENSE)
