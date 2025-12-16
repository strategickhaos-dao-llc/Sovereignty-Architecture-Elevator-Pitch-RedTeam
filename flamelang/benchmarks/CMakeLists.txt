cmake_minimum_required(VERSION 3.20)
project(FlameLangBenchmarks CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Find Google Benchmark
find_package(benchmark REQUIRED)

# Compiler flags for optimized benchmarks
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    add_compile_options(-O3 -march=native -Wall -Wextra)
endif()

# C++ Benchmark executable
add_executable(cpp_benchmark cpp_benchmark.cpp)
target_link_libraries(cpp_benchmark benchmark::benchmark pthread)

# Enable testing
enable_testing()

# Add benchmark as a test
add_test(NAME cpp_benchmark_run COMMAND cpp_benchmark)

# Installation
install(TARGETS cpp_benchmark DESTINATION bin)

# Custom target to run benchmarks with nice output
add_custom_target(run_benchmarks
    COMMAND cpp_benchmark --benchmark_format=json --benchmark_out=cpp_results.json
    DEPENDS cpp_benchmark
    COMMENT "Running C++ benchmarks..."
)
