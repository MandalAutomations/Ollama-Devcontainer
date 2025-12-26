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
- (Optional) **GPU with CUDA or ROCm support** for GPU-accelerated inference
  - **NVIDIA GPUs**: [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) must be installed on the host system
  - **AMD GPUs**: ROCm-compatible AMD GPU with ROCm drivers installed on the host system
  - Docker must be configured to use the appropriate GPU runtime

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

### GPU Acceleration

This template is configured to automatically use GPU acceleration (NVIDIA or AMD) if available. The docker-compose.yml file includes GPU resource reservations that will enable GPU support when:

**For NVIDIA GPUs:**
1. Your system has an NVIDIA GPU
2. NVIDIA Container Toolkit is installed on the host
3. Docker is configured to use the NVIDIA runtime

**For AMD GPUs:**
1. Your system has a ROCm-compatible AMD GPU
2. ROCm drivers are installed on the host
3. Docker has access to `/dev/kfd` and `/dev/dri` devices

If no GPU is available, Ollama will automatically fall back to CPU inference.

#### Verifying GPU Usage

To check if your setup is using GPU acceleration, run:

```bash
python examples/check_gpu.py
```

This script will:
- Test inference performance
- Display tokens/second metric (GPU typically >50 tokens/sec, CPU typically <20 tokens/sec)
- Provide guidance on whether GPU acceleration is active

You can also check GPU status directly:

```bash
# For NVIDIA GPUs - Check if GPU is accessible to the Ollama container
docker exec ollama nvidia-smi

# For AMD GPUs - Check ROCm GPU status
docker exec ollama rocm-smi

# View Ollama logs (GPU usage is logged during model loading)
docker logs ollama
```

#### Installing NVIDIA Container Toolkit (Linux)

If you have an NVIDIA GPU but GPU acceleration isn't working:

```bash
# Add the NVIDIA Container Toolkit repository
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Install the toolkit
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Restart Docker
sudo systemctl restart docker
```

After installation, rebuild the dev container for changes to take effect.

#### Installing ROCm for AMD GPUs (Linux)

If you have an AMD GPU but GPU acceleration isn't working:

```bash
# Check if your AMD GPU is supported
# Visit: https://rocm.docs.amd.com/en/latest/release/gpu_os_support.html

# Install ROCm (Ubuntu/Debian)
# For Ubuntu 22.04
wget https://repo.radeon.com/amdgpu-install/latest/ubuntu/jammy/amdgpu-install_latest_all.deb
sudo apt-get install ./amdgpu-install_latest_all.deb

# Install ROCm components
sudo amdgpu-install --usecase=rocm --no-dkms

# Add user to render and video groups
sudo usermod -a -G render,video $USER

# Restart system for changes to take effect
sudo reboot
```

After installation, rebuild the dev container for changes to take effect.

**Note**: AMD GPU support requires ROCm 5.7 or later. Check the [official ROCm documentation](https://rocm.docs.amd.com/) for your specific GPU model and OS.

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

- `text_embedding.py`: Example for generating embeddings
- `text_generate_response.py`: Example for generating responses
- `image_classification.py`: Example for image detection
- `check_gpu.py`: Check GPU availability and performance

To run an example, use:

```bash
python examples/check_gpu.py            # Check GPU status and performance
python examples/text_embedding.py
python examples/text_generate_response.py
python examples/image_classification.py
```

Each script will initialize the specified Ollama model and perform its respective task.

## License

[MIT License](LICENSE)
