# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY task_manager_mcp.py .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash mcp
USER mcp

# Set environment variables with defaults
# Use host.docker.internal to access host machine from container
ENV TASK_MANAGER_HOST=host.docker.internal
ENV TASK_MANAGER_PORT=8080
ENV TASK_MANAGER_TIMEOUT=30
ENV USE_MOCK_CLIENT=false

# Expose port (not strictly necessary for MCP but good practice)
EXPOSE 3000

# Run the MCP server
CMD ["python", "task_manager_mcp.py"]