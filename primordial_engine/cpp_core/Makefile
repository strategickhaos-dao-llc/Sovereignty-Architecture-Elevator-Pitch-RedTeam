# Makefile for Primordial Tongues Engine C++ Core

CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2
TARGET = primordial_engine
SOURCES = primordial_core.cpp example_usage.cpp
OBJECTS = $(SOURCES:.cpp=.o)

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJECTS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $<

clean:
	rm -f $(OBJECTS) $(TARGET)

run: $(TARGET)
	./$(TARGET)

.PHONY: all clean run
