"""Memory buffer management for GPU data"""
from typing import Optional, Tuple, Union
import numpy as np

class BufferFlags:
    READ_WRITE = 0x01
    READ_ONLY = 0x02
    WRITE_ONLY = 0x04
    HOST_ACCESS = 0x08
    DEVICE_LOCAL = 0x10

class Buffer:
    """GPU memory buffer with automatic management"""
    
    def __init__(self, device: 'Device', size: int, flags: int = BufferFlags.READ_WRITE):
        self.device = device
        self.size = size
        self.flags = flags
        self._ptr = None
        self._allocated = False
    
    @classmethod
    def from_numpy(cls, device: 'Device', data: np.ndarray, 
                   flags: int = BufferFlags.READ_WRITE) -> 'Buffer':
        """Create buffer from numpy array"""
        buf = cls(device, data.nbytes, flags)
        buf.upload(data)
        return buf
    
    @classmethod
    def empty(cls, device: 'Device', shape: Tuple[int, ...], 
              dtype=np.float32, flags: int = BufferFlags.READ_WRITE) -> 'Buffer':
        """Create empty buffer with given shape"""
        size = int(np.prod(shape)) * np.dtype(dtype).itemsize
        return cls(device, size, flags)
    
    @classmethod
    def zeros(cls, device: 'Device', shape: Tuple[int, ...],
              dtype=np.float32, flags: int = BufferFlags.READ_WRITE) -> 'Buffer':
        """Create zero-initialized buffer"""
        data = np.zeros(shape, dtype=dtype)
        return cls.from_numpy(device, data, flags)
    
    def upload(self, data: np.ndarray):
        """Upload data to GPU"""
        if data.nbytes > self.size:
            raise ValueError(f"Data size {data.nbytes} exceeds buffer size {self.size}")
        self._allocate()
        # Transfer to device memory
        self._ptr = data.tobytes()
        self.shape = data.shape
        self.dtype = data.dtype
    
    def download(self) -> np.ndarray:
        """Download data from GPU"""
        if not self._allocated:
            raise RuntimeError("Buffer not allocated")
        # Transfer from device memory
        return np.frombuffer(self._ptr, dtype=self.dtype).reshape(self.shape)
    
    def to_numpy(self) -> np.ndarray:
        """Alias for download()"""
        return self.download()
    
    def _allocate(self):
        """Allocate device memory"""
        if not self._allocated:
            # Platform-specific allocation
            self._allocated = True
    
    def release(self):
        """Release device memory"""
        if self._allocated:
            self._ptr = None
            self._allocated = False
    
    def __del__(self):
        self.release()
    
    def __repr__(self):
        status = "allocated" if self._allocated else "empty"
        return f"Buffer({self.size} bytes, {status})"
