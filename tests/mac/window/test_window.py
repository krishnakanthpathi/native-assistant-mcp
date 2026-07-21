import pytest


class TestListApps:
    def test_list_apps(self):
        from tools.mac.window.list_apps import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("list_apps", {})
        assert "[" in result or "No running" in result or "bundleId" in result


class TestListWindows:
    def test_list_windows(self):
        from tools.mac.window.list_windows import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("list_windows", {})
        assert "[" in result or "id" in result.lower()


class TestFocusApp:
    def test_focus_app_requires_bundle_or_name(self):
        from tools.mac.window.focus_app import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        with pytest.raises(Exception):
            mcp.call_tool("focus_app", {})


class TestSetSpace:
    def test_set_space_validates_index(self):
        from tools.mac.window.set_space import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        with pytest.raises(Exception):
            mcp.call_tool("set_space", {"index": 15})
