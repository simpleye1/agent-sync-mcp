.PHONY: help generate clean test check-tools install-tools

# Configuration
SWAGGER_FILE := docs/swagger.yaml
GENERATED_DIR := src/clients/generated
CLIENT_NAME := _client

help:
	@echo "Available targets:"
	@echo "  generate      - Generate Python client from OpenAPI spec"
	@echo "  clean         - Remove generated client"
	@echo "  regenerate    - Clean and regenerate client"
	@echo "  test          - Run tests"
	@echo "  check-tools   - Check if required CLI tools are installed"
	@echo "  install-tools - Install required CLI tools"

check-tools:
	@echo "Checking required tools..."
	@command -v openapi-python-client >/dev/null 2>&1 || { \
		echo "❌ openapi-python-client not found"; \
		echo "   Run 'make install-tools' to install"; \
		exit 1; \
	}
	@echo "✅ openapi-python-client is installed"
	@openapi-python-client --version

install-tools:
	@echo "Installing openapi-python-client..."
	pip install openapi-python-client
	@echo "✅ Installation complete"

clean:
	@echo "Cleaning generated client..."
	@rm -rf $(GENERATED_DIR)/$(CLIENT_NAME)
	@rm -rf $(GENERATED_DIR)/README.md
	@rm -rf $(GENERATED_DIR)/pyproject.toml
	@rm -rf $(GENERATED_DIR)/.ruff_cache
	@echo "✅ Clean complete"

generate: check-tools
	@echo "Generating Python client from $(SWAGGER_FILE)..."
	@mkdir -p $(GENERATED_DIR)
	openapi-python-client generate --path $(SWAGGER_FILE) --output-path $(GENERATED_DIR) --overwrite
	@echo "✅ Client generated at $(GENERATED_DIR)"

regenerate: clean generate
	@echo "✅ Regeneration complete"

test:
	@echo "Running tests..."
	python tests/simple_test.py
	python tests/test_generated_client.py
	@echo "✅ Tests complete"
