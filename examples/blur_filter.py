#!/usr/bin/env python3
"""Image blur filter using GPU convolution"""
import numpy as np
from phoenix_core import Device, Buffer, Kernel

def main():
    device = Device.auto_select()
    
    # Create test image
    width, height = 1920, 1080
    image = np.random.randn(height, width, 3).astype(np.float32)
    
    # Gaussian blur kernel (5x5)
    kernel_weights = np.array([
        [1, 4, 6, 4, 1],
        [4, 16, 24, 16, 4],
        [6, 24, 36, 24, 6],
        [4, 16, 24, 16, 4],
        [1, 4, 6, 4, 1]
    ], dtype=np.float32) / 256.0
    
    # Upload data
    img_buf = Buffer.from_numpy(device, image)
    out_buf = Buffer.zeros(device, shape=image.shape)
    weight_buf = Buffer.from_numpy(device, kernel_weights)
    
    # Load blur kernel
    kernel = Kernel.from_file(device, "kernels/blur.hip")
    kernel.compile()
    
    # Execute
    BLOCK = 16
    kernel.execute(
        grid=(width // BLOCK, height // BLOCK, 1),
        block=(BLOCK, BLOCK, 1),
        args=[img_buf, out_buf, weight_buf, width, height]
    )
    
    result = out_buf.to_numpy()
    print(f"✓ Blur filter applied to {width}x{height} image")

if __name__ == "__main__":
    main()
