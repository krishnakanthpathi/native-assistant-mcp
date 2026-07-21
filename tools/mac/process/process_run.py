import subprocess
import json
import os
import signal
from fastmcp import FastMCP

DEFAULT_ALLOWED_PROCESSES = [
    'git', 'rg', 'gh', 'fd', 'python3', 'node', 'npm', 'npx',
    'swift', 'swiftc', 'osascript', 'cupsfilter', 'qlmanage',
    'shortcuts', 'open', 'screencapture', 'cat', 'ls', 'echo', 'ps'
]

ALLOWED_PROCESSES = os.environ.get('MAC_MCP_PROCESS_ALLOW', '').split(':') + DEFAULT_ALLOWED_PROCESSES if os.environ.get('MAC_MCP_PROCESS_ALLOW') else DEFAULT_ALLOWED_PROCESSES

async_sessions = {}


def check_command_allowed(command):
    base_name = command.strip().split()[0] if command.strip() else ''
    simple_name = base_name.split('/')[-1] if '/' in base_name else base_name
    if simple_name not in ALLOWED_PROCESSES and base_name not in ALLOWED_PROCESSES:
        raise ValueError(f'Command "{base_name}" is not in the allow-listed processes.')


def register(mcp: FastMCP):
    @mcp.tool()
    def process_run(command: str, args: list = None, timeout_ms: int = 10000) -> str:
        """Run an allow-listed process synchronously (capped output + timeout)."""
        args = args or []
        check_command_allowed(command)
        
        env = os.environ.copy()
        env['PAGER'] = 'cat'
        
        res = subprocess.run(
            [command] + args,
            capture_output=True,
            text=True,
            timeout=timeout_ms / 1000,
            env=env
        )
        
        output = f"Exit Code: {res.returncode}\nSTDOUT:\n{res.stdout[:10000]}\nSTDERR:\n{res.stderr[:10000]}"
        return output
