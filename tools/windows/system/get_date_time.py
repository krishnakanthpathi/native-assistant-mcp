from datetime import datetime
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def get_date_time() -> str:
        """Gets current system date, time, and timezone information."""
        now = datetime.now().astimezone()
        return now.strftime("%Y-%m-%d %H:%M:%S %Z (UTC%z)")
