"""Memory allocator with pooling"""
from typing import Dict, Optional, Tuple
from collections import defaultdict
import threading

class MemoryBlock:
    """Represents a block of device memory"""
    def __init__(self, ptr: int, size: int, device_id: int):
        self.ptr = ptr
        self.size = size
        self.device_id = device_id
        self.in_use = False
        self.ref_count = 0
    
    def __repr__(self):
        return f"Block(ptr=0x{self.ptr:x}, size={self.size}, used={self.in_use})"

class MemoryPool:
    """Pool of pre-allocated memory blocks"""
    
    def __init__(self, device_id: int, initial_size: int = 1024 * 1024 * 256):
        self.device_id = device_id
        self.total_size = initial_size
        self.blocks: Dict[int, MemoryBlock] = {}
        self.free_blocks: list = []
        self._lock = threading.Lock()
        
        # Pre-allocate initial pool
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Pre-allocate memory pool"""
        block = MemoryBlock(
            ptr=0x10000000,  # Simulated pointer
            size=self.total_size,
            device_id=self.device_id
        )
        self.blocks[block.ptr] = block
        self.free_blocks.append(block)
    
    def allocate(self, size: int, alignment: int = 256) -> Optional[MemoryBlock]:
        """Allocate memory block from pool"""
        with self._lock:
            # Align size
            aligned_size = (size + alignment - 1) & ~(alignment - 1)
            
            # Find best fit
            best_fit = None
            for block in self.free_blocks:
                if block.size >= aligned_size:
                    if best_fit is None or block.size < best_fit.size:
                        best_fit = block
            
            if best_fit is None:
                return None  # Out of memory
            
            # Split block if too large
            if best_fit.size > aligned_size * 2:
                new_block = MemoryBlock(
                    ptr=best_fit.ptr + aligned_size,
                    size=best_fit.size - aligned_size,
                    device_id=self.device_id
                )
                self.blocks[new_block.ptr] = new_block
                self.free_blocks.append(new_block)
                best_fit.size = aligned_size
            
            best_fit.in_use = True
            self.free_blocks.remove(best_fit)
            return best_fit
    
    def free(self, block: MemoryBlock):
        """Return block to pool"""
        with self._lock:
            block.in_use = False
            block.ref_count = 0
            self.free_blocks.append(block)
            # TODO: Merge adjacent free blocks
    
    @property
    def available(self) -> int:
        """Total available memory in pool"""
        return sum(b.size for b in self.free_blocks)
    
    @property
    def used(self) -> int:
        """Total used memory in pool"""
        return sum(b.size for b in self.blocks.values() if b.in_use)

class Allocator:
    """Global memory allocator"""
    
    _pools: Dict[int, MemoryPool] = {}
    _lock = threading.Lock()
    
    @classmethod
    def get_pool(cls, device_id: int) -> MemoryPool:
        """Get or create memory pool for device"""
        with cls._lock:
            if device_id not in cls._pools:
                cls._pools[device_id] = MemoryPool(device_id)
            return cls._pools[device_id]
    
    @classmethod
    def allocate(cls, device_id: int, size: int) -> Optional[MemoryBlock]:
        """Allocate memory on device"""
        pool = cls.get_pool(device_id)
        return pool.allocate(size)
    
    @classmethod
    def free(cls, block: MemoryBlock):
        """Free memory block"""
        pool = cls.get_pool(block.device_id)
        pool.free(block)
    
    @classmethod
    def stats(cls) -> Dict[int, Dict[str, int]]:
        """Get memory statistics for all devices"""
        stats = {}
        for device_id, pool in cls._pools.items():
            stats[device_id] = {
                'total': pool.total_size,
                'used': pool.used,
                'available': pool.available,
            }
        return stats
