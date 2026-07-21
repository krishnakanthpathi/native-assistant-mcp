import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def say_speech(text: str) -> str:
        """Speaks the input text aloud using the macOS native speech synthesizer."""
        if not text:
            raise ValueError("Text parameter is required")
        
        subprocess.run(['say', text], check=True)
        return 'Successfully spoke text aloud.'
