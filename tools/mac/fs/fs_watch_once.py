import os
import json
import time
from fastmcp import FastMCP

ALLOWED_ROOTS = ['/Users/krishnakanth']


def validate_path(target_path):
    resolved = os.path.abspath(target_path)
    allowed = any(resolved == root or resolved.startswith(root + os.sep) for root in ALLOWED_ROOTS)
    if not allowed:
        raise ValueError(f"Access denied to path: {target_path}. Only paths under /Users/krishnakanth are allowed.")
    return resolved


def register(mcp: FastMCP):
    @mcp.tool()
    def fs_watch_once(path: str, timeout_ms: int = 5000) -> str:
        """Block until the next change inside a path (or timeout). Returns changed paths."""
        resolved = validate_path(path)
        
        import threading
        
        result = {'done': False, 'output': 'No changes detected within timeout.'}
        
        def watch():
            try:
                from watchdog.observers import Observer
                from watchdog.events import FileSystemEventHandler
                
                class Handler(FileSystemEventHandler):
                    def on_any_event(self, event):
                        if not result['done']:
                            result['done'] = True
                            result['output'] = json.dumps({
                                'eventType': event.event_type,
                                'filename': event.src_path
                            })
                
                observer = Observer()
                observer.schedule(Handler(), resolved, recursive=True)
                observer.start()
                
                start = time.time()
                while not result['done'] and (time.time() - start) * 1000 < timeout_ms:
                    time.sleep(0.1)
                
                observer.stop()
                observer.join()
            except ImportError:
                result['output'] = 'watchdog library not installed'
        
        thread = threading.Thread(target=watch)
        thread.start()
        thread.join(timeout_ms / 1000 + 1)
        
        return result['output']
