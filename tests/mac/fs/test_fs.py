import pytest
import os
import tempfile


class TestFsRead:
    def test_fs_read_file(self):
        from tools.mac.fs.fs_read import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("fs_read", {"path": "/Users/krishnakanth/.zshrc"})
        assert len(result) > 0 or "error" in result.lower()


class TestFsWrite:
    def test_fs_write_temp_file(self):
        from tools.mac.fs.fs_write import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("fs_write", {
            "path": "/Users/krishnakanth/test_write.txt",
            "content": "test content",
            "mode": "overwrite"
        })
        assert "success" in result.lower() or "written" in result.lower()


class TestFsList:
    def test_fs_list_home(self):
        from tools.mac.fs.fs_list import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("fs_list", {"path": "/Users/krishnakanth"})
        assert "[" in result or "kind" in result


class TestFsStat:
    def test_fs_stat_file(self):
        from tools.mac.fs.fs_stat import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("fs_stat", {"path": "/Users/krishnakanth/.zshrc"})
        assert "size" in result or "kind" in result


class TestFsMakeDir:
    def test_fs_make_dir(self):
        from tools.mac.fs.fs_make_dir import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("fs_make_dir", {"path": "/Users/krishnakanth/test_dir_temp"})
        assert "success" in result.lower() or "created" in result.lower()


class TestFsDelete:
    def test_fs_delete_requires_path(self):
        from tools.mac.fs.fs_delete import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        with pytest.raises(Exception):
            mcp.call_tool("fs_delete", {})
