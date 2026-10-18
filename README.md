# Native Assistant MCP

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![FastMCP](https://img.shields.io/badge/FastMCP-0.1.0%2B-green.svg)](https://github.com/jlowin/fastmcp)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows-lightgrey.svg)](https://apple.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A pure-Python **FastMCP** server providing 70+ native OS capabilities to AI agents on macOS and Windows. Enables autonomous control of windows, spaces, processes, file systems, shortcuts, finder, and input emulation.

---

## ⚡ Features & Capabilities

- **Mission Control Space Management**: Real-time desktop space inspection and sliding navigation using macOS SkyLight C-framework bindings (`CGSCopyManagedDisplaySpaces`).
- **Native Accessibility Window Control**: Precision window discovery, raising, moving, and resizing via CoreGraphics and AXUIElement APIs.
- **Async Process Management**: Start long-running background CLI processes with non-blocking stdout/stderr streaming buffers and interactive stdin pipes.
- **Multimodal Clipboard**: Read and write UTF-8 text, Base64 PNG images, Finder file URL arrays (`Cmd+C`/`Cmd+V`), and rich text (`rtf`).
- **System Automation**: Apple Shortcuts integration, native notifications, volume adjustment, Spotlight search, QuickLook previews, and dark mode toggling.
- **Input Emulation**: Native mouse moves, clicks, drag operations, scroll wheel events, and full UTF-8 Unicode/emoji typing.

---

## 📁 Project Structure

```
native-assistant-mcp/
├── server.py              # FastMCP server entrypoint (platform-conditional loader)
├── requirements.txt       # Core dependencies (fastmcp, watchdog)
├── README.md              # Documentation & tool reference
└── tools/                 # Modular tool implementations
    ├── mac/               # macOS automation modules
    │   ├── active_window/ # Active application & window title inspection
    │   ├── app_integration/ # Calendar, Messages, Safari, Notes, Terminal
    │   ├── apps/          # App listing, opening, closing, iPhone Mirroring
    │   ├── custom/        # Raw AppleScript execution
    │   ├── finder/        # Spotlight search, QuickLook, Finder selection & reveal
    │   ├── fs/            # File I/O, search, PDF rendering, xattr, directory watch
    │   ├── input/         # Mouse, keyboard, scroll, emoji text typing, media control
    │   ├── process/       # Sync/async CLI process execution, streaming, killing
    │   ├── shortcuts/     # Apple Shortcuts runner & listing
    │   ├── system/        # Dark mode, trash, battery/disk telemetry, lock screen
    │   ├── volume/        # Output volume percentage getter & setter
    │   └── window/        # AX window management, list_spaces, set_space
    └── windows/           # Windows automation modules
```

---

## 🚀 Quick Start

### 1. Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/krishnakanthpathi/native-assistant-mcp.git
cd native-assistant-mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> **Note (macOS)**: Mouse movement tools utilize `cliclick`. Install it via Homebrew:
> ```bash
> brew install cliclick
> ```

### 2. Running the Server

```bash
python server.py
```

---

## 🔌 MCP Client Configuration

### Claude Desktop / Antigravity IDE / Cursor

Add this configuration to your client's MCP configuration file (e.g., `~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "native-assistant-mcp": {
      "command": "/Users/YOUR_USERNAME/Projects/native-assistant-mcp/.venv/bin/python",
      "args": [
        "/Users/YOUR_USERNAME/Projects/native-assistant-mcp/server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

---

## 🛠️ Complete Tool Inventory (macOS — 70 Tools)

### 1. Window & Space Management (8 tools)
| Tool | Arguments | Description |
| :--- | :--- | :--- |
| `list_spaces` | _none_ | Lists all Mission Control desktop spaces with IDs, UUIDs, window counts, and active space index via SkyLight C API. |
| `set_space` | `index: int` | Switches to a Mission Control space (1-based index) using dynamic relative navigation. |
| `list_windows` | _none_ | Returns bounds, IDs, and owner application names of all on-screen windows. |
| `list_apps` | _none_ | Lists running GUI applications with PIDs and bundle IDs. |
| `focus_app` | `bundle_id: str, name: str` | Brings target application to the frontmost focus. |
| `focus_window` | `window_id: int` | Raises and focuses a specific window by its window ID. |
| `move_window` | `window_id: int, x: int, y: int` | Repositions a window to `(x, y)` global coordinates via Accessibility API. |
| `resize_window` | `window_id: int, width: int, height: int` | Resizes window dimensions to `(width, height)`. |

### 2. System Telemetry & Control (9 tools)
| Tool | Arguments | Description |
| :--- | :--- | :--- |
| `get_date_time` | _none_ | Current system date, local time, timezone, and epoch milliseconds. |
| `get_system_stats` | _none_ | Battery percentage, charging state, load averages, and root disk usage. |
| `wifi_control` | `action: str, state: str` | Checks Wi-Fi status or toggles Wi-Fi interface power (`on`/`off`). |
| `get_volume` | _none_ | Reads current system output audio volume (0-100%). |
| `volume_set` | `level: float` | Sets master output volume (0-100%). |
| `set_dark_mode` | `enable: bool` | Toggles or sets macOS Dark Mode appearance. |
| `get_active_window` | _none_ | Returns frontmost active application name and window title. |
| `lock_screen` | _none_ | Instantly locks screen / displaysleep. |
| `system_power` | `action: str` | Executes system power action: `sleep`, `restart`, or `shutdown`. |

### 3. Process Management (7 tools)
| Tool | Arguments | Description |
| :--- | :--- | :--- |
| `process_run` | `command: str, args: list, timeout: int` | Synchronously executes a CLI command with stdout/stderr capture. |
| `process_start` | `command: str, args: list` | Launches an asynchronous background process session with streaming buffers. |
| `process_read_output` | `session_id: str` | Non-blocking read of stdout/stderr from an active background session. |
| `process_write_input` | `session_id: str, input_str: str` | Writes input string to an active session's stdin pipe. |
| `process_terminate` | `session_id: str` | Gracefully terminates (SIGTERM → SIGKILL) an active session. |
| `process_list` | _none_ | Enumerates active running processes with PID, PPID, and command path. |
| `process_kill` | `pid: int, signal: int` | Terminates process by PID (PID 1 protected). |

### 4. File System Operations (14 tools)
| Tool | Arguments | Description |
| :--- | :--- | :--- |
| `fs_read` | `path: str, encoding: str` | Reads file content as UTF-8 text or Base64 string. |
| `fs_read_many` | `paths: list` | Batch reads up to 50 files in a single call. |
| `fs_write` | `path: str, content: str` | Writes text or binary content to target path. |
| `fs_edit` | `path: str, find: str, replace: str` | In-place text replacement within a file. |
| `fs_list` | `path: str` | Lists directory contents with sizes, file kinds, and modification dates. |
| `fs_stat` | `path: str` | File metadata, permissions, timestamps, and extended attributes. |
| `fs_copy` | `src: str, dst: str` | Recursive copy of files or directories. |
| `fs_move` | `src: str, dst: str` | Moves or renames files or directories. |
| `fs_make_dir` | `path: str` | Creates directory recursively (`mkdir -p`). |
| `fs_delete` | `path: str, permanent: bool` | Moves file to Trash or deletes permanently. |
| `fs_write_pdf` | `path: str, text: str` | Renders plain text into a PDF document. |
| `fs_watch_once` | `path: str, timeout: int` | Blocks until directory change event or timeout via `watchdog`. |
| `fs_xattr_get` | `path: str, name: str` | Reads specific extended attribute or lists all (`*`). |
| `fs_xattr_set` | `path: str, name: str, value: str` | Sets extended attribute value. |

### 5. Finder & Search (4 tools)
| Tool | Arguments | Description |
| :--- | :--- | :--- |
| `spotlight_search` | `query: str, limit: int` | Searches local filesystem via native macOS `mdfind` index. |
| `get_finder_selection` | _none_ | Returns paths of files currently selected in frontmost Finder window. |
| `reveal_in_finder` | `path: str` | Opens Finder window highlighting the target file path. |
| `quick_look` | `path: str` | Launches macOS QuickLook preview panel for a file. |

### 6. Clipboard, Scripting & Shortcuts (6 tools)
| Tool | Arguments | Description |
| :--- | :--- | :--- |
| `clipboard_read` | `content_type: str` | Reads pasteboard (`string`, `image` base64 PNG, `file_urls` JSON, `rtf`). |
| `clipboard_write` | `content_type: str, value: str` | Writes typed data to macOS pasteboard. |
| `shortcut_list` | `folder: str` | Lists installed Apple Shortcuts (optional folder filter). |
| `shortcut_run` | `name: str, input_path: str, output_path: str` | Executes Apple Shortcut by name with 60s timeout. |
| `wait_ms` | `ms: int` | Pauses execution for N milliseconds (capped at 60,000 ms). |
| `run_applescript` | `script: str` | Executes raw AppleScript code on macOS. |

### 7. Input Emulation (8 tools)
| Tool | Arguments | Description |
| :--- | :--- | :--- |
| `mouse_move` | `x: int, y: int` | Moves cursor to global screen coordinates `(x, y)`. |
| `mouse_click` | `x: int, y: int, button: str, count: int, modifiers: list` | Clicks mouse at coordinates (`left`, `right`, `middle`, double/triple). |
| `mouse_drag` | `from_x: int, from_y: int, to_x: int, to_y: int` | Performs press, drag, and release between coordinates. |
| `mouse_scroll` | `dx: int, dy: int, unit: str` | Sends scroll-wheel deltas in line or pixel units via CGEvent. |
| `key_press` | `key: str, modifiers: list` | Simulates single key press with modifier keys. |
| `type_text` | `text: str` | Pastes Unicode text stream into active field with full emoji/UTF-8 support. |
| `keystroke_action` | `action: str, text: str, key: str, modifiers: list` | Executes typed text or shortcut combination. |
| `media_control` | `action: str, player: str` | Controls playback (`play`, `pause`, `next`, `previous`) in Music or Spotify. |

### 8. App Integrations (9 tools)
| Tool | Arguments | Description |
| :--- | :--- | :--- |
| `list_applications` | _none_ | Lists all installed `.app` application bundles on macOS. |
| `open_application` | `app: str` | Launches or brings an installed application to focus. |
| `close_application` | `app: str` | Gracefully closes an application via AppleScript. |
| `iphone_mirror` | `action: str` | Launches or focuses the macOS iPhone Mirroring app. |
| `terminal` | `action: str, command: str, text: str, target: str` | Opens windows, executes commands, or lists sessions in Terminal/iTerm2. |
| `notes` | `action: str, title: str, body: str, query: str, note_id: str` | Creates, searches, or appends notes in Apple Notes.app. |
| `safari` | `action: str, url: str, script: str` | Opens URLs, lists open tabs, or executes JavaScript in Safari. |
| `calendar` | `action: str, title: str, start_date: str, end_date: str` | Lists today's events or creates new calendar events in Calendar.app. |
| `messages` | `action: str, recipient: str, message: str` | Lists recent chats or sends an iMessage via Messages.app. |

### 9. Desktop Alerts & System Tasks (5 tools)
| Tool | Arguments | Description |
| :--- | :--- | :--- |
| `notify` | `title: str, body: str, subtitle: str` | Displays Notification Center banner. |
| `prompt_user` | `message: str, default_answer: str` | Displays modal text input popup dialog and returns user response. |
| `say_speech` | `text: str` | Text-to-speech voice synthesis via `say`. |
| `take_screenshot` | `target: str, display_id: int, window_id: int` | Captures silent screenshot (`screen`, `window`, or `iphone_mirror`). |
| `empty_trash` | _none_ | Empties macOS Trash folder via Finder. |

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
