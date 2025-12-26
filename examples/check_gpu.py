import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.llama import llama

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
MODEL = "tinyllama:latest"  # Use a small model for quick testing

# Performance thresholds for GPU detection (tokens per second)
GPU_THRESHOLD = 50  # Performance above this suggests GPU acceleration
CPU_THRESHOLD = 20  # Performance below this suggests CPU-only inference

if __name__ == "__main__":
    print("Checking GPU availability and performance...")
    print("=" * 60)
    
    # Initialize the llama client
    client = llama(OLLAMA_HOST, MODEL)
    
    # Check GPU status
    gpu_info = client.check_gpu_status()
    
    if gpu_info:
        print("\n✓ Successfully connected to Ollama")
        print(f"\nPerformance Metrics:")
        print(f"  • Model load duration: {gpu_info.get('load_duration', 'N/A')} ns")
        print(f"  • Prompt evaluation tokens: {gpu_info.get('prompt_eval_count', 'N/A')}")
        print(f"  • Prompt evaluation duration: {gpu_info.get('prompt_eval_duration', 'N/A')} ns")
        print(f"  • Response tokens: {gpu_info.get('eval_count', 'N/A')}")
        print(f"  • Response generation duration: {gpu_info.get('eval_duration', 'N/A')} ns")
        
        if gpu_info.get('tokens_per_second') is not None:
            print(f"  • Tokens per second: {gpu_info['tokens_per_second']}")
            print("\n" + "=" * 60)
            print("\nPerformance Notes:")
            print(f"  • GPU acceleration typically achieves >{GPU_THRESHOLD} tokens/second")
            print(f"  • CPU-only inference is typically <{CPU_THRESHOLD} tokens/second")
            print("  • Actual performance varies by model size and hardware")
            
            if gpu_info['tokens_per_second'] > GPU_THRESHOLD:
                print("\n✓ Performance indicates GPU acceleration is likely active!")
            elif gpu_info['tokens_per_second'] > CPU_THRESHOLD:
                print("\n⚠ Performance is moderate - GPU may or may not be active")
            else:
                print("\n⚠ Performance suggests CPU-only inference")
                print("  Check if NVIDIA Container Toolkit is installed and configured")
    else:
        print("\n✗ Failed to connect to Ollama or check GPU status")
        print("  Make sure the Ollama service is running")
    
    print("\n" + "=" * 60)
    print("\nTo verify GPU access at the system level, you can also run:")
    print("  docker exec ollama nvidia-smi")
    print("\nThis will show NVIDIA GPU information if available.")
