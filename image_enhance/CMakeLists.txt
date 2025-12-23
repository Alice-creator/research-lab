cmake_minimum_required(VERSION 3.18)
project(SRGAN CUDA CXX)

# C++ and CUDA standards
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CUDA_STANDARD 17)

# Find CUDA
find_package(CUDAToolkit REQUIRED)

# CUDA architecture for RTX 3060 (SM 86)
set(CMAKE_CUDA_ARCHITECTURES 86)

# Source files
set(CUDA_SOURCES
    src/cuda/tensor.cu
    src/cuda/operations.cu
    src/cuda/gemm.cu
    src/cuda/conv2d.cu
    src/cuda/batchnorm.cu
    src/cuda/activation.cu
    src/cuda/pixelshuffle.cu
)

set(CPP_SOURCES
    src/main.cpp
)

# Create executable
add_executable(srgan ${CPP_SOURCES} ${CUDA_SOURCES})

# Include directories
target_include_directories(srgan PRIVATE
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_SOURCE_DIR}/src/nn
    ${CMAKE_SOURCE_DIR}/src/utils
    ${CMAKE_SOURCE_DIR}/src/cuda
)

# Link CUDA runtime
target_link_libraries(srgan PRIVATE CUDA::cudart)

# Optional: Link cuBLAS for optimized matrix operations
# target_link_libraries(srgan PRIVATE CUDA::cublas)

# Compiler flags
target_compile_options(srgan PRIVATE
    $<$<COMPILE_LANGUAGE:CUDA>:-O3>
    $<$<COMPILE_LANGUAGE:CXX>:-O3>
)
