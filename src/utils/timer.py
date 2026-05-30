"""Performance timing utilities"""
import time
from typing import Optional
from contextlib import contextmanager

class Timer:
    """High-resolution timer for performance measurement"""
    
    def __init__(self, name: str = "Timer"):
        self.name = name
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.elapsed: Optional[float] = None
    
    def start(self):
        """Start timer"""
        self.start_time = time.perf_counter()
        return self
    
    def stop(self) -> float:
        """Stop timer and return elapsed time"""
        self.end_time = time.perf_counter()
        self.elapsed = self.end_time - self.start_time
        return self.elapsed
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, *args):
        self.stop()
    
    def __repr__(self):
        if self.elapsed is not None:
            return f"{self.name}: {self.elapsed*1000:.2f}ms"
        return f"{self.name}: not started"

@contextmanager
def timer(name: str = "Operation"):
    """Context manager for timing"""
    t = Timer(name)
    t.start()
    yield t
    t.stop()
