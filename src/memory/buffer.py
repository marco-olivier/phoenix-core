"""Managed buffer with automatic lifecycle"""
from typing import Optional
from .allocator import Allocator, MemoryBlock
import numpy as np

class ManagedBuffer:
    """Buffer with automatic memory management"""
    
    def __init__(self, device_id: int, size: int):
        self.device_id = device_id
        self.size = size
        self._block: Optional[MemoryBlock] = None
        self._acquire()
    
    def _acquire(self):
        """Acquire memory from allocator"""
        self._block = Allocator.allocate(self.device_id, self.size)
        if self._block is None:
            raise MemoryError(f"Failed to allocate {self.size} bytes on device {self.device_id}")
    
    def upload(self, data: np.ndarray):
        """Upload numpy array to buffer"""
        if data.nbytes > self.size:
            raise ValueError(f"Data too large: {data.nbytes} > {self.size}")
        # Transfer data to device
        self._data = data.copy()
    
    def download(self) -> np.ndarray:
        """Download buffer contents to numpy"""
        if not hasattr(self, '_data'):
            raise RuntimeError("No data in buffer")
        return self._data.copy()
    
    def release(self):
        """Release buffer memory"""
        if self._block is not None:
            Allocator.free(self._block)
            self._block = None
    
    def __del__(self):
        self.release()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.release()
    
    @property
    def is_allocated(self) -> bool:
        return self._block is not None
