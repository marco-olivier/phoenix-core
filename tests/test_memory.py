"""Memory management tests"""
import pytest
from src.memory.allocator import MemoryPool, Allocator

class TestMemoryPool:
    def test_allocate(self):
        pool = MemoryPool(device_id=0)
        block = pool.allocate(1024)
        assert block is not None
        assert block.size >= 1024
        assert block.in_use == True
    
    def test_free(self):
        pool = MemoryPool(device_id=0)
        block = pool.allocate(1024)
        pool.free(block)
        assert block.in_use == False
    
    def test_available(self):
        pool = MemoryPool(device_id=0)
        initial = pool.available
        block = pool.allocate(1024)
        assert pool.available < initial
        pool.free(block)
        assert pool.available == initial

class TestAllocator:
    def test_allocate_free(self):
        block = Allocator.allocate(0, 1024)
        assert block is not None
        Allocator.free(block)
    
    def test_stats(self):
        stats = Allocator.stats()
        assert isinstance(stats, dict)
