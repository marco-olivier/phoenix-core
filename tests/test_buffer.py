"""Buffer tests"""
import pytest
import numpy as np
from src.device import Device
from src.buffer import Buffer

class TestBuffer:
    def test_from_numpy(self, device, random_array):
        buf = Buffer.from_numpy(device, random_array)
        assert buf.size == random_array.nbytes
    
    def test_empty(self, device):
        buf = Buffer.empty(device, shape=(1024,), dtype=np.float32)
        assert buf.size == 1024 * 4
    
    def test_zeros(self, device):
        buf = Buffer.zeros(device, shape=(100, 100))
        result = buf.to_numpy()
        np.testing.assert_array_equal(result, np.zeros((100, 100)))
    
    def test_upload_download(self, device, small_array):
        buf = Buffer.from_numpy(device, small_array)
        result = buf.to_numpy()
        np.testing.assert_array_almost_equal(result, small_array)
    
    def test_release(self, device):
        buf = Buffer.empty(device, shape=(100,))
        assert buf.size > 0
        buf.release()
