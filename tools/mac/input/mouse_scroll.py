import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def mouse_scroll(dx: int, dy: int, unit: str = 'line') -> str:
        """Send a scroll-wheel event in line or pixel units."""
        swift_code = '''
import Cocoa
let dx = Int32(CommandLine.arguments[1]) ?? 0
let dy = Int32(CommandLine.arguments[2]) ?? 0
let unitType = CommandLine.arguments[3]
let units: CGScrollEventUnit = (unitType == "pixel") ? .pixel : .line
let event = CGEvent(scrollWheelEvent2Source: nil, units: units, wheelCount: 2, wheel1: dy, wheel2: dx, wheel3: 0)
event?.post(tap: .cghidEventTap)
'''
        subprocess.run(['swift', '-', str(dx), str(dy), unit], input=swift_code, capture_output=True, text=True, check=True)
        return 'Scrolled successfully.'
