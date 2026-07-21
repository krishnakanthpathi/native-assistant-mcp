import pytest
import subprocess
import sys


class TestVolumeSet:
    def test_volume_set_valid(self):
        from tools.mac.volume.volume_set import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("volume_set", {"level": 50})
        assert "50" in result or "success" in result.lower()
    
    def test_volume_set_clamps_high(self):
        from tools.mac.volume.volume_set import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("volume_set", {"level": 150})
        assert "100" in result or "success" in result.lower()
    
    def test_volume_set_clamps_low(self):
        from tools.mac.volume.volume_set import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("volume_set", {"level": -10})
        assert "0" in result or "success" in result.lower()
