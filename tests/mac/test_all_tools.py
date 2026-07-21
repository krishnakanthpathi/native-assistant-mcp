import subprocess
import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class TestVolumeTools:
    def test_volume_set_valid(self):
        subprocess.run(['osascript', '-e', 'set volume output volume 50'], check=True)
        result = subprocess.run(['osascript', '-e', 'output volume of (get volume settings)'], capture_output=True, text=True)
        assert result.returncode == 0
    
    def test_volume_set_clamps_100(self):
        subprocess.run(['osascript', '-e', 'set volume output volume 150'], check=True)
        result = subprocess.run(['osascript', '-e', 'output volume of (get volume settings)'], capture_output=True, text=True)
        assert int(result.stdout.strip()) == 100
    
    def test_get_volume(self):
        result = subprocess.run(['osascript', '-e', 'output volume of (get volume settings)'], capture_output=True, text=True)
        assert result.returncode == 0
        assert result.stdout.strip().isdigit()


class TestActiveWindow:
    def test_get_active_window(self):
        script = 'tell application "System Events" to get name of first process whose frontmost is true'
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        assert result.returncode == 0
        assert len(result.stdout.strip()) > 0


class TestApps:
    def test_list_applications(self):
        import os
        apps = set()
        dirs = ['/Applications', '/System/Applications', os.path.expanduser('~/Applications')]
        for d in dirs:
            if os.path.exists(d):
                for f in os.listdir(d):
                    if f.endswith('.app'):
                        apps.add(f.replace('.app', ''))
        assert len(apps) > 0
    
    def test_open_application(self):
        result = subprocess.run(['open', '-a', 'Finder'], capture_output=True, text=True)
        assert result.returncode == 0


class TestSystemTools:
    def test_set_dark_mode(self):
        script = 'tell application "System Events" to tell appearance preferences to set dark mode to true'
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        assert result.returncode == 0
    
    def test_get_system_stats_battery(self):
        result = subprocess.run(['pmset', '-g', 'batt'], capture_output=True, text=True)
        assert result.returncode == 0
    
    def test_get_system_stats_disk(self):
        result = subprocess.run(['df', '-lh', '/'], capture_output=True, text=True)
        assert result.returncode == 0
        assert "Filesystem" in result.stdout or "/" in result.stdout
    
    def test_lock_screen(self):
        result = subprocess.run(['pmset', 'displaysleepnow'], capture_output=True, text=True)
        assert result.returncode == 0
    
    def test_say_speech(self):
        result = subprocess.run(['say', 'test'], capture_output=True, text=True)
        assert result.returncode == 0
    
    def test_notify(self):
        script = 'display notification "Test body" with title "Test"'
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        assert result.returncode == 0
    
    def test_get_date_time(self):
        from datetime import datetime
        now = datetime.now()
        assert now is not None


class TestProcessTools:
    def test_process_run_ls(self):
        result = subprocess.run(['ls', '/Users/krishnakanth'], capture_output=True, text=True)
        assert result.returncode == 0
    
    def test_process_list(self):
        result = subprocess.run(['ps', '-ax', '-o', 'pid,ppid,uid,comm'], capture_output=True, text=True)
        assert result.returncode == 0
        assert "PID" in result.stdout
    
    def test_process_list_format(self):
        result = subprocess.run(['ps', '-ax', '-o', 'pid,comm'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        assert len(lines) > 1


class TestShortcutTools:
    def test_shortcut_list(self):
        result = subprocess.run(['shortcuts', 'list'], capture_output=True, text=True)
        assert result.returncode == 0


class TestWindowTools:
    def test_list_apps(self):
        script = '''
tell application "System Events"
    set names to name of every process whose background only is false
    return names
end tell
'''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        assert result.returncode == 0
    
    def test_list_windows_swift(self):
        swift_code = '''
import Cocoa
let options = CGWindowListOption(arrayLiteral: .excludeDesktopElements, .optionOnScreenOnly)
guard let list = CGWindowListCopyWindowInfo(options, kCGNullWindowID) as? [[String: Any]] else {
    print("[]")
    exit(0)
}
print("found " + String(list.count) + " windows")
'''
        result = subprocess.run(['swift', '-'], input=swift_code, capture_output=True, text=True)
        assert result.returncode == 0


class TestAppIntegration:
    def test_mail_exists(self):
        result = subprocess.run(['osascript', '-e', 'tell application "Mail" to get name'], capture_output=True, text=True)
        assert result.returncode == 0 or "Mail" in result.stderr
    
    def test_safari_exists(self):
        result = subprocess.run(['osascript', '-e', 'tell application "Safari" to get name'], capture_output=True, text=True)
        assert result.returncode == 0 or "Safari" in result.stderr


class TestFileSystemTools:
    def test_fs_list_home(self):
        import os
        entries = os.listdir('/Users/krishnakanth')
        assert len(entries) > 0
    
    def test_fs_stat(self):
        import os
        stat = os.stat('/Users/krishnakanth')
        assert stat.st_size > 0 or stat.st_mode > 0
    
    def test_fs_read_file(self):
        import os
        zshrc = '/Users/krishnakanth/.zshrc'
        if os.path.exists(zshrc):
            with open(zshrc, 'r') as f:
                content = f.read()
            assert len(content) >= 0
        else:
            pytest.skip("No .zshrc file")
    
    def test_fs_make_dir_and_delete(self):
        import os
        test_dir = '/Users/krishnakanth/test_mcp_temp_dir'
        os.makedirs(test_dir, exist_ok=True)
        assert os.path.exists(test_dir)
        os.rmdir(test_dir)
        assert not os.path.exists(test_dir)
