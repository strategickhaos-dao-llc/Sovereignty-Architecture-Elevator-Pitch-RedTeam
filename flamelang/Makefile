# FlameLang Makefile
# Build automation

.PHONY: help install test clean repl demo run-demo

help:
	@echo "🔥 FlameLang Build Automation"
	@echo ""
	@echo "Available targets:"
	@echo "  install    - Install dependencies"
	@echo "  test       - Run test suite"
	@echo "  repl       - Start interactive REPL"
	@echo "  demo       - Run interactive demo"
	@echo "  run-demo   - Execute demo.fl example"
	@echo "  clean      - Remove build artifacts"
	@echo "  help       - Show this help"

install:
	@echo "🔥 Installing FlameLang dependencies..."
	pip3 install numpy sympy scipy psutil
	chmod +x flamelang
	@echo "✓ Installation complete"
	@echo ""
	@echo "Try: make repl"

test:
	@echo "🔥 Running FlameLang test suite..."
	python3 tests/test_all.py

repl:
	@echo "🔥 Starting FlameLang REPL..."
	./flamelang repl

demo:
	@echo "🔥 Running interactive demo..."
	python3 demo.py

run-demo:
	@echo "🔥 Executing demo.fl..."
	./flamelang run examples/demo.fl

clean:
	@echo "🔥 Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Clean complete"
