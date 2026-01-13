'''
This script contains a test calculation to check that the AMD GPU
is successfully detected and can run computations. 
python3 /workspace/ROCm Example.py
'''

import torch
import time

def benchmark(device, size=8000):
    torch.manual_seed(0)

    # Create two large matrices
    A = torch.randn(size, size, device=device)
    B = torch.randn(size, size, device=device)

    # Warm-up
    for _ in range(2):
        _ = torch.mm(A, B)

    torch.cuda.synchronize() if device.startswith("cuda") or device.startswith("hip") else None

    start = time.time()
    _ = torch.mm(A, B)
    torch.cuda.synchronize() if device.startswith("cuda") or device.startswith("hip") else None
    end = time.time()

    return end - start


def main():
    print("PyTorch version:", torch.__version__)
    print("GPU available:", torch.cuda.is_available())

    SIZE = 10_000

    print("\nRunning CPU benchmark...")
    cpu_time = benchmark("cpu", SIZE)
    print(f"CPU time: {cpu_time:.3f} seconds")

    if torch.cuda.is_available():
        gpu_device = "cuda" if torch.cuda.is_available() else "hip"
        print("\nRunning GPU benchmark...")
        gpu_time = benchmark(gpu_device, SIZE)
        print(f"GPU time: {gpu_time:.3f} seconds")

        speedup = cpu_time / gpu_time
        print(f"\nSpeedup (CPU / GPU): {speedup:.1f}x")
        print(f"GPU name: {torch.cuda.get_device_name(0)}")

if __name__ == "__main__":
    main()