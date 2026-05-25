"""Device abstraction for GPU hardware"""
from enum import Enum
from typing import Optional, List
import ctypes

class DeviceType(Enum):
    GPU = "gpu"
    CPU = "cpu"
    AUTO = "auto"

class DeviceInfo:
    """Hardware device information"""
    def __init__(self, device_id: int, name: str, vendor: str, 
                 memory_total: int, compute_units: int):
        self.device_id = device_id
        self.name = name
        self.vendor = vendor
        self.memory_total = memory_total
        self.compute_units = compute_units
        self.memory_free = memory_total  # Initial state
    
    def __repr__(self):
        return f"Device({self.name}, {self.memory_total // (1024**3)}GB, {self.compute_units} CUs)"

class Device:
    """GPU device abstraction"""
    _devices: List['Device'] = []
    _initialized = False
    
    def __init__(self, device_id: int = 0):
        self.device_id = device_id
        self._info = self._probe_device(device_id)
        self._context = None
    
    @classmethod
    def auto_select(cls) -> 'Device':
        """Automatically select best available device"""
        devices = cls.enumerate()
        if not devices:
            raise RuntimeError("No GPU devices found")
        # Select device with most memory
        best = max(devices, key=lambda d: d.memory_total)
        return cls(best.device_id)
    
    @classmethod
    def enumerate(cls) -> List[DeviceInfo]:
        """List all available GPU devices"""
        if not cls._initialized:
            cls._probe_all_devices()
        return cls._devices
    
    def _probe_device(self, device_id: int) -> DeviceInfo:
        """Probe device capabilities"""
        # Hardware detection via HIP/OpenCL
        return DeviceInfo(
            device_id=device_id,
            name="GPU Device",
            vendor="Unknown",
            memory_total=16 * (1024**3),  # 16GB default
            compute_units=120
        )
    
    @classmethod
    def _probe_all_devices(cls):
        """Detect all available devices"""
        cls._devices = []
        # Platform-specific detection
        cls._initialized = True
    
    def create_context(self):
        """Create compute context for this device"""
        if self._context is None:
            self._context = DeviceContext(self)
        return self._context
    
    @property
    def info(self) -> DeviceInfo:
        return self._info

class DeviceContext:
    """Compute context managing device state"""
    def __init__(self, device: Device):
        self.device = device
        self.streams = []
    
    def create_stream(self):
        """Create a new execution stream"""
        stream = Stream(self)
        self.streams.append(stream)
        return stream
    
    def synchronize(self):
        """Wait for all streams to complete"""
        for stream in self.streams:
            stream.wait()

class Stream:
    """Asynchronous execution stream"""
    def __init__(self, context: DeviceContext):
        self.context = context
        self.operations = []
    
    def submit(self, operation):
        """Submit operation to stream"""
        self.operations.append(operation)
    
    def wait(self):
        """Wait for stream to complete"""
        pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.wait()
