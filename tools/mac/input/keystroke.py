import subprocess
import time
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def keystroke_action(action: str, text: str = None, key: str = None, modifiers: list = None) -> str:
        """Simulates typing text or pressing specific keyboard shortcut keys on macOS."""
        modifiers = modifiers or []
        
        KEY_CODES = {
            'enter': '36', 'return': '36', 'tab': '48', 'space': '49',
            'escape': '53', 'delete': '51', 'backspace': '51',
            'up': '126', 'down': '125', 'left': '123', 'right': '124'
        }
        
        MODIFIER_MAP = {
            'command': 'command down', 'cmd': 'command down',
            'option': 'option down', 'alt': 'option down',
            'control': 'control down', 'ctrl': 'control down',
            'shift': 'shift down'
        }
        
        if action == 'type':
            if not text:
                raise ValueError("Text parameter is required for typing action")
            
            original_clipboard = ''
            try:
                res = subprocess.run(['pbpaste'], capture_output=True, text=True)
                original_clipboard = res.stdout
            except Exception:
                pass
            
            subprocess.run(['pbcopy'], input=text, text=True, check=True)
            time.sleep(0.05)
            
            script = 'tell application "System Events" to keystroke "v" using command down'
            subprocess.run(['osascript', '-e', script], check=True)
            time.sleep(0.1)
            
            if original_clipboard:
                subprocess.run(['pbcopy'], input=original_clipboard, text=True)
            
            return 'Typed text successfully.'
        
        elif action in ['shortcut', 'press']:
            if not key:
                raise ValueError("Key parameter is required for shortcut/press action")
            
            lower_key = key.lower()
            
            if lower_key in KEY_CODES:
                action_script = f'key code {KEY_CODES[lower_key]}'
            else:
                action_script = f'keystroke "{lower_key[0]}"'
            
            if modifiers:
                applescript_mods = [MODIFIER_MAP.get(m.lower()) for m in modifiers if m.lower() in MODIFIER_MAP]
                if applescript_mods:
                    action_script += f' using {{{", ".join(applescript_mods)}}}'
            
            script = f'tell application "System Events" to {action_script}'
            subprocess.run(['osascript', '-e', script], check=True)
            return 'Shortcut action completed successfully.'
        
        else:
            raise ValueError(f'Unknown action "{action}"')
