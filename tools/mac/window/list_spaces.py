import subprocess
import json
from fastmcp import FastMCP

SWIFT_SPACES_SCRIPT = '''
import Cocoa

typealias CGSConnectionID = UInt
@_silgen_name("CGSMainConnectionID")
func CGSMainConnectionID() -> CGSConnectionID

@_silgen_name("CGSCopyManagedDisplaySpaces")
func CGSCopyManagedDisplaySpaces(_ cid: CGSConnectionID) -> CFArray?

let cid = CGSMainConnectionID()
guard let displays = CGSCopyManagedDisplaySpaces(cid) as? [[String: Any]] else {
    print("{}")
    exit(0)
}

var allDisplays: [[String: Any]] = []
var activeSpaceIndex = 1

for (dispIdx, d) in displays.enumerated() {
    let curSpace = d["Current Space"] as? [String: Any] ?? [:]
    let curUuid = curSpace["uuid"] as? String ?? ""
    let rawSpaces = d["Spaces"] as? [[String: Any]] ?? []
    
    var spaceList: [[String: Any]] = []
    for (i, s) in rawSpaces.enumerated() {
        let uuid = s["uuid"] as? String ?? ""
        let isCur = (uuid == curUuid)
        let idx = i + 1
        if isCur {
            activeSpaceIndex = idx
        }
        spaceList.append([
            "index": idx,
            "id": s["ManagedSpaceID"] ?? 0,
            "uuid": uuid,
            "type": (s["type"] as? Int ?? 0) == 0 ? "desktop" : "fullscreen_app",
            "is_current": isCur
        ])
    }
    
    allDisplays.append([
        "display": d["Display Identifier"] ?? "Display \(dispIdx + 1)",
        "current_space_uuid": curUuid,
        "current_space_index": activeSpaceIndex,
        "spaces": spaceList
    ])
}

let result: [String: Any] = [
    "current_space_index": activeSpaceIndex,
    "total_spaces": allDisplays.reduce(0) { $0 + (($1["spaces"] as? [Any])?.count ?? 0) },
    "displays": allDisplays
]

if let data = try? JSONSerialization.data(withJSONObject: result, options: .prettyPrinted),
   let str = String(data: data, encoding: .utf8) {
    print(str)
}
'''


def get_spaces_info() -> str:
    try:
        res = subprocess.run(['swift', '-'], input=SWIFT_SPACES_SCRIPT, capture_output=True, text=True, check=True)
        return res.stdout.strip() or "{}"
    except Exception as e:
        return json.dumps({'error': str(e), 'message': 'Failed to retrieve spaces via SkyLight.'}, indent=2)


def register(mcp: FastMCP):
    @mcp.tool()
    def list_spaces() -> str:
        """List all macOS Mission Control spaces, displays, their indices, IDs, and the currently active space."""
        return get_spaces_info()

