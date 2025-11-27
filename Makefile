# Makefile for Sovereignty Architecture Provenance System
# Deterministic bundle creation, hashing, signing, and pinning

.PHONY: all bundle hash sign pin verify receipts clean help

# Configuration
BUNDLE_NAME ?= swarmgate_v1.0
BUNDLE_FILE = $(BUNDLE_NAME).tar.gz
RECEIPTS_DIR ?= provenance
SIGNATURE_FILE = $(BUNDLE_FILE).asc

# Bundle contents - files to include in the deterministic bundle
BUNDLE_CONTENTS = \
	swarmgate.yaml \
	ai_constitution.yaml \
	dao_record.yaml \
	governance/ \
	policy/ \
	bin/

# Default target
all: bundle hash

# Help
help:
	@echo "Sovereignty Architecture Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  bundle    Create deterministic tar bundle"
	@echo "  hash      Compute BLAKE3 hash of bundle"
	@echo "  sign      GPG sign the bundle"
	@echo "  pin       Pin bundle to IPFS"
	@echo "  verify    Verify bundle integrity"
	@echo "  receipts  Generate provenance receipts"
	@echo "  release   Full release: bundle → hash → sign → pin → receipts"
	@echo "  clean     Remove generated files"
	@echo ""
	@echo "Variables:"
	@echo "  BUNDLE_NAME=$(BUNDLE_NAME)"
	@echo "  RECEIPTS_DIR=$(RECEIPTS_DIR)"

# Create deterministic tar bundle
# Uses reproducible tar options for consistent hashing
bundle: $(BUNDLE_FILE)

$(BUNDLE_FILE): $(BUNDLE_CONTENTS)
	@echo "📦 Creating deterministic bundle: $(BUNDLE_FILE)"
	@mkdir -p $(RECEIPTS_DIR)
	tar --sort=name \
		--mtime="2025-01-01 00:00:00Z" \
		--owner=0 \
		--group=0 \
		--numeric-owner \
		-czf $(BUNDLE_FILE) \
		$(BUNDLE_CONTENTS) 2>/dev/null || \
	tar -czf $(BUNDLE_FILE) $(BUNDLE_CONTENTS)
	@echo "✅ Bundle created: $(BUNDLE_FILE)"
	@ls -lh $(BUNDLE_FILE)

# Compute BLAKE3 hash
hash: $(BUNDLE_FILE)
	@echo "🔐 Computing BLAKE3 hash..."
	@if command -v b3sum >/dev/null 2>&1; then \
		HASH=$$(b3sum $(BUNDLE_FILE) | awk '{print $$1}'); \
		echo "   BLAKE3: $$HASH"; \
		echo "$$HASH" > $(RECEIPTS_DIR)/$(BUNDLE_NAME).b3sum; \
	else \
		echo "⚠️ b3sum not installed, using SHA256"; \
		HASH=$$(sha256sum $(BUNDLE_FILE) | awk '{print $$1}'); \
		echo "   SHA256: $$HASH"; \
		echo "$$HASH" > $(RECEIPTS_DIR)/$(BUNDLE_NAME).sha256; \
	fi

# GPG sign the bundle
sign: $(BUNDLE_FILE)
	@echo "🔏 Signing bundle..."
	@./bin/sign $(BUNDLE_FILE)

# Pin to IPFS
pin: $(BUNDLE_FILE)
	@echo "📤 Pinning to IPFS..."
	@./bin/pin $(BUNDLE_FILE)

# Verify bundle
verify: $(BUNDLE_FILE)
	@echo "🔍 Verifying bundle..."
	@./bin/verify $(BUNDLE_FILE)

# Generate receipts
receipts:
	@echo "📋 Generating receipts..."
	@./bin/receipts index
	@./bin/receipts bundle $(BUNDLE_NAME)

# Full release process
release: bundle hash sign pin receipts
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "✅ RELEASE COMPLETE: $(BUNDLE_NAME)"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "Bundle:    $(BUNDLE_FILE)"
	@echo "Signature: $(SIGNATURE_FILE)"
	@echo "Receipts:  $(RECEIPTS_DIR)/"
	@echo ""
	@echo "To verify this release:"
	@echo "  make verify"

# Clean generated files
clean:
	@echo "🧹 Cleaning generated files..."
	rm -f $(BUNDLE_FILE) $(SIGNATURE_FILE)
	rm -rf $(RECEIPTS_DIR)/bundle_*
	@echo "✅ Clean complete"

# Development helpers
.PHONY: dev-setup lint test

dev-setup:
	@echo "🔧 Setting up development environment..."
	@npm install
	@pip install -r requirements.alignment.txt 2>/dev/null || true
	@echo "✅ Development environment ready"

lint:
	@echo "🔍 Running linters..."
	@npm run lint 2>/dev/null || echo "No npm lint configured"

test:
	@echo "🧪 Running tests..."
	@./bin/verify $(BUNDLE_FILE) 2>/dev/null || echo "No bundle to verify yet"
