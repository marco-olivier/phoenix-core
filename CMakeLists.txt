cmake_minimum_required(VERSION 3.20)
project(PhoenixCore VERSION 0.1.0 LANGUAGES CXX HIP)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Options
option(PHOENIX_BUILD_TESTS "Build tests" ON)
option(PHOENIX_BUILD_EXAMPLES "Build examples" ON)
option(PHOENIX_USE_HIP "Use HIP backend" ON)
option(PHOENIX_USE_OPENCL "Use OpenCL backend" OFF)

# Find HIP
if(PHOENIX_USE_HIP)
    find_package(hip REQUIRED)
    message(STATUS "HIP found: ${hip_VERSION}")
endif()

# Core library
add_library(phoenix_core STATIC
    src/runtime/device.cpp
    src/runtime/context.cpp
    src/runtime/stream.cpp
    src/memory/buffer.cpp
    src/memory/allocator.cpp
    src/compiler/kernel.cpp
    src/compiler/optimizer.cpp
)

target_include_directories(phoenix_core PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

if(PHOENIX_USE_HIP)
    target_link_libraries(phoenix_core PRIVATE hip::host hip::device)
    target_compile_definitions(phoenix_core PUBLIC PHOENIX_USE_HIP=1)
endif()

# Python bindings
add_subdirectory(python)

# Tests
if(PHOENIX_BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

# Examples
if(PHOENIX_BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()
