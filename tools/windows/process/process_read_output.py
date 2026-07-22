from fastmcp import FastMCP
from tools.windows.process.process_start import _PROCESS_STORE


def register(mcp: FastMCP):
    @mcp.tool()
    def process_read_output(pid: int) -> str:
        """Reads accumulated output from background process."""
        proc = _PROCESS_STORE.get(pid)
        if not proc:
            return f"Process with PID {pid} not tracked."
        out, err = proc.communicate(timeout=1) if proc.poll() is not None else ("", "")
        return f"Stdout:\n{out}\nStderr:\n{err}"
