from fastmcp import FastMCP

from .process_start import async_sessions


def register(mcp: FastMCP):
    @mcp.tool()
    def process_write_input(session_id: str, input_text: str, close_after: bool = False) -> str:
        """Write string to an active process session's standard input."""
        session = async_sessions.get(session_id)
        if not session:
            raise ValueError(f'Process session "{session_id}" not found.')
        if session['closed']:
            raise ValueError('Process session is already closed.')
        
        session['process'].stdin.write(input_text)
        if close_after:
            session['process'].stdin.close()
        
        return 'Input written successfully to process stdin.'
