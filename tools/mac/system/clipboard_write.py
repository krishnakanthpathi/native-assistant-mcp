import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def clipboard_write(content_type: str, value: str) -> str:
        """Write a typed value (string / image / file_urls / rtf) to the system pasteboard."""
        swift_code = '''
import Cocoa
guard CommandLine.arguments.count >= 3 else {
    exit(1)
}
let typeArg = CommandLine.arguments[1]
let val = CommandLine.arguments[2]
let pb = NSPasteboard.general
pb.clearContents()

if typeArg == "image" {
    if let data = Data(base64Encoded: val) {
        pb.setData(data, forType: .png)
    }
} else if typeArg == "file_urls" {
    if let data = val.data(using: .utf8),
       let paths = try? JSONSerialization.jsonObject(with: data, options: []) as? [String] {
        let urls = paths.map { URL(fileURLWithPath: $0) as NSURL }
        pb.writeObjects(urls)
    }
} else if typeArg == "rtf" {
    if let data = Data(base64Encoded: val) {
        pb.setData(data, forType: .rtf)
    }
} else {
    pb.setString(val, forType: .string)
}
print("Clipboard updated.")
'''
        res = subprocess.run(['swift', '-', content_type, value], input=swift_code, capture_output=True, text=True)
        return res.stdout.strip()
