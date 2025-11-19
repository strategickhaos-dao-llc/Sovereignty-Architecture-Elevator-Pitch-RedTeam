.PHONY: help dev start-ngrok destroy clean build test lint docker-up docker-down

help: ## Show this help message
	@echo "🏛️  Sovereignty Architecture - Make Commands"
	@echo "================================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

dev: ## Start local development (event-gateway + ngrok)
	@echo "🚀 Starting sovereign dev environment..."
	@docker-compose up -d postgres redis qdrant
	@npm run dev &
	@./start-ngrok.sh

start-ngrok: ## Start ngrok tunnels with auto-replay
	@./start-ngrok.sh

build: ## Build TypeScript project
	@echo "🔨 Building TypeScript..."
	@npm run build

test: ## Run tests (if they exist)
	@echo "🧪 Running tests..."
	@npm test || echo "⚠️  No tests configured"

lint: ## Run linter
	@echo "🔍 Linting code..."
	@npm run lint

docker-up: ## Start all Docker services
	@echo "🐳 Starting Docker stack..."
	@docker-compose up -d

docker-down: ## Stop all Docker services
	@echo "🛑 Stopping Docker stack..."
	@docker-compose down

destroy: ## Nuclear option - nuke everything and start fresh (chaos mode)
	@echo "💥 DESTROY MODE: Nuking all services and state..."
	@echo "   This will remove all containers, volumes, and ngrok state"
	@read -p "   Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@echo "🗑️  Stopping and removing Docker containers..."
	@docker-compose down -v --remove-orphans || true
	@echo "🔪 Killing ngrok processes..."
	@pkill -f ngrok || true
	@echo "🧹 Cleaning ngrok state..."
	@rm -rf .ngrok2/ || true
	@rm -f /tmp/ngrok.log || true
	@echo "🧼 Cleaning build artifacts..."
	@rm -rf dist/ node_modules/.cache || true
	@echo "✅ Destruction complete! Ready for fresh start."
	@echo "   Run 'make dev' to rebuild from scratch"

clean: ## Clean build artifacts and caches
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf dist/ node_modules/.cache
	@echo "✅ Clean complete"

install: ## Install dependencies
	@echo "📦 Installing dependencies..."
	@npm install

setup: install ## Setup project (install + build)
	@echo "🔧 Setting up project..."
	@$(MAKE) build
	@echo "✅ Setup complete! Run 'make dev' to start development"

.DEFAULT_GOAL := help
