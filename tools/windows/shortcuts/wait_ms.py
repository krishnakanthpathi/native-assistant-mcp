import time
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def wait_ms(milliseconds: int) -> str:
        """Pauses execution for specified duration in milliseconds."""
        sec = max(0, milliseconds) / 1000.0
        time.sleep(sec)
        return f"Waited {milliseconds}ms."
