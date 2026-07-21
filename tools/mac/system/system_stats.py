import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def get_system_stats() -> str:
        """Retrieves current macOS system statistics (battery, disk space, and simple CPU/memory status)."""
        battery = 'Unknown'
        try:
            res = subprocess.run(['pmset', '-g', 'batt'], capture_output=True, text=True)
            battery = res.stdout.strip() if res.returncode == 0 else 'Unavailable (possibly a desktop Mac)'
        except Exception:
            battery = 'Unavailable (possibly a desktop Mac)'

        disk = 'Unknown'
        try:
            res = subprocess.run(['df', '-lh', '/'], capture_output=True, text=True)
            lines = res.stdout.strip().split('\n')
            if len(lines) > 1:
                disk = lines[1]
        except Exception:
            disk = 'Unavailable'

        return f"System Statistics:\n- Battery status: {battery}\n- Disk status (Root /): {disk}"
