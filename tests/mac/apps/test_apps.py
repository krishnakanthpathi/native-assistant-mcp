import pytest


class TestListApplications:
    def test_list_applications_returns_list(self):
        from tools.mac.apps.list_applications import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("list_applications", {})
        assert "Safari" in result or "Finder" in result or "Applications" in result


class TestOpenApplication:
    def test_open_finder(self):
        from tools.mac.apps.open_application import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("open_application", {"app": "Finder"})
        assert "success" in result.lower() or "opened" in result.lower()


class TestCloseApplication:
    def test_close_application_requires_app(self):
        from tools.mac.apps.close_application import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        with pytest.raises(Exception):
            mcp.call_tool("close_application", {})


class TestIphoneMirror:
    def test_iphone_mirror_launch(self):
        from tools.mac.apps.iphone_mirror import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("iphone_mirror", {"action": "launch"})
        assert "activated" in result.lower() or "success" in result.lower()
