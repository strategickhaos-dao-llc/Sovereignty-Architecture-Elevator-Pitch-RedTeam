cmake_minimum_required(VERSION 3.10)
project(Solvern VERSION 1.0.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Compiler flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -pedantic")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g -O0")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")

# Source files
set(SOURCES
    solvern.cpp
)

# Headers
set(HEADERS
    primordial_vectors.hpp
)

# Executable
add_executable(solvern ${SOURCES} ${HEADERS})

# Include directories
target_include_directories(solvern PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Installation
install(TARGETS solvern DESTINATION bin)
install(FILES primordial_vectors.hpp DESTINATION include/solvern)
