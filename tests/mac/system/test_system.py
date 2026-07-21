import pytest


class TestDarkMode:
    def test_set_dark_mode_on(self):
        from tools.mac.system.dark_mode import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("set_dark_mode", {"enable": True})
        assert "success" in result.lower() or "updated" in result.lower()


class TestEmptyTrash:
    def test_empty_trash(self):
        from tools.mac.system.empty_trash import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("empty_trash", {})
        assert "success" in result.lower() or "emptied" in result.lower()


class TestSystemStats:
    def test_get_system_stats(self):
        from tools.mac.system.system_stats import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("get_system_stats", {})
        assert "Battery" in result or "Disk" in result


class TestLockScreen:
    def test_lock_screen(self):
        from tools.mac.system.lock_screen import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("lock_screen", {})
        assert "locked" in result.lower()


class TestSaySpeech:
    def test_say_speech(self):
        from tools.mac.system.say_speech import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("say_speech", {"text": "test"})
        assert "success" in result.lower() or "spoke" in result.lower()


class TestSystemPower:
    def test_system_power_validates_action(self):
        from tools.mac.system.system_power import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        with pytest.raises(Exception):
            mcp.call_tool("system_power", {"action": "invalid"})


class TestNotify:
    def test_notify(self):
        from tools.mac.system.notify import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("notify", {"title": "Test", "body": "Test body"})
        assert "success" in result.lower() or "posted" in result.lower()


class TestGetDateTime:
    def test_get_date_time(self):
        from tools.mac.system.get_date_time import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("get_date_time", {})
        assert "isoString" in result or "localTime" in result
