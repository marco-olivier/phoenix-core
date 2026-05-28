"""Compute context management"""
from typing import Optional, Dict
import threading

class Context:
    """Manages GPU compute context and resources"""
    
    _current: Optional['Context'] = None
    _lock = threading.Lock()
    
    def __init__(self, device_id: int = 0):
        self.device_id = device_id
        self.streams = []
        self.memory_pools = {}
        self._initialized = False
    
    @classmethod
    def current(cls) -> 'Context':
        """Get current active context"""
        with cls._lock:
            if cls._current is None:
                cls._current = Context()
            return cls._current
    
    @classmethod
    def set_current(cls, ctx: 'Context'):
        """Set active context"""
        with cls._lock:
            cls._current = ctx
    
    def initialize(self):
        """Initialize compute context"""
        if self._initialized:
            return
        # Platform-specific initialization
        self._initialized = True
    
    def create_stream(self, priority: int = 0):
        """Create execution stream"""
        from .stream import Stream
        stream = Stream(self, priority)
        self.streams.append(stream)
        return stream
    
    def synchronize(self):
        """Wait for all operations to complete"""
        for stream in self.streams:
            stream.synchronize()
    
    def __enter__(self):
        self.initialize()
        self.set_current(self)
        return self
    
    def __exit__(self, *args):
        self.synchronize()
