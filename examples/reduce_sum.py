#!/usr/bin/env python3
"""Parallel reduction sum example"""
import numpy as np
from phoenix_core import Device, Buffer, Kernel

def main():
    device = Device.auto_select()
    
    # Large array for reduction
    N = 16 * 1024 * 1024  # 16M elements
    data = np.random.randn(N).astype(np.float32)
    
    # Upload
    data_buf = Buffer.from_numpy(device, data)
    result_buf = Buffer.zeros(device, shape=(1,), dtype=np.float32)
    
    # Load reduction kernel
    kernel = Kernel.from_file(device, "kernels/reduce.hip")
    kernel.compile()
    
    # Execute with shared memory
    BLOCK_SIZE = 256
    grid_size = (N + BLOCK_SIZE - 1) // BLOCK_SIZE
    
    kernel.execute(
        grid=(grid_size, 1, 1),
        block=(BLOCK_SIZE, 1, 1),
        args=[data_buf, result_buf, N],
        shared_mem=BLOCK_SIZE * 4  # float32 = 4 bytes
    )
    
    gpu_sum = result_buf.to_numpy()[0]
    cpu_sum = np.sum(data)
    
    print(f"GPU sum: {gpu_sum:.6f}")
    print(f"CPU sum: {cpu_sum:.6f}")
    print(f"✓ Reduction verified (error: {abs(gpu_sum - cpu_sum):.6e})")

if __name__ == "__main__":
    main()
