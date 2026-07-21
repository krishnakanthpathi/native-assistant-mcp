import pytest


class TestActiveWindow:
    def test_get_active_window(self):
        from tools.mac.active_window.active_window import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("get_active_window", {})
        assert "active" in result.lower() or "application" in result.lower()
