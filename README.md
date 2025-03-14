# Dev-Container-Compose

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
- `main.py` - Example script for Ollama interaction
- `requirements.txt` - Python dependencies

## Using Ollama

The template comes with a pre-configured Ollama service and a Python client for interacting with it.

### Available Models

By default, the template is configured to use `gemma3:1b`. You can use any model from the [Ollama Model Library](https://ollama.com/library).

### Example Usage

```python
# Import the Llama client
from src.llama import llama

# Initialize with Ollama host and model
client = llama("http://ollama:11434", "gemma3:1b")

# Pull the model if not already available
client.check_and_pull_model()

# Generate a response
response = client.generate_response("What is the capital of France?")
```

## Customizing the Environment

### Adding Python Dependencies

Add any required packages to `requirements.txt` and they will be automatically installed when the container starts.

### Using Different Models

Change the model in `main.py` by modifying the `MODEL` constant. The template will automatically pull the model if it's not already available.

## Running the Example

To run the example script:

```bash
python main.py
```

This will initialize the specified Ollama model and generate a response to the prompt defined in `main.py`.

## License

[MIT License](LICENSE)
