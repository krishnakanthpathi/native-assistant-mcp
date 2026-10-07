import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def wifi_control(action: str) -> str:
        """Controls macOS Wi-Fi power ('on', 'off', 'status')."""
        act = action.lower().strip()
        if act == "on":
            subprocess.run(['networksetup', '-setairportpower', 'en0', 'on'], check=True)
            return "Wi-Fi turned ON."
        elif act == "off":
            subprocess.run(['networksetup', '-setairportpower', 'en0', 'off'], check=True)
            return "Wi-Fi turned OFF."
        elif act == "status":
            res = subprocess.run(['networksetup', '-getairportpower', 'en0'], capture_output=True, text=True, check=True)
            return res.stdout.strip()
        else:
            raise ValueError(f"Unknown Wi-Fi action: '{action}'. Supported: 'on', 'off', 'status'.")
