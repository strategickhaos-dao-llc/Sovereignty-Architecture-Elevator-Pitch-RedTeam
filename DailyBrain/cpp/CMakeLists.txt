cmake_minimum_required(VERSION 3.10)
project(DailyBrain VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Source files
set(SOURCES
    src/main.cpp
    src/commute.cpp
    src/sleep.cpp
    src/reviews.cpp
    src/meetings.cpp
)

# Create executable
add_executable(daily_brain ${SOURCES})

# Include directories
target_include_directories(daily_brain PRIVATE src)

# Compiler flags
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(daily_brain PRIVATE -Wall -Wextra -pedantic)
endif()
