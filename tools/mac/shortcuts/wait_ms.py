import time
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def wait_ms(ms: int) -> str:
        """Sleep/wait for N milliseconds (maximum 60000 ms)."""
        delay = min(max(ms, 0), 60000)
        time.sleep(delay / 1000)
        return f'Finished waiting for {delay} ms.'
