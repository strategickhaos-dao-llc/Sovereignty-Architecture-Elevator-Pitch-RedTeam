.PHONY: install install-dev test clean

install:
	@echo "🔥 Installing FlameLang..."
	@./install.sh

install-dev:
	@echo "🔥 Installing FlameLang (development mode)..."
	@pip3 install -e .
	@echo "✓ Development installation complete"

test:
	@echo "🔥 Running tests..."
	@cd tests && python3 test_all.py

clean:
	@echo "🔥 Cleaning build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@rm -rf build dist *.egg-info 2>/dev/null || true
	@echo "✓ Clean complete"
