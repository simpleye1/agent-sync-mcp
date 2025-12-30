#!/bin/bash

# Build Docker image for Agent Sync MCP
# Usage: ./build-and-push.sh [tag]

set -e

# Default values
IMAGE_NAME="agent-sync-mcp"
TAG=${1:-latest}

echo "Building Docker image: ${IMAGE_NAME}:${TAG}"

# Build the image
docker build -t "${IMAGE_NAME}:${TAG}" .

echo "Image built successfully!"
echo ""
echo "Usage with Claude Desktop:"
echo ""
echo "# Production mode:"
echo "claude mcp add agent-sync -s user\\"
echo "  --env \"TASK_MANAGER_HOST=localhost\" \\"
echo "  --env \"TASK_MANAGER_PORT=8080\" \\"
echo "  --env \"TASK_MANAGER_TIMEOUT=30\" \\"
echo "  --env \"USE_MOCK_CLIENT=false\" \\"
echo "  -- docker run -i --rm \\"
echo "    -e TASK_MANAGER_HOST \\"
echo "    -e TASK_MANAGER_PORT \\"
echo "    -e TASK_MANAGER_TIMEOUT \\"
echo "    -e USE_MOCK_CLIENT \\"
echo "    ${IMAGE_NAME}:${TAG}"
echo ""
echo "# Mock mode for testing:"
echo "claude mcp add agent-sync-mock -s user\\"
echo "  --env \"USE_MOCK_CLIENT=true\" \\"
echo "  -- docker run -i --rm \\"
echo "    -e USE_MOCK_CLIENT \\"
echo "    ${IMAGE_NAME}:${TAG}"