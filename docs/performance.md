# Performance Guide

## Memory Optimization

### Use Device-Local Memory
```python
# Prefer device-local buffers for GPU-only data
buf = Buffer.from_numpy(device, data, flags=BufferFlags.DEVICE_LOCAL)
```

### Reuse Buffers
```python
# Pre-allocate and reuse buffers
output = Buffer.empty(device, shape=(N, N))
for i in range(iterations):
    kernel.execute(..., args=[input, output, N])
    # Process output without reallocating
```

## Kernel Optimization

### Tune Block Size
```python
# Experiment with different block sizes
for block_size in [64, 128, 256, 512, 1024]:
    kernel.execute(grid=(N//block_size, 1, 1), block=(block_size, 1, 1), ...)
```

### Use Fast Math
```python
# Enable fast math for approximate computations
options = CompileOptions(fast_math=True)
kernel.compile(options)
```

## Profiling

### Built-in Timer
```python
from phoenix_core.utils import Timer

with Timer("Kernel Execution") as t:
    kernel.execute(...)

print(t)  # Shows elapsed time
```

## Common Patterns

### Batch Processing
```python
# Process data in batches for better GPU utilization
for batch in batches:
    input_buf.upload(batch)
    kernel.execute(...)
    result = output_buf.download()
```

### Overlap Compute and Transfer
```python
# Use streams for concurrent operations
with device.create_stream() as s1:
    kernel1.execute_async(..., stream=s1)
with device.create_stream() as s2:
    kernel2.execute_async(..., stream=s2)
s1.wait()
s2.wait()
```
