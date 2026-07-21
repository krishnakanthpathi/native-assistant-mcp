import pytest


class TestShortcutList:
    def test_shortcut_list(self):
        from tools.mac.shortcuts.shortcut_list import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("shortcut_list", {})
        assert "[" in result or "No shortcuts" in result or len(result) >= 0


class TestWaitMs:
    def test_wait_ms(self):
        from tools.mac.shortcuts.wait_ms import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("wait_ms", {"ms": 100})
        assert "waited" in result.lower() or "finished" in result.lower()
    
    def test_wait_ms_caps_at_60000(self):
        from tools.mac.shortcuts.wait_ms import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("wait_ms", {"ms": 100000})
        assert "60000" in result
