#!/usr/bin/env python3
"""
Agent Status MCP Server
MCP server for tracking Claude agent execution status

This is the main entry point that imports and runs the MCP server.
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from server import mcp

if __name__ == "__main__":
    mcp.run()