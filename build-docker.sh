#!/bin/bash

# Build Docker image for Task Manager MCP
# Usage: ./build-and-push.sh [tag]

set -e

# Default values
IMAGE_NAME="task-manager-mcp"
TAG=${1:-latest}

echo "Building Docker image: ${IMAGE_NAME}:${TAG}"

# Build the image
docker build -t "${IMAGE_NAME}:${TAG}" .

echo "Image built successfully!"
echo ""
echo "Usage with Claude Desktop:"
echo ""
echo "# macOS/Windows:"
echo "claude mcp add task-manager -s user \\"
echo "  --env \"TASK_MANAGER_HOST=host.docker.internal\" \\"
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
echo "# Linux:"
echo "claude mcp add task-manager -s user \\"
echo "  --env \"TASK_MANAGER_HOST=localhost\" \\"
echo "  --env \"TASK_MANAGER_PORT=8080\" \\"
echo "  --env \"TASK_MANAGER_TIMEOUT=30\" \\"
echo "  --env \"USE_MOCK_CLIENT=false\" \\"
echo "  -- docker run -i --rm --network=host \\"
echo "    -e TASK_MANAGER_HOST \\"
echo "    -e TASK_MANAGER_PORT \\"
echo "    -e TASK_MANAGER_TIMEOUT \\"
echo "    -e USE_MOCK_CLIENT \\"
echo "    ${IMAGE_NAME}:${TAG}"
echo ""
echo "# Mock mode (all platforms):"
echo "claude mcp add task-manager-mock -s user \\"
echo "  --env \"USE_MOCK_CLIENT=true\" \\"
echo "  -- docker run -i --rm \\"
echo "    -e USE_MOCK_CLIENT \\"
echo "    ${IMAGE_NAME}:${TAG}"