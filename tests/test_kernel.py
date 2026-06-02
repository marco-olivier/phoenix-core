"""Kernel tests"""
import pytest
from src.device import Device
from src.kernel import Kernel

VECTOR_ADD = """
__global__ void vector_add(float* a, float* b, float* c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        c[i] = a[i] + b[i];
    }
}
"""

class TestKernel:
    def test_from_string(self, device):
        kernel = Kernel.from_string(device, VECTOR_ADD, language="hip")
        assert kernel.source.language == "hip"
        assert kernel._compiled == False
    
    def test_compile(self, device):
        kernel = Kernel.from_string(device, VECTOR_ADD)
        kernel.compile()
        assert kernel._compiled == True
    
    def test_execute(self, device):
        kernel = Kernel.from_string(device, VECTOR_ADD)
        kernel.compile()
        # Execute with dummy args
        kernel.execute(
            grid=(1, 1, 1),
            block=(256, 1, 1),
            args=[None, None, None, 1024]
        )
