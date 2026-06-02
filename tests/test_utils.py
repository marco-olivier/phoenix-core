"""Utility tests"""
import pytest
from src.utils.validation import validate_shape, validate_dtype, validate_grid_block
from src.utils.timer import Timer
import numpy as np

class TestValidation:
    def test_validate_shape(self):
        validate_shape((1024, 1024))  # Should not raise
        with pytest.raises(ValueError):
            validate_shape(())
        with pytest.raises(ValueError):
            validate_shape((-1, 1024))
    
    def test_validate_dtype(self):
        validate_dtype(np.float32, [np.float32, np.float64])
        with pytest.raises(ValueError):
            validate_dtype(np.int32, [np.float32])
    
    def test_validate_grid_block(self):
        validate_grid_block((64, 1, 1), (256, 1, 1))
        with pytest.raises(ValueError):
            validate_grid_block((64,), (256,))  # Wrong dimensions
        with pytest.raises(ValueError):
            validate_grid_block((1, 1, 1), (1025, 1, 1))  # Block too large

class TestTimer:
    def test_timer(self):
        import time
        t = Timer("Test")
        t.start()
        time.sleep(0.01)
        elapsed = t.stop()
        assert elapsed >= 0.01
    
    def test_context_manager(self):
        import time
        with Timer("Context") as t:
            time.sleep(0.01)
        assert t.elapsed >= 0.01
