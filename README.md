# Native Assistant MCP

A pure Python FastMCP server providing system automation tools for macOS and Windows.

## Installation

```bash
pip install -r requirements.txt
```

## Running

### MCP Server (stdio mode)
```bash
python server.py
```

### HTTP Server (for web frontend testing)
```bash
python http_server.py
```

Then open `frontend/index.html` in your browser to test tools interactively.

## Running Tests

```bash
pytest tests/ -v
```

## Architecture

The server uses a modular architecture with tools organized by function:

- `tools/mac/` - macOS-specific tools
- `tools/windows/` - Windows-specific tools

Tools are conditionally loaded based on the operating system.

## Tool Categories (macOS - 52+ tools)

### Volume
- `volume_set(level)` - Set system volume (0-100)
- `get_volume()` - Get current system volume

### Active Window
- `get_active_window()` - Get current active window app name

### Apps
- `list_applications()` - List all installed applications
- `open_application(app)` - Launch/focus an application
- `close_application(app)` - Close an application
- `iphone_mirror(action)` - Launch iPhone Mirroring

### System
- `set_dark_mode(enable)` - Toggle dark/light mode
- `empty_trash()` - Empty the Trash
- `get_system_stats()` - Get battery/disk stats
- `lock_screen()` - Lock the screen
- `say_speech(text)` - Text-to-speech
- `system_power(action)` - Sleep/restart/shutdown
- `take_screenshot(target)` - Take screenshot
- `notify(title, body)` - Send notification
- `prompt_user(message)` - Show dialog
- `get_date_time()` - Get current date/time
- `clipboard_read(type)` - Read clipboard
- `clipboard_write(type, value)` - Write to clipboard

### Input
- `mouse_move(x, y)` - Move mouse
- `mouse_click(x, y, button)` - Click mouse
- `mouse_drag(from, to)` - Drag mouse
- `mouse_scroll(dx, dy)` - Scroll
- `key_press(key, modifiers)` - Press key
- `type_text(text)` - Type text
- `keystroke_action(action, text)` - Keystroke action
- `media_control(action, player)` - Media control

### File System
- `fs_read(path)` - Read file
- `fs_read_many(paths)` - Read multiple files
- `fs_write(path, content)` - Write file
- `fs_edit(path, find, replace)` - Edit file
- `fs_write_pdf(path, text)` - Create PDF
- `fs_list(path)` - List directory
- `fs_stat(path)` - Get file stats
- `fs_copy(src, dst)` - Copy file/dir
- `fs_move(src, dst)` - Move file/dir
- `fs_make_dir(path)` - Create directory
- `fs_delete(path)` - Delete file/dir
- `fs_watch_once(path)` - Watch for changes
- `fs_xattr_get(path, name)` - Get extended attr
- `fs_xattr_set(path, name, value)` - Set extended attr

### Process
- `process_run(command, args)` - Run process sync
- `process_start(command, args)` - Start process async
- `process_read_output(session_id)` - Read process output
- `process_write_input(session_id, input)` - Write to process
- `process_terminate(session_id)` - Terminate process
- `process_list()` - List all processes
- `process_kill(pid)` - Kill process

### Shortcuts
- `shortcut_list(folder)` - List shortcuts
- `shortcut_run(name)` - Run shortcut
- `wait_ms(ms)` - Wait milliseconds

### Window
- `list_apps()` - List running apps
- `list_windows()` - List windows
- `focus_app(bundle_id)` - Focus app
- `focus_window(id)` - Focus window
- `move_window(id, x, y)` - Move window
- `resize_window(id, w, h)` - Resize window
- `set_space(index)` - Switch space

### App Integration
- `mail(action, ...)` - Mail.app actions
- `calendar(action, ...)` - Calendar.app actions
- `messages(action, ...)` - Messages.app actions
- `safari(action, ...)` - Safari actions
- `notes(action, ...)` - Notes.app actions
- `terminal(action, ...)` - Terminal/iTerm2 actions

### Custom
- `run_applescript(script)` - Execute AppleScript

## Project Structure

```
native-assistant-mcp/
├── server.py              # MCP entrypoint
├── http_server.py         # HTTP server for frontend testing
├── requirements.txt       # Python dependencies
├── pytest.ini             # Pytest configuration
├── README.md
├── tools/                 # Tool modules
│   ├── mac/              # macOS tools
│   └── windows/          # Windows tools
├── tests/                 # Test files
│   └── mac/              # macOS tool tests
└── frontend/              # Web testing UI
    └── index.html
```
