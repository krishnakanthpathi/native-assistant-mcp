import pytest


class TestMail:
    def test_mail_list_unread(self):
        from tools.mac.app_integration.mail import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("mail", {"action": "list-unread"})
        assert len(result) >= 0


class TestCalendar:
    def test_calendar_list_today(self):
        from tools.mac.app_integration.calendar import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("calendar", {"action": "list-today"})
        assert len(result) >= 0


class TestMessages:
    def test_messages_list_recent(self):
        from tools.mac.app_integration.messages import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("messages", {"action": "list-recent"})
        assert len(result) >= 0


class TestSafari:
    def test_safari_get_tabs(self):
        from tools.mac.app_integration.safari import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("safari", {"action": "get-tabs"})
        assert len(result) >= 0


class TestNotes:
    def test_notes_search(self):
        from tools.mac.app_integration.notes import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("notes", {"action": "search", "query": "test"})
        assert len(result) >= 0


class TestTerminal:
    def test_terminal_list_sessions(self):
        from tools.mac.app_integration.terminal import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("terminal", {"action": "list_sessions"})
        assert len(result) >= 0
