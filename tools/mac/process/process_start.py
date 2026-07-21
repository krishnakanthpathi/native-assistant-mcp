import subprocess
import os
import time
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
    def process_start(command: str, args: list = None) -> str:
        """Start an allow-listed process asynchronously, returning a session ID."""
        args = args or []
        check_command_allowed(command)
        
        import uuid
        session_id = f'proc-{int(time.time() * 1000)}-{uuid.uuid4().hex[:5]}'
        
        env = os.environ.copy()
        env['PAGER'] = 'cat'
        
        proc = subprocess.Popen(
            [command] + args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        
        async_sessions[session_id] = {
            'process': proc,
            'stdout': '',
            'stderr': '',
            'exit_code': None,
            'closed': False
        }
        
        import threading
        
        def read_output():
            stdout, stderr = proc.communicate()
            async_sessions[session_id]['stdout'] = stdout
            async_sessions[session_id]['stderr'] = stderr
            async_sessions[session_id]['exit_code'] = proc.returncode
            async_sessions[session_id]['closed'] = True
        
        thread = threading.Thread(target=read_output)
        thread.start()
        
        return json.dumps({'sessionId': session_id, 'pid': proc.pid})
