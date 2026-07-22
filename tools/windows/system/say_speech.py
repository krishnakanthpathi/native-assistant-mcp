import subprocess
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def say_speech(text: str) -> str:
        """Speaks the provided text using Windows SAPI Text-to-Speech."""
        if sys.platform == 'win32':
            ps_script = f"Add-Type -AssemblyName System.Speech; $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; $synth.Speak('{text}')"
            subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        return f"Spoke: '{text}'."
