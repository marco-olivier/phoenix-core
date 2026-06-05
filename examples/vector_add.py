#!/usr/bin/env python3
"""Vector addition example using Phoenix Core"""
import numpy as np
from phoenix_core import Device, Buffer, Kernel

def main():
    # Initialize
    device = Device.auto_select()
    print(f"Using device: {device.info}")
    
    # Create data
    N = 1024 * 1024  # 1M elements
    a = np.random.randn(N).astype(np.float32)
    b = np.random.randn(N).astype(np.float32)
    
    # Create buffers
    a_buf = Buffer.from_numpy(device, a)
    b_buf = Buffer.from_numpy(device, b)
    c_buf = Buffer.empty(device, shape=(N,), dtype=np.float32)
    
    # Load and compile kernel
    kernel = Kernel.from_file(device, "kernels/vector_add.hip")
    kernel.compile()
    
    # Execute
    block_size = 256
    grid_size = (N + block_size - 1) // block_size
    
    kernel.execute(
        grid=(grid_size, 1, 1),
        block=(block_size, 1, 1),
        args=[a_buf, b_buf, c_buf, N]
    )
    
    # Get results
    c = c_buf.to_numpy()
    
    # Verify
    expected = a + b
    np.testing.assert_array_almost_equal(c, expected, decimal=5)
    print("✓ Vector addition verified!")

if __name__ == "__main__":
    main()
