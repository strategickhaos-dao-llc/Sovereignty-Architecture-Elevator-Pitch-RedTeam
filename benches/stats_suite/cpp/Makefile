# BM-001: Makefile for C++ Statistical Benchmarks

CXX = g++
CXXFLAGS = -std=c++17 -O3 -Wall -Wextra -march=native
TARGET = five_number_summary

.PHONY: all clean test

all: $(TARGET)

$(TARGET): five_number_summary.cpp
	$(CXX) $(CXXFLAGS) -o $(TARGET) five_number_summary.cpp

clean:
	rm -f $(TARGET)

test: $(TARGET)
	@echo "Testing with small dataset..."
	@echo "10 20 30 40 50 60 70 80 90 100" | ./$(TARGET)
