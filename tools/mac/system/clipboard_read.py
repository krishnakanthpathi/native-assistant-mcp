import subprocess
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def clipboard_read(content_type: str = 'string') -> str:
        """Read the system pasteboard as a typed value (string / image / file_urls / rtf)."""
        swift_code = '''
import Cocoa
let typeArg = CommandLine.arguments[1]
let pb = NSPasteboard.general

if typeArg == "image" {
    if let data = pb.data(forType: .png) {
        print(data.base64EncodedString())
    } else if let data = pb.data(forType: .tiff) {
        if let image = NSImage(data: data),
           let tiffData = image.tiffRepresentation,
           let bitmap = NSBitmapImageRep(data: tiffData),
           let pngData = bitmap.representation(using: .png, properties: [:]) {
            print(pngData.base64EncodedString())
        }
    }
} else if typeArg == "file_urls" {
    if let classes = [NSURL.self] as? [AnyClass],
       let urls = pb.readObjects(forClasses: classes, options: nil) as? [URL] {
        let paths = urls.map { $0.path }
        if let jsonData = try? JSONSerialization.data(withJSONObject: paths, options: []),
           let jsonString = String(data: jsonData, encoding: .utf8) {
            print(jsonString)
        }
    }
} else if typeArg == "rtf" {
    if let rtfData = pb.data(forType: .rtf) {
        print(rtfData.base64EncodedString())
    }
} else {
    if let str = pb.string(forType: .string) {
        print(str)
    }
}
'''
        res = subprocess.run(['swift', '-', content_type], input=swift_code, capture_output=True, text=True)
        return res.stdout.strip()
