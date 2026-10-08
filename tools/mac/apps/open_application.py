import os
import subprocess
from fastmcp import FastMCP

ALIASES = {
    "chrome": "Google Chrome",
    "crom": "Google Chrome",
    "crome": "Google Chrome",
    "gogol chrome": "Google Chrome",
    "google chrome": "Google Chrome",
    "code": "Visual Studio Code",
    "vscode": "Visual Studio Code",
    "sublime": "Sublime Text",
    "word": "Microsoft Word",
    "excel": "Microsoft Excel",
    "powerpoint": "Microsoft PowerPoint",
    "terminal": "Terminal",
    "iterm": "iTerm",
    "notes": "Notes",
    "music": "Music",
    "mail": "Mail",
    "messages": "Messages",
    "safari": "Safari",
    "settings": "System Settings",
    "system settings": "System Settings",
    "calculator": "Calculator",
    "calendar": "Calendar",
}


def resolve_application(app_name: str) -> str:
    """Resolves an app name or alias to an installed macOS application path or name."""
    if not app_name:
        return app_name

    # Check if exact path or name exists
    if os.path.exists(app_name):
        return app_name

    cleaned = app_name.lower().strip().rstrip(".app")
    if cleaned in ALIASES:
        target = ALIASES[cleaned]
    else:
        target = app_name

    # Try direct open test without failing
    res = subprocess.run(["open", "-a", target], capture_output=True, text=True)
    if res.returncode == 0:
        return target

    # Search standard application directories
    search_dirs = [
        "/Applications",
        "/System/Applications",
        "/System/Applications/Utilities",
        os.path.expanduser("~/Applications"),
    ]
    for d in search_dirs:
        if not os.path.exists(d):
            continue
        try:
            for item in os.listdir(d):
                if item.endswith(".app"):
                    stem = item[:-4].lower()
                    if cleaned == stem or cleaned in stem or stem in cleaned:
                        return os.path.join(d, item)
        except Exception:
            continue

    return target


def register(mcp: FastMCP):
    @mcp.tool()
    def open_application(app: str) -> str:
        """Launches or brings to focus a GUI application installed on macOS."""
        if not app:
            raise ValueError("App name is required")

        resolved = resolve_application(app)
        res = subprocess.run(["open", "-a", resolved], capture_output=True, text=True)
        if res.returncode != 0:
            # Fallback to direct path open if resolved is a path
            if os.path.exists(resolved):
                subprocess.run(["open", resolved], check=True)
            else:
                raise RuntimeError(res.stderr.strip() or f"Unable to find application named '{app}'")

        display_name = os.path.basename(resolved).replace(".app", "")
        return f'Application "{display_name}" opened successfully.'

