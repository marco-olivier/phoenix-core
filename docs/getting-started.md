# Getting Started with Phoenix Core

## Installation

```bash
# From PyPI
pip install phoenix-core

# From source
git clone https://github.com/marco-olivier/phoenix-core.git
cd phoenix-core
pip install -e .
```

## Basic Usage

### 1. Device Selection

```python
from phoenix_core import Device

# Auto-select best GPU
device = Device.auto_select()

# Or list all devices
devices = Device.enumerate()
for d in devices:
    print(d)
```

### 2. Memory Management

```python
import numpy as np
from phoenix_core import Buffer

# Create buffer from numpy array
data = np.random.randn(1024, 1024).astype(np.float32)
buffer = Buffer.from_numpy(device, data)

# Download results
result = buffer.to_numpy()
```

### 3. Kernel Execution

```python
from phoenix_core import Kernel

# Load kernel
kernel = Kernel.from_file(device, "my_kernel.hip")

# Execute
kernel.execute(
    grid=(64, 1, 1),
    block=(256, 1, 1),
    args=[input_buf, output_buf, N]
)
```

## Next Steps

- Check [API Reference](api-reference.md) for detailed docs
- See [Examples](../examples/) for more code
- Read [Performance Guide](performance.md) for optimization tips
