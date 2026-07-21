import pytest


class TestGetVolume:
    def test_get_volume_returns_percentage(self):
        from tools.mac.volume.get_volume import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("get_volume", {})
        assert "%" in result
        assert any(char.isdigit() for char in result)
