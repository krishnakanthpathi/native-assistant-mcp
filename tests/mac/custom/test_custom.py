import pytest


class TestRunAppleScript:
    def test_run_applescript_simple(self):
        from tools.mac.custom.run_applescript import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("run_applescript", {"script": 'return "hello"'})
        assert "hello" in result.lower() or "success" in result.lower()
    
    def test_run_applescript_requires_script(self):
        from tools.mac.custom.run_applescript import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        with pytest.raises(Exception):
            mcp.call_tool("run_applescript", {})
