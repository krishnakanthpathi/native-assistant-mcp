import json
from fastmcp import FastMCP

from .process_start import async_sessions


def register(mcp: FastMCP):
    @mcp.tool()
    def process_read_output(session_id: str) -> str:
        """Read available stdout and stderr from an async process session (non-blocking)."""
        session = async_sessions.get(session_id)
        if not session:
            raise ValueError(f'Process session "{session_id}" not found.')
        
        output = {
            'closed': session['closed'],
            'exitCode': session['exit_code'],
            'stdout': session['stdout'],
            'stderr': session['stderr']
        }
        
        session['stdout'] = ''
        session['stderr'] = ''
        
        return json.dumps(output, indent=2)
