from fastmcp import FastMCP
from tools.windows.process.process_start import _PROCESS_STORE


def register(mcp: FastMCP):
    @mcp.tool()
    def process_write_input(pid: int, input_text: str) -> str:
        """Writes stdin input to background process."""
        proc = _PROCESS_STORE.get(pid)
        if not proc or proc.poll() is not None:
            return f"Process {pid} is not active."
        if proc.stdin:
            proc.stdin.write(input_text + "\n")
            proc.stdin.flush()
            return f"Wrote input to process {pid}."
        return f"Process {pid} stdin not available."
