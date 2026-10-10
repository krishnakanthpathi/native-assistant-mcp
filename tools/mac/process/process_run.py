import subprocess
import json
import os
import signal
from fastmcp import FastMCP

DEFAULT_ALLOWED_PROCESSES = [
    'git', 'rg', 'gh', 'fd', 'python3', 'node', 'npm', 'npx',
    'swift', 'swiftc', 'osascript', 'cupsfilter', 'qlmanage',
    'shortcuts', 'open', 'screencapture', 'cat', 'ls', 'echo', 'ps',
    'lmem', 'zsh', 'bash', 'sh'
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
        import shlex
        args = list(args) if args else []
        if not args and (' ' in command.strip() or '\t' in command.strip()):
            try:
                parts = shlex.split(command.strip())
                if parts:
                    command = parts[0]
                    args = parts[1:]
            except Exception:
                pass

        import shutil
        from pathlib import Path

        check_command_allowed(command)
        
        env = os.environ.copy()
        env['PAGER'] = 'cat'

        home = str(Path.home())
        extra_paths = [
            f"{home}/.local/bin",
            f"{home}/.lightmem/bin",
            "/opt/homebrew/bin",
            "/opt/homebrew/sbin",
            "/usr/local/bin",
            "/Library/Frameworks/Python.framework/Versions/3.14/bin",
            "/Library/Frameworks/Python.framework/Versions/3.12/bin",
        ]
        existing_path = env.get("PATH", "/usr/bin:/bin:/usr/sbin:/sbin")
        env["PATH"] = ":".join(extra_paths) + ":" + existing_path

        cmd_path = shutil.which(command, path=env["PATH"]) or command
        
        res = subprocess.run(
            [cmd_path] + args,
            capture_output=True,
            text=True,
            timeout=timeout_ms / 1000,
            env=env
        )
        
        output = f"Exit Code: {res.returncode}\nSTDOUT:\n{res.stdout[:10000]}\nSTDERR:\n{res.stderr[:10000]}"
        return output
