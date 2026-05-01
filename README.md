# Ollama Dev Container Template

A ready-to-use development environment template for Python projects with integrated LLM capabilities via Ollama.

## Features

- Pre-configured VS Code Dev Container setup with Docker Compose
- Python 3.10 environment with automatic dependency installation
- Integrated Ollama server for local LLM inference
- Example scripts for embeddings, response generation, image classification, and GPU checks

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) installed
- [VS Code](https://code.visualstudio.com/) with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- (Optional) **GPU with CUDA or ROCm support** for GPU-accelerated inference
  - **NVIDIA GPUs**: [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) on the host system
  - **AMD GPUs**: ROCm-compatible AMD GPU with ROCm drivers on the host system
  - Docker must be configured to use the appropriate GPU runtime

## Getting started

1. Click **Use this template** to create a new repository from this template.
2. Clone your new repository.
3. Open it in VS Code.
4. When prompted, click **Reopen in Container**.
5. Wait for the container to build and initialize (this pulls images and installs dependencies).

## Environment structure

- `.devcontainer/` — Dev Container configuration and `docker-compose.yml`
- `src/` — Python source code modules (e.g. `src/llama.py`)
- `examples/` — Example scripts for embeddings, response generation, image classification, and GPU checks
- `requirements.txt` — Python dependencies
- `Modelfile` — Optional Ollama Modelfile for building custom models

## Using Ollama

### GPU acceleration

This template is configured to automatically use GPU acceleration (NVIDIA or AMD) if available. The `docker-compose.yml` includes GPU resource reservations that activate when:

**NVIDIA GPUs**
1. Your system has an NVIDIA GPU.
2. NVIDIA Container Toolkit is installed on the host.
3. Docker is configured to use the NVIDIA runtime.

**AMD GPUs**
1. Your system has a ROCm-compatible AMD GPU.
2. ROCm drivers are installed on the host.
3. Docker has access to `/dev/kfd` and `/dev/dri`.

If no GPU is available, Ollama falls back to CPU inference.

#### Verifying GPU usage

```bash
python examples/check_gpu.py
```

This script tests inference performance, displays a tokens/second metric, and reports whether GPU acceleration is active.

You can also check GPU status directly:

```bash
# NVIDIA — check GPU access from the Ollama container
docker exec ollama nvidia-smi

# AMD — check ROCm GPU status
docker exec ollama rocm-smi

# View Ollama logs (GPU usage is logged during model loading)
docker logs ollama
```

#### Installing NVIDIA Container Toolkit (Linux)

```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

After installation, rebuild the dev container.

#### Installing ROCm for AMD GPUs (Linux)

```bash
# Confirm GPU support: https://rocm.docs.amd.com/en/latest/release/gpu_os_support.html

# Ubuntu 22.04
wget https://repo.radeon.com/amdgpu-install/latest/ubuntu/jammy/amdgpu-install_latest_all.deb
sudo apt-get install ./amdgpu-install_latest_all.deb
sudo amdgpu-install --usecase=rocm --no-dkms

sudo usermod -a -G render,video $USER
sudo reboot
```

After installation, rebuild the dev container. **Note:** AMD GPU support requires ROCm 5.7 or later.

### Available models

The example scripts default to `tinyllama:latest`. You can use any model from the [Ollama Model Library](https://ollama.com/library) — just edit the `MODEL` constant in the script you're running.

### Example usage

```python
import os
from src.llama import llama

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
MODEL = "tinyllama:latest"  # See https://ollama.com/library

client = llama(OLLAMA_HOST, MODEL)

# Pull the model if not already cached
client.check_and_pull_model()

# Generate a response
response = client.generate_response("What is the capital of France?")
print(response)
```

## Customizing the environment

### Adding Python dependencies

Add packages to `requirements.txt`. They'll be installed automatically when the container starts.

### Using different models

Change the `MODEL` value at the top of the relevant script in `examples/`. The first run will pull the model if it isn't already cached.

## Running the examples

Examples live in the `examples/` folder:

- `check_gpu.py` — Check GPU availability and inference performance.
- `text_embedding.py` — Generate embeddings.
- `text_generate_response.py` — Generate a response (interactive or single-prompt).
- `image_classification.py` — Image classification with a vision model.

Run any of them with:

```bash
python examples/check_gpu.py
python examples/text_embedding.py
python examples/text_generate_response.py
python examples/image_classification.py
```

## License

[MIT License](LICENSE)
