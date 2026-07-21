import subprocess
import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def list_windows() -> str:
        """List on-screen windows with title, owner app, pid, bounds, and window layer."""
        swift_code = '''
import Cocoa
let options = CGWindowListOption(arrayLiteral: .excludeDesktopElements, .optionOnScreenOnly)
guard let list = CGWindowListCopyWindowInfo(options, kCGNullWindowID) as? [[String: Any]] else {
    print("[]")
    exit(0)
}
var res: [[String: Any]] = []
for w in list {
    let layer = w[kCGWindowLayer as String] as? Int ?? 0
    if layer > 50 { continue }
    let pid = w[kCGWindowOwnerPID as String] as? Int ?? 0
    let owner = w[kCGWindowOwnerName as String] as? String ?? ""
    let title = w[kCGWindowName as String] as? String ?? ""
    let winId = w[kCGWindowNumber as String] as? Int ?? 0
    let bounds = w[kCGWindowBounds as String] as? [String: Any] ?? [:]
    res.append([
        "id": winId,
        "title": title,
        "owner": owner,
        "pid": pid,
        "layer": layer,
        "bounds": bounds
    ])
}
if let data = try? JSONSerialization.data(withJSONObject: res, options: .prettyPrinted),
   let str = String(data: data, encoding: .utf8) {
    print(str)
}
'''
        res = subprocess.run(['swift', '-'], input=swift_code, capture_output=True, text=True)
        return res.stdout.strip() or '[]'
