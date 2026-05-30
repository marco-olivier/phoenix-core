"""Custom exceptions"""

class PhoenixError(Exception):
    """Base exception for Phoenix Core"""
    pass

class DeviceError(PhoenixError):
    """Device-related errors"""
    pass

class MemoryError(PhoenixError):
    """Memory allocation errors"""
    pass

class CompileError(PhoenixError):
    """Kernel compilation errors"""
    def __init__(self, message: str, errors: list = None):
        super().__init__(message)
        self.errors = errors or []

class RuntimeError(PhoenixError):
    """Runtime execution errors"""
    pass

class InvalidArgumentError(PhoenixError):
    """Invalid argument errors"""
    pass
