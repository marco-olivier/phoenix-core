"""Compiler tests"""
import pytest
from src.compiler.kernel import KernelCompiler, CompileOptions, CompileTarget
from src.compiler.optimizer import KernelOptimizer

VECTOR_ADD = """
__global__ void vector_add(float* a, float* b, float* c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) c[i] = a[i] + b[i];
}
"""

class TestKernelCompiler:
    def test_compile(self):
        compiler = KernelCompiler()
        result = compiler.compile(VECTOR_ADD)
        assert result.success == True
        assert result.binary is not None
    
    def test_compile_options(self):
        compiler = KernelCompiler()
        options = CompileOptions(
            target=CompileTarget.HIP,
            optimization_level=2,
            fast_math=True
        )
        result = compiler.compile(VECTOR_ADD, options)
        assert result.success == True
    
    def test_cache(self):
        compiler = KernelCompiler()
        r1 = compiler.compile(VECTOR_ADD)
        r2 = compiler.compile(VECTOR_ADD)
        assert r1.binary == r2.binary  # Should be cached

class TestKernelOptimizer:
    def test_passes(self):
        optimizer = KernelOptimizer()
        passes = optimizer.get_passes()
        assert len(passes) > 0
        assert 'register_allocator' in passes
    
    def test_optimize(self):
        optimizer = KernelOptimizer()
        ir = {'type': 'kernel', 'body': 'test'}
        result = optimizer.optimize(ir, level=2)
        assert result is not None
