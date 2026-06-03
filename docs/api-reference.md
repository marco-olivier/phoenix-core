# API Reference

## Device

### `Device(device_id: int = 0)`
Create device instance.

### `Device.auto_select() -> Device`
Automatically select best available device.

### `Device.enumerate() -> List[DeviceInfo]`
List all available GPU devices.

### `device.info -> DeviceInfo`
Get device information.

## Buffer

### `Buffer.from_numpy(device, data, flags) -> Buffer`
Create buffer from numpy array.

### `Buffer.empty(device, shape, dtype, flags) -> Buffer`
Create empty buffer.

### `Buffer.zeros(device, shape, dtype, flags) -> Buffer`
Create zero-initialized buffer.

### `buffer.upload(data)`
Upload numpy array to GPU.

### `buffer.download() -> np.ndarray`
Download buffer contents.

### `buffer.to_numpy() -> np.ndarray`
Alias for download().

### `buffer.release()`
Release device memory.

## Kernel

### `Kernel.from_file(device, path) -> Kernel`
Load kernel from file.

### `Kernel.from_string(device, source, language) -> Kernel`
Create kernel from source string.

### `kernel.compile(options=None)`
Compile kernel for execution.

### `kernel.execute(grid, block, args, shared_mem=0)`
Execute kernel.

## Memory

### `MemoryPool(device_id, initial_size)`
Create memory pool.

### `Allocator.allocate(device_id, size) -> MemoryBlock`
Allocate memory block.

### `Allocator.free(block)`
Free memory block.

### `Allocator.stats() -> Dict`
Get memory statistics.
