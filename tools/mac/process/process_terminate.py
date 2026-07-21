import signal
from fastmcp import FastMCP

from .process_start import async_sessions


def register(mcp: FastMCP):
    @mcp.tool()
    def process_terminate(session_id: str) -> str:
        """Terminate an async process session (sends SIGTERM, then SIGKILL after 1s if needed)."""
        session = async_sessions.get(session_id)
        if not session:
            raise ValueError(f'Process session "{session_id}" not found.')
        
        if not session['closed']:
            session['process'].terminate()
            
            import threading
            def force_kill():
                if not session['closed']:
                    session['process'].kill()
            
            timer = threading.Timer(1.0, force_kill)
            timer.start()
        
        del async_sessions[session_id]
        return f'Process session {session_id} termination request sent.'
