import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def resize_window(window_id: int, width: int, height: int) -> str:
        """Resize a window to (width, height) coordinates via Accessibility API."""
        swift_code = '''
import Cocoa
import ApplicationServices

let targetId = Int32(CommandLine.arguments[1]) ?? 0
let targetW = CGFloat(Double(CommandLine.arguments[2]) ?? 0.0)
let targetH = CGFloat(Double(CommandLine.arguments[3]) ?? 0.0)

let options = CGWindowListOption(arrayLiteral: .excludeDesktopElements, .optionOnScreenOnly)
guard let list = CGWindowListCopyWindowInfo(options, kCGNullWindowID) as? [[String: Any]] else {
    exit(1)
}

var targetPid: pid_t? = nil
var targetTitle: String? = nil
for w in list {
    let winId = w[kCGWindowNumber as String] as? Int32 ?? 0
    if winId == targetId {
        targetPid = w[kCGWindowOwnerPID as String] as? pid_t
        targetTitle = w[kCGWindowName as String] as? String
        break
    }
}

guard let pid = targetPid else {
    print("Window not found")
    exit(1)
}

let axApp = AXUIElementCreateApplication(pid)
var windowList: AnyObject?
let result = AXUIElementCopyAttributeValue(axApp, kAXWindowsAttribute as CFString, &windowList)

if result == .success, let windows = windowList as? [AXUIElement] {
    for w in windows {
        var titleVal: AnyObject?
        AXUIElementCopyAttributeValue(w, kAXTitleAttribute as CFString, &titleVal)
        let title = titleVal as? String ?? ""
        
        if targetTitle != nil && title == targetTitle {
            var size = CGSize(width: targetW, height: targetH)
            if let axSize = AXValueCreate(.cfSize, &size) {
                let err = AXUIElementSetAttributeValue(w, kAXSizeAttribute as CFString, axSize)
                if err == .success {
                    print("Window resized successfully.")
                    exit(0)
                } else {
                    print("Accessibility error setting size: " + String(err.rawValue))
                    exit(1)
                }
            }
        }
    }
}
print("Could not resize window.")
exit(1)
'''
        res = subprocess.run(['swift', '-', str(window_id), str(width), str(height)], input=swift_code, capture_output=True, text=True)
        return res.stdout.strip() or 'Window resized.'
