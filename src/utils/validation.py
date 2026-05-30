"""Input validation utilities"""
from typing import Tuple, Union
import numpy as np

def validate_shape(shape: Tuple[int, ...], name: str = "shape"):
    """Validate tensor shape"""
    if not isinstance(shape, tuple):
        raise TypeError(f"{name} must be a tuple, got {type(shape)}")
    if len(shape) == 0:
        raise ValueError(f"{name} cannot be empty")
    for i, dim in enumerate(shape):
        if not isinstance(dim, int) or dim <= 0:
            raise ValueError(f"{name}[{i}] must be positive integer, got {dim}")

def validate_dtype(dtype, allowed: list = None):
    """Validate data type"""
    if allowed and dtype not in allowed:
        raise ValueError(f"Unsupported dtype: {dtype}. Allowed: {allowed}")

def validate_device_id(device_id: int):
    """Validate device ID"""
    if not isinstance(device_id, int) or device_id < 0:
        raise ValueError(f"Invalid device ID: {device_id}")

def validate_grid_block(grid: Tuple[int, int, int], block: Tuple[int, int, int]):
    """Validate grid and block dimensions"""
    for name, dims in [("grid", grid), ("block", block)]:
        if len(dims) != 3:
            raise ValueError(f"{name} must have 3 dimensions")
        for i, d in enumerate(dims):
            if d <= 0:
                raise ValueError(f"{name}[{i}] must be positive")
    
    # Check block size limit
    block_size = block[0] * block[1] * block[2]
    if block_size > 1024:
        raise ValueError(f"Block size {block_size} exceeds maximum 1024")
