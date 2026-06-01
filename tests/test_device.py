"""Device tests"""
import pytest
from src.device import Device, DeviceInfo

class TestDevice:
    def test_enumerate(self):
        devices = Device.enumerate()
        assert isinstance(devices, list)
    
    def test_auto_select(self):
        device = Device.auto_select()
        assert isinstance(device, Device)
        assert device.device_id >= 0
    
    def test_device_info(self):
        device = Device(0)
        info = device.info
        assert isinstance(info, DeviceInfo)
        assert info.memory_total > 0
    
    def test_create_context(self):
        device = Device(0)
        ctx = device.create_context()
        assert ctx is not None
        assert ctx.device == device
