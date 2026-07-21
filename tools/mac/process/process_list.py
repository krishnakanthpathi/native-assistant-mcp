import subprocess
import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def process_list() -> str:
        """List running processes on the system (pid, ppid, uid, command). Read-only."""
        res = subprocess.run(['ps', '-ax', '-o', 'pid,ppid,uid,comm'], capture_output=True, text=True)
        lines = res.stdout.strip().split('\n')
        
        results = []
        for line in lines[1:]:
            tokens = line.strip().split()
            if len(tokens) >= 4:
                results.append({
                    'pid': int(tokens[0]),
                    'ppid': int(tokens[1]),
                    'uid': int(tokens[2]),
                    'command': ' '.join(tokens[3:])
                })
        
        return json.dumps(results[:1000], indent=2)
