import subprocess
import os
from datetime import datetime
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def take_screenshot(target: str = 'screen', display_id: int = None, window_id: int = None) -> str:
        """Capture a screenshot of the full screen, a specific window, or the iPhone Mirroring window."""
        if target not in ['screen', 'window', 'iphone_mirror']:
            raise ValueError("Target must be 'screen', 'window', or 'iphone_mirror'")
        
        target_dir = os.path.abspath('data/screenshots')
        os.makedirs(target_dir, exist_ok=True)
        
        timestamp = int(datetime.now().timestamp() * 1000)
        
        if target == 'window':
            if window_id is None:
                raise ValueError('window_id is required when target is "window"')
            file_path = os.path.join(target_dir, f'window_screenshot_{window_id}_{timestamp}.png')
            subprocess.run(['screencapture', '-x', '-l', str(window_id), file_path], check=True)
        
        elif target == 'iphone_mirror':
            swift_code = '''
import Cocoa
let options = CGWindowListOption(arrayLiteral: .excludeDesktopElements, .optionOnScreenOnly)
guard let list = CGWindowListCopyWindowInfo(options, kCGNullWindowID) as? [[String: Any]] else {
    exit(1)
}
for w in list {
    let owner = w[kCGWindowOwnerName as String] as? String ?? ""
    let winId = w[kCGWindowNumber as String] as? Int32 ?? 0
    if owner.lowercased().contains("iphone mirroring") {
        print(winId)
        exit(0)
    }
}
exit(1)
'''
            res = subprocess.run(['swift', '-'], input=swift_code, capture_output=True, text=True)
            if res.returncode != 0:
                raise ValueError('iPhone Mirroring window not found on screen. Make sure the app is open.')
            
            mirror_window_id = res.stdout.strip()
            file_path = os.path.join(target_dir, f'iphone_mirror_screenshot_{timestamp}.png')
            subprocess.run(['screencapture', '-l', mirror_window_id, file_path], check=True)
        
        else:
            file_path = os.path.join(target_dir, f'screenshot_{timestamp}.png')
            if display_id:
                subprocess.run(['screencapture', '-x', '-D', str(display_id), file_path], check=True)
            else:
                subprocess.run(['screencapture', '-x', file_path], check=True)
        
        return f'Screenshot saved to {file_path}'
