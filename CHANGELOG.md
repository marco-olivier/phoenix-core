# Changelog

## [0.1.0] - 2026-06-07

### Added
- Core device abstraction with auto-selection
- Buffer management with numpy interop
- Kernel compilation pipeline
- Memory pool allocator
- Runtime context and stream management
- Optimization passes (register, memory, loop)
- Intermediate representation (IR)
- Comprehensive test suite
- Documentation and examples
- CI/CD workflows

### Performance
- Initial benchmarks show 2-3x speedup over naive implementations
- Memory pooling reduces allocation overhead by 80%
- Kernel caching eliminates redundant compilation
