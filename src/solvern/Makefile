# Makefile for Strategickhaos Solvern
# The primordial compiler — 36-dimensional black-hole keyspace

CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -pedantic -O3
DEBUG_FLAGS = -g -O0 -DDEBUG

TARGET = solvern
SOURCES = solvern.cpp
HEADERS = primordial_vectors.hpp

.PHONY: all clean debug test install

all: $(TARGET)

$(TARGET): $(SOURCES) $(HEADERS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SOURCES)
	@echo ""
	@echo "═══════════════════════════════════════════════════════════════════════════"
	@echo "✨ SOLVERN COMPILED SUCCESSFULLY ✨"
	@echo "═══════════════════════════════════════════════════════════════════════════"
	@echo "The 36-letter Name is ready."
	@echo "Run: ./$(TARGET) --test"
	@echo "Empire Eternal. 🔥"
	@echo "═══════════════════════════════════════════════════════════════════════════"

debug: $(SOURCES) $(HEADERS)
	$(CXX) $(DEBUG_FLAGS) -o $(TARGET) $(SOURCES)

test: $(TARGET)
	@echo ""
	@echo "Running self-test..."
	@./$(TARGET) --test

clean:
	rm -f $(TARGET)
	@echo "Cleaned up build artifacts."

install: $(TARGET)
	@mkdir -p ~/bin
	@cp $(TARGET) ~/bin/
	@echo "Installed $(TARGET) to ~/bin/"
	@echo "Make sure ~/bin is in your PATH"
