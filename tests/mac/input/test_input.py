import pytest


class TestMouseMove:
    def test_mouse_move_validates_coords(self):
        from tools.mac.input.mouse_move import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("mouse_move", {"x": 100, "y": 100})
        assert "moved" in result.lower() or "success" in result.lower()


class TestMouseClick:
    def test_mouse_click_validates_button(self):
        from tools.mac.input.mouse_click import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        with pytest.raises(Exception):
            mcp.call_tool("mouse_click", {"x": 100, "y": 100, "button": "invalid"})


class TestMouseDrag:
    def test_mouse_drag(self):
        from tools.mac.input.mouse_drag import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("mouse_drag", {"from_x": 100, "from_y": 100, "to_x": 200, "to_y": 200})
        assert "dragged" in result.lower() or "success" in result.lower()


class TestKeyPress:
    def test_key_press(self):
        from tools.mac.input.key_press import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("key_press", {"key": "enter"})
        assert "success" in result.lower() or "pressed" in result.lower()


class TestTypeText:
    def test_type_text_requires_text(self):
        from tools.mac.input.type_text import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        with pytest.raises(Exception):
            mcp.call_tool("type_text", {})


class TestMediaControl:
    def test_media_control_validates_action(self):
        from tools.mac.input.media_control import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        with pytest.raises(Exception):
            mcp.call_tool("media_control", {"action": "invalid"})
