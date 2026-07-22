import json
import sys
import os
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from datetime import datetime, timezone

sys.path.insert(0, '.')


class MCPHTTPHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[HTTP] {args[0]}")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == '/tools':
            tools_list = [
                {'name': 'volume_set', 'description': 'Set system volume (0-100)'},
                {'name': 'get_volume', 'description': 'Get current system volume'},
                {'name': 'get_active_window', 'description': 'Get current active window'},
                {'name': 'list_applications', 'description': 'List installed applications'},
                {'name': 'open_application', 'description': 'Open an application'},
                {'name': 'close_application', 'description': 'Close an application'},
                {'name': 'iphone_mirror', 'description': 'Launch iPhone Mirroring'},
                {'name': 'set_dark_mode', 'description': 'Toggle dark mode'},
                {'name': 'empty_trash', 'description': 'Empty the Trash'},
                {'name': 'get_system_stats', 'description': 'Get system statistics'},
                {'name': 'lock_screen', 'description': 'Lock the screen'},
                {'name': 'say_speech', 'description': 'Text-to-speech'},
                {'name': 'system_power', 'description': 'Sleep/restart/shutdown'},
                {'name': 'take_screenshot', 'description': 'Take a screenshot'},
                {'name': 'notify', 'description': 'Send notification'},
                {'name': 'prompt_user', 'description': 'Show dialog prompt'},
                {'name': 'get_date_time', 'description': 'Get current date/time'},
                {'name': 'clipboard_read', 'description': 'Read clipboard'},
                {'name': 'clipboard_write', 'description': 'Write to clipboard'},
                {'name': 'mouse_move', 'description': 'Move mouse cursor'},
                {'name': 'mouse_click', 'description': 'Click mouse'},
                {'name': 'mouse_drag', 'description': 'Drag mouse'},
                {'name': 'mouse_scroll', 'description': 'Scroll mouse'},
                {'name': 'key_press', 'description': 'Press a key'},
                {'name': 'type_text', 'description': 'Type text'},
                {'name': 'keystroke_action', 'description': 'Keystroke action'},
                {'name': 'media_control', 'description': 'Control media playback'},
                {'name': 'fs_read', 'description': 'Read a file'},
                {'name': 'fs_list', 'description': 'List directory'},
                {'name': 'fs_stat', 'description': 'Get file stats'},
                {'name': 'fs_write', 'description': 'Write a file'},
                {'name': 'fs_copy', 'description': 'Copy file/dir'},
                {'name': 'fs_move', 'description': 'Move file/dir'},
                {'name': 'fs_make_dir', 'description': 'Create directory'},
                {'name': 'fs_delete', 'description': 'Delete file/dir'},
                {'name': 'process_run', 'description': 'Run a process'},
                {'name': 'process_list', 'description': 'List processes'},
                {'name': 'process_kill', 'description': 'Kill process'},
                {'name': 'shortcut_list', 'description': 'List shortcuts'},
                {'name': 'shortcut_run', 'description': 'Run shortcut'},
                {'name': 'wait_ms', 'description': 'Wait milliseconds'},
                {'name': 'list_apps', 'description': 'List running apps'},
                {'name': 'list_windows', 'description': 'List windows'},
                {'name': 'focus_app', 'description': 'Focus an app'},
                {'name': 'focus_window', 'description': 'Focus window'},
                {'name': 'move_window', 'description': 'Move window'},
                {'name': 'resize_window', 'description': 'Resize window'},
                {'name': 'set_space', 'description': 'Switch space'},
                {'name': 'mail', 'description': 'Mail actions'},
                {'name': 'calendar', 'description': 'Calendar actions'},
                {'name': 'messages', 'description': 'Messages actions'},
                {'name': 'safari', 'description': 'Safari actions'},
                {'name': 'notes', 'description': 'Notes actions'},
                {'name': 'terminal', 'description': 'Terminal actions'},
                {'name': 'run_applescript', 'description': 'Run AppleScript'},
            ]
            self.send_json_response(tools_list)
        
        elif parsed.path == '/health':
            self.send_json_response({'status': 'ok'})
        
        else:
            self.send_error(404, 'Not Found')

    def do_POST(self):
        parsed = urlparse(self.path)
        
        if parsed.path.startswith('/tools/'):
            tool_name = parsed.path[7:]
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            try:
                params = json.loads(body) if body else {}
            except json.JSONDecodeError:
                params = {}
            
            try:
                result = self.execute_tool(tool_name, params)
                self.send_json_response({'status': 'success', 'result': result})
            except Exception as e:
                self.send_json_response({'status': 'error', 'error': str(e)}, status=400)
        
        else:
            self.send_error(404, 'Not Found')

    def execute_tool(self, tool_name, params):
        if tool_name == 'volume_set':
            level = max(0, min(100, int(params.get('level', 50))))
            subprocess.run(['osascript', '-e', f'set volume output volume {level}'], check=True)
            return f'Set volume to {level}%'
        
        elif tool_name == 'get_volume':
            res = subprocess.run(['osascript', '-e', 'output volume of (get volume settings)'], capture_output=True, text=True, check=True)
            return f'Volume: {res.stdout.strip()}%'
        
        elif tool_name == 'get_active_window':
            script = 'tell application "System Events" to get name of first process whose frontmost is true'
            res = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, check=True)
            return f'Active: {res.stdout.strip()}'
        
        elif tool_name == 'list_applications':
            apps = set()
            for d in ['/Applications', '/System/Applications', os.path.expanduser('~/Applications')]:
                if os.path.exists(d):
                    for f in os.listdir(d):
                        if f.endswith('.app'):
                            apps.add(f.replace('.app', ''))
            return sorted(apps)
        
        elif tool_name == 'open_application':
            app = params.get('app', 'Finder')
            subprocess.run(['open', '-a', app], check=True)
            return f'Opened {app}'
        
        elif tool_name == 'close_application':
            app = params.get('app')
            if not app:
                raise ValueError('app is required')
            subprocess.run(['osascript', '-e', f'quit application "{app}"'], check=True)
            return f'Closed {app}'
        
        elif tool_name == 'get_system_stats':
            battery = subprocess.run(['pmset', '-g', 'batt'], capture_output=True, text=True).stdout.strip()
            disk = subprocess.run(['df', '-lh', '/'], capture_output=True, text=True).stdout.strip()
            return {'battery': battery, 'disk': disk}
        
        elif tool_name == 'notify':
            title = params.get('title', 'Test')
            body = params.get('body', 'Test')
            subprocess.run(['osascript', '-e', f'display notification "{body}" with title "{title}"'], check=True)
            return 'Notification sent'
        
        elif tool_name == 'get_date_time':
            now = datetime.now()
            return {
                'localTime': str(now),
                'isoString': datetime.now(timezone.utc).isoformat(),
                'epochMs': int(now.timestamp() * 1000)
            }
        
        elif tool_name == 'say_speech':
            text = params.get('text', 'test')
            subprocess.run(['say', text], check=True)
            return f'Said: {text}'
        
        elif tool_name == 'process_list':
            res = subprocess.run(['ps', '-ax', '-o', 'pid,ppid,uid,comm'], capture_output=True, text=True)
            lines = res.stdout.strip().split('\n')[1:101]
            processes = []
            for line in lines:
                parts = line.split()
                if len(parts) >= 4:
                    processes.append({'pid': int(parts[0]), 'ppid': int(parts[1]), 'uid': int(parts[2]), 'command': ' '.join(parts[3:])})
            return processes
        
        elif tool_name == 'process_run':
            cmd = params.get('command', 'ls')
            args = params.get('args', [])
            res = subprocess.run([cmd] + args, capture_output=True, text=True)
            return {'exitCode': res.returncode, 'stdout': res.stdout[:5000], 'stderr': res.stderr[:5000]}
        
        elif tool_name == 'wait_ms':
            import time
            ms = min(max(params.get('ms', 1000), 0), 60000)
            time.sleep(ms / 1000)
            return f'Waited {ms}ms'
        
        elif tool_name == 'fs_list':
            path = params.get('path', '/Users/krishnakanth')
            entries = []
            for e in os.listdir(path):
                full = os.path.join(path, e)
                entries.append({'name': e, 'kind': 'directory' if os.path.isdir(full) else 'file'})
            return entries
        
        elif tool_name == 'fs_stat':
            path = params.get('path')
            if not path:
                raise ValueError('path is required')
            stat = os.stat(path)
            return {'size': stat.st_size, 'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()}
        
        elif tool_name == 'shortcut_list':
            res = subprocess.run(['shortcuts', 'list'], capture_output=True, text=True)
            return [s for s in res.stdout.strip().split('\n') if s]
        
        elif tool_name == 'run_powershell':
            script = params.get('script')
            if not script:
                raise ValueError('script is required')
            res = subprocess.run(['powershell', '-Command', script], capture_output=True, text=True)
            if res.returncode != 0:
                raise ValueError(res.stderr)
            return res.stdout.strip() or 'Success'
        
        else:
            return f'Tool {tool_name} not implemented in HTTP mode. Use MCP server directly.'

    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, default=str).encode('utf-8'))


def run_server(port=8000):
    server = HTTPServer(('localhost', port), MCPHTTPHandler)
    print(f"\n{'='*60}")
    print(f"Native Assistant MCP HTTP Server")
    print(f"{'='*60}")
    print(f"Server running at: http://localhost:{port}")
    print(f"Frontend: Open frontend/index.html in your browser")
    print(f"API endpoints:")
    print(f"  GET  /tools      - List all tools")
    print(f"  POST /tools/<name> - Execute a tool")
    print(f"  GET  /health     - Health check")
    print(f"{'='*60}\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
