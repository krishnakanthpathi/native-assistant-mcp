import os
import signal
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def process_kill(pid: int, sig: str = 'SIGTERM') -> str:
        """Send a signal to kill a process PID (refuses PID 1 or cross-user kills by default)."""
        if pid == 1:
            raise ValueError('Permission denied: cannot kill PID 1.')
        
        sig_value = getattr(signal, sig, signal.SIGTERM)
        os.kill(pid, sig_value)
        return f'Signal {sig} sent to PID {pid} successfully.'
