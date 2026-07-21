import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def focus_window(window_id: int) -> str:
        """Raise and focus a specific window by its window number ID."""
        swift_code = '''
import Cocoa
import ApplicationServices

let targetId = Int32(CommandLine.arguments[1]) ?? 0
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
    print("Window not found in on-screen window list.")
    exit(1)
}

if let app = NSRunningApplication(processIdentifier: pid) {
    app.activate(options: .activateIgnoringOtherApps)
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
            AXUIElementPerformAction(w, kAXRaiseAction as CFString)
            print("Window raised")
            exit(0)
        }
    }
}
print("Activated application holding the window.")
'''
        res = subprocess.run(['swift', '-', str(window_id)], input=swift_code, capture_output=True, text=True)
        return res.stdout.strip() or 'Window focused.'
