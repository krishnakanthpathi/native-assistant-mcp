import pytest


class TestProcessRun:
    def test_process_run_ls(self):
        from tools.mac.process.process_run import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("process_run", {"command": "ls", "args": ["/Users/krishnakanth"]})
        assert "Exit Code" in result


class TestProcessList:
    def test_process_list(self):
        from tools.mac.process.process_list import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        result = mcp.call_tool("process_list", {})
        assert "pid" in result.lower() or "[" in result


class TestProcessKill:
    def test_process_kill_refuses_pid_1(self):
        from tools.mac.process.process_kill import register
        from fastmcp import FastMCP
        mcp = FastMCP("test")
        register(mcp)
        with pytest.raises(Exception):
            mcp.call_tool("process_kill", {"pid": 1})
