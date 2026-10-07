import asyncio
import pytest
from fastmcp import FastMCP

# FastMCP 4.x compatibility bridge for legacy sync test assertions
orig_call_tool = FastMCP.call_tool


def call_tool_sync_compat(self, *args, **kwargs):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        return orig_call_tool(self, *args, **kwargs)

    res = asyncio.run(orig_call_tool(self, *args, **kwargs))
    if getattr(res, "is_error", False):
        error_msg = res.content[0].text if (res.content and hasattr(res.content[0], "text")) else "Tool execution failed"
        raise ValueError(error_msg)
    if getattr(res, "content", None) and hasattr(res.content[0], "text"):
        return res.content[0].text
    return res


FastMCP.call_tool = call_tool_sync_compat
