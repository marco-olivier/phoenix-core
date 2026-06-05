#!/usr/bin/env python3
"""Matrix multiplication example using Phoenix Core"""
import numpy as np
from phoenix_core import Device, Buffer, Kernel

def main():
    device = Device.auto_select()
    
    # Matrix dimensions
    M, N, K = 1024, 1024, 1024
    
    # Create matrices
    A = np.random.randn(M, K).astype(np.float32)
    B = np.random.randn(K, N).astype(np.float32)
    
    # Upload to GPU
    a_buf = Buffer.from_numpy(device, A)
    b_buf = Buffer.from_numpy(device, B)
    c_buf = Buffer.zeros(device, shape=(M, N), dtype=np.float32)
    
    # Load matrix multiply kernel
    kernel = Kernel.from_file(device, "kernels/matmul.hip")
    kernel.compile()
    
    # Execute with tiled approach
    TILE = 16
    kernel.execute(
        grid=(N // TILE, M // TILE, 1),
        block=(TILE, TILE, 1),
        args=[a_buf, b_buf, c_buf, M, N, K]
    )
    
    # Verify
    C = c_buf.to_numpy()
    expected = A @ B
    np.testing.assert_array_almost_equal(C, expected, decimal=3)
    print("✓ Matrix multiplication verified!")

if __name__ == "__main__":
    main()
