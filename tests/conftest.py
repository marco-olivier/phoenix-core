"""Test configuration and fixtures"""
import pytest
import numpy as np
from src.device import Device
from src.buffer import Buffer

@pytest.fixture
def device():
    """Get test device"""
    return Device(0)

@pytest.fixture
def random_array():
    """Generate random numpy array"""
    return np.random.randn(1024, 1024).astype(np.float32)

@pytest.fixture
def small_array():
    """Small test array"""
    return np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float32)
