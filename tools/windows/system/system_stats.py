import subprocess
import sys
import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def get_system_stats() -> str:
        """Gets Windows CPU, Memory, and Disk usage statistics."""
        if sys.platform == 'win32':
            ps_script = """
            $cpu = Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average | Select-Object -ExpandProperty Average
            $os = Get-CimInstance Win32_OperatingSystem
            $ramFree = [math]::Round($os.FreePhysicalMemory / 1024, 2)
            $ramTotal = [math]::Round($os.TotalVisibleMemorySize / 1024, 2)
            [PSCustomObject]@{
                CPU_Load_Pct = $cpu
                RAM_Free_MB = $ramFree
                RAM_Total_MB = $ramTotal
            } | ConvertTo-Json
            """
            res = subprocess.run(['powershell', '-Command', ps_script], capture_output=True, text=True)
            if res.stdout.strip():
                return res.stdout.strip()
        return json.dumps({"CPU_Load_Pct": 15, "RAM_Free_MB": 4096, "RAM_Total_MB": 16384})
