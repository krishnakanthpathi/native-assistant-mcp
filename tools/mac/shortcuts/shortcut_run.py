import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def shortcut_run(name: str, input_path: str = None, output_path: str = None) -> str:
        """Run an Apple Shortcut by name (optional input/output paths). 60 s timeout."""
        cmd = ['shortcuts', 'run', name]
        if input_path:
            cmd.extend(['-i', input_path])
        if output_path:
            cmd.extend(['-o', output_path])
        
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        output = f'Shortcut executed successfully. Output: {res.stdout.strip() or "No output."}'
        if res.stderr.strip():
            output += f' Errors: {res.stderr}'
        
        return output
