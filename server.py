import sys
from fastmcp import FastMCP


mcp = FastMCP("Native Assistant")


if sys.platform == 'darwin':
    from tools.mac.volume.volume_set import register as reg_vol_set
    from tools.mac.volume.get_volume import register as reg_vol_get
    from tools.mac.active_window.active_window import register as reg_act_win
    
    from tools.mac.apps.list_applications import register as reg_list_apps
    from tools.mac.apps.open_application import register as reg_open_app
    from tools.mac.apps.close_application import register as reg_close_app
    from tools.mac.apps.iphone_mirror import register as reg_iphone_mirror
    
    from tools.mac.system.dark_mode import register as reg_dark_mode
    from tools.mac.system.empty_trash import register as reg_empty_trash
    from tools.mac.system.system_stats import register as reg_sys_stats
    from tools.mac.system.lock_screen import register as reg_lock_screen
    from tools.mac.system.say_speech import register as reg_say_speech
    from tools.mac.system.system_power import register as reg_sys_power
    from tools.mac.system.take_screenshot import register as reg_screenshot
    from tools.mac.system.notify import register as reg_notify
    from tools.mac.system.prompt_user import register as reg_prompt_user
    from tools.mac.system.get_date_time import register as reg_date_time
    from tools.mac.system.clipboard_read import register as reg_clip_read
    from tools.mac.system.clipboard_write import register as reg_clip_write
    
    from tools.mac.input.mouse_move import register as reg_mouse_move
    from tools.mac.input.mouse_click import register as reg_mouse_click
    from tools.mac.input.mouse_drag import register as reg_mouse_drag
    from tools.mac.input.mouse_scroll import register as reg_mouse_scroll
    from tools.mac.input.key_press import register as reg_key_press
    from tools.mac.input.type_text import register as reg_type_text
    from tools.mac.input.keystroke import register as reg_keystroke
    from tools.mac.input.media_control import register as reg_media_control
    
    from tools.mac.fs.fs_read import register as reg_fs_read
    from tools.mac.fs.fs_read_many import register as reg_fs_read_many
    from tools.mac.fs.fs_write import register as reg_fs_write
    from tools.mac.fs.fs_edit import register as reg_fs_edit
    from tools.mac.fs.fs_write_pdf import register as reg_fs_write_pdf
    from tools.mac.fs.fs_list import register as reg_fs_list
    from tools.mac.fs.fs_stat import register as reg_fs_stat
    from tools.mac.fs.fs_copy import register as reg_fs_copy
    from tools.mac.fs.fs_move import register as reg_fs_move
    from tools.mac.fs.fs_make_dir import register as reg_fs_mkdir
    from tools.mac.fs.fs_delete import register as reg_fs_delete
    from tools.mac.fs.fs_watch_once import register as reg_fs_watch
    from tools.mac.fs.fs_xattr_get import register as reg_xattr_get
    from tools.mac.fs.fs_xattr_set import register as reg_xattr_set
    
    from tools.mac.process.process_run import register as reg_proc_run
    from tools.mac.process.process_start import register as reg_proc_start
    from tools.mac.process.process_read_output import register as reg_proc_read
    from tools.mac.process.process_write_input import register as reg_proc_write
    from tools.mac.process.process_terminate import register as reg_proc_term
    from tools.mac.process.process_list import register as reg_proc_list
    from tools.mac.process.process_kill import register as reg_proc_kill
    
    from tools.mac.shortcuts.shortcut_list import register as reg_shortcut_list
    from tools.mac.shortcuts.shortcut_run import register as reg_shortcut_run
    from tools.mac.shortcuts.wait_ms import register as reg_wait_ms
    
    from tools.mac.window.list_apps import register as reg_win_list_apps
    from tools.mac.window.list_windows import register as reg_win_list_windows
    from tools.mac.window.focus_app import register as reg_win_focus_app
    from tools.mac.window.focus_window import register as reg_win_focus_win
    from tools.mac.window.move_window import register as reg_win_move
    from tools.mac.window.resize_window import register as reg_win_resize
    from tools.mac.window.set_space import register as reg_win_set_space
    
    from tools.mac.app_integration.mail import register as reg_mail
    from tools.mac.app_integration.calendar import register as reg_calendar
    from tools.mac.app_integration.messages import register as reg_messages
    from tools.mac.app_integration.safari import register as reg_safari
    from tools.mac.app_integration.notes import register as reg_notes
    from tools.mac.app_integration.terminal import register as reg_terminal
    
    from tools.mac.custom.run_applescript import register as reg_applescript
    
    reg_vol_set(mcp)
    reg_vol_get(mcp)
    reg_act_win(mcp)
    
    reg_list_apps(mcp)
    reg_open_app(mcp)
    reg_close_app(mcp)
    reg_iphone_mirror(mcp)
    
    reg_dark_mode(mcp)
    reg_empty_trash(mcp)
    reg_sys_stats(mcp)
    reg_lock_screen(mcp)
    reg_say_speech(mcp)
    reg_sys_power(mcp)
    reg_screenshot(mcp)
    reg_notify(mcp)
    reg_prompt_user(mcp)
    reg_date_time(mcp)
    reg_clip_read(mcp)
    reg_clip_write(mcp)
    
    reg_mouse_move(mcp)
    reg_mouse_click(mcp)
    reg_mouse_drag(mcp)
    reg_mouse_scroll(mcp)
    reg_key_press(mcp)
    reg_type_text(mcp)
    reg_keystroke(mcp)
    reg_media_control(mcp)
    
    reg_fs_read(mcp)
    reg_fs_read_many(mcp)
    reg_fs_write(mcp)
    reg_fs_edit(mcp)
    reg_fs_write_pdf(mcp)
    reg_fs_list(mcp)
    reg_fs_stat(mcp)
    reg_fs_copy(mcp)
    reg_fs_move(mcp)
    reg_fs_mkdir(mcp)
    reg_fs_delete(mcp)
    reg_fs_watch(mcp)
    reg_xattr_get(mcp)
    reg_xattr_set(mcp)
    
    reg_proc_run(mcp)
    reg_proc_start(mcp)
    reg_proc_read(mcp)
    reg_proc_write(mcp)
    reg_proc_term(mcp)
    reg_proc_list(mcp)
    reg_proc_kill(mcp)
    
    reg_shortcut_list(mcp)
    reg_shortcut_run(mcp)
    reg_wait_ms(mcp)
    
    reg_win_list_apps(mcp)
    reg_win_list_windows(mcp)
    reg_win_focus_app(mcp)
    reg_win_focus_win(mcp)
    reg_win_move(mcp)
    reg_win_resize(mcp)
    reg_win_set_space(mcp)
    
    reg_mail(mcp)
    reg_calendar(mcp)
    reg_messages(mcp)
    reg_safari(mcp)
    reg_notes(mcp)
    reg_terminal(mcp)
    
    reg_applescript(mcp)
    
elif sys.platform == 'win32':
    from tools.windows.active_window.active_window import register as reg_win_act
    from tools.windows.powershell.powershell import register as reg_win_ps
    
    reg_win_act(mcp)
    reg_win_ps(mcp)


if __name__ == "__main__":
    mcp.run()
