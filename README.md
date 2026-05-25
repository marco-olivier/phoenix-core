# Phoenix Core

High-performance GPU compute library with hardware abstraction layer for parallel workloads.

## Features

- **Hardware Abstraction**: Unified API across GPU vendors
- **Memory Management**: Smart buffer allocation and pooling
- **Kernel Compilation**: Runtime shader/kernel compilation
- **Parallel Execution**: Multi-stream workload scheduling
- **Performance Profiling**: Built-in metrics collection

## Architecture

```
┌─────────────────────────────────────────┐
│           Application Layer             │
├─────────────────────────────────────────┤
│         Phoenix Core API                │
├──────────┬──────────┬───────────────────┤
│ Runtime  │ Compiler │ Memory Manager    │
├──────────┴──────────┴───────────────────┤
│        Hardware Abstraction             │
├─────────┬─────────┬─────────────────────┤
│  HIP    │  OpenCL │  Vulkan Compute     │
└─────────┴─────────┴─────────────────────┘
```

## Quick Start

```python
from phoenix_core import Device, Buffer, Kernel

# Initialize device
device = Device.auto_select()

# Create buffers
input_buf = Buffer.from_numpy(device, data)
output_buf = Buffer.empty(device, shape=(1024, 1024))

# Compile and run kernel
kernel = Kernel.from_file(device, "vector_add.hip")
kernel.execute(grid=(64, 1, 1), block=(256, 1, 1), 
               args=[input_buf, output_buf, N])

# Read results
result = output_buf.to_numpy()
```

## Requirements

- Python 3.9+
- ROCm 5.7+ / CUDA 12+ / Vulkan 1.3+
- CMake 3.20+

## Installation

```bash
pip install phoenix-core
```

## Documentation

- [Getting Started](docs/getting-started.md)
- [API Reference](docs/api-reference.md)
- [Performance Guide](docs/performance.md)
- [Examples](examples/)

## License

MIT License - see [LICENSE](LICENSE)
