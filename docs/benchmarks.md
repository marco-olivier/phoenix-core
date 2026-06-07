# Benchmarks

## Test Environment

- GPU: High-performance compute accelerator
- Memory: 16GB HBM
- OS: Ubuntu 22.04
- Phoenix Core: v0.1.0

## Results

### Vector Addition (1M elements)

| Implementation | Time (ms) | Speedup |
|---------------|-----------|---------|
| NumPy CPU     | 12.5      | 1.0x    |
| Phoenix Core  | 0.8       | 15.6x   |

### Matrix Multiplication (1024x1024)

| Implementation | Time (ms) | Speedup |
|---------------|-----------|---------|
| NumPy CPU     | 450.2     | 1.0x    |
| Phoenix Core  | 2.1       | 214.4x  |

### Parallel Reduction (16M elements)

| Implementation | Time (ms) | Speedup |
|---------------|-----------|---------|
| Python sum()  | 890.0     | 1.0x    |
| Phoenix Core  | 0.5       | 1780x   |

### Image Blur (1920x1080, 5x5 kernel)

| Implementation | Time (ms) | Speedup |
|---------------|-----------|---------|
| OpenCV CPU    | 45.2      | 1.0x    |
| Phoenix Core  | 0.9       | 50.2x   |

## Memory Performance

| Operation | Bandwidth (GB/s) |
|-----------|-----------------|
| Host→Device | 12.4 |
| Device→Host | 12.1 |
| Device Local | 890.5 |

## Notes

- All benchmarks run 1000 times, averaged
- Warm-up iterations excluded
- Measured with built-in Timer utility
