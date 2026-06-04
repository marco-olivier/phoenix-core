# Architecture Overview

## System Components

Phoenix Core is organized into several subsystems:

```
┌─────────────────────────────────────────────────────┐
│                    Application                       │
├─────────────────────────────────────────────────────┤
│                  Phoenix Core API                    │
├────────────┬─────────────┬─────────────────────────┤
│  Runtime   │  Compiler   │    Memory Manager        │
│            │             │                          │
│ - Context  │ - Parser    │ - Pool Allocator         │
│ - Stream   │ - Optimizer │ - Buffer Manager         │
│ - Executor │ - Codegen   │ - Reference Counting     │
├────────────┴─────────────┴─────────────────────────┤
│              Hardware Abstraction Layer              │
├──────────┬──────────┬──────────┬───────────────────┤
│   HIP    │  OpenCL  │  Vulkan  │   CPU Fallback    │
└──────────┴──────────┴──────────┴───────────────────┘
```

## Design Principles

1. **Zero-overhead abstraction**: Core API adds minimal overhead
2. **Lazy initialization**: Resources allocated on first use
3. **Thread safety**: All public APIs are thread-safe
4. **Extensible backends**: Easy to add new hardware support

## Data Flow

1. User creates Device and Buffers
2. Kernel compiled on first use (cached)
3. Runtime dispatches to appropriate backend
4. Results copied back via Buffer API

## Memory Model

- Host memory: CPU-accessible, pageable
- Device memory: GPU-local, high bandwidth
- Managed memory: Automatic migration (if supported)
