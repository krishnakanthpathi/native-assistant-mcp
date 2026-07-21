import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def media_control(action: str, player: str = 'Music') -> str:
        """Controls playing media tracks (Music/Spotify) on macOS."""
        if action not in ['play', 'pause', 'playpause', 'next', 'previous']:
            raise ValueError("Action must be 'play', 'pause', 'playpause', 'next', or 'previous'")
        if player not in ['Music', 'Spotify']:
            raise ValueError("Player must be 'Music' or 'Spotify'")
        
        script = f'tell application "{player}" to {action}'
        subprocess.run(['osascript', '-e', script], check=True)
        return f'Media action "{action}" sent to "{player}" successfully.'
