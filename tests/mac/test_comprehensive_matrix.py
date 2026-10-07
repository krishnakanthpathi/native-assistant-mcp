import asyncio
import json
import os
import shutil
import tempfile
import pytest
import server


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
class TestComprehensiveMatrix:
    async def test_volume_tools(self):
        res = await server.mcp.call_tool("get_volume", {})
        assert not res.is_error
        assert "volume" in res.content[0].text.lower()

    async def test_active_window(self):
        res = await server.mcp.call_tool("get_active_window", {})
        assert not res.is_error

    async def test_apps_list(self):
        res = await server.mcp.call_tool("list_applications", {})
        assert not res.is_error
        assert len(res.content[0].text) > 0

    async def test_system_stats(self):
        res = await server.mcp.call_tool("get_system_stats", {})
        assert not res.is_error
        assert "cpu" in res.content[0].text.lower() or "battery" in res.content[0].text.lower() or "memory" in res.content[0].text.lower()

    async def test_get_date_time(self):
        res = await server.mcp.call_tool("get_date_time", {})
        assert not res.is_error
        assert "localTime" in res.content[0].text or "isoString" in res.content[0].text

    async def test_clipboard_operations(self):
        write_res = await server.mcp.call_tool("clipboard_write", {"content_type": "text", "value": "mcp_test_value"})
        assert not write_res.is_error
        read_res = await server.mcp.call_tool("clipboard_read", {})
        assert not read_res.is_error
        assert "mcp_test_value" in read_res.content[0].text

    async def test_wifi_control_status(self):
        res = await server.mcp.call_tool("wifi_control", {"action": "status"})
        assert not res.is_error
        assert "Wi-Fi" in res.content[0].text or "en0" in res.content[0].text

    async def test_finder_spotlight(self):
        res = await server.mcp.call_tool("spotlight_search", {"query": "Desktop", "limit": 5})
        assert not res.is_error

    async def test_finder_reveal_and_quicklook(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tf:
            tf.write(b"Hello test")
            temp_path = tf.name

        try:
            rev_res = await server.mcp.call_tool("reveal_in_finder", {"path": temp_path})
            assert not rev_res.is_error
            ql_res = await server.mcp.call_tool("quick_look", {"path": temp_path})
            assert not ql_res.is_error
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    async def test_filesystem_lifecycle(self):
        test_dir = tempfile.mkdtemp(prefix="mcp_fs_test_")
        test_file = os.path.join(test_dir, "sample.txt")
        copy_file = os.path.join(test_dir, "sample_copy.txt")

        try:
            # write
            w_res = await server.mcp.call_tool("fs_write", {"path": test_file, "content": "Initial line\nTarget word here"})
            assert not w_res.is_error

            # read
            r_res = await server.mcp.call_tool("fs_read", {"path": test_file})
            assert not r_res.is_error
            assert "Initial line" in r_res.content[0].text

            # edit
            e_res = await server.mcp.call_tool("fs_edit", {"path": test_file, "find": "Target word", "replace": "Replaced word"})
            assert not e_res.is_error

            # list
            l_res = await server.mcp.call_tool("fs_list", {"path": test_dir})
            assert not l_res.is_error
            assert "sample.txt" in l_res.content[0].text

            # stat
            s_res = await server.mcp.call_tool("fs_stat", {"path": test_file})
            assert not s_res.is_error

            # copy
            c_res = await server.mcp.call_tool("fs_copy", {"src": test_file, "dst": copy_file})
            assert not c_res.is_error
            assert os.path.exists(copy_file)

            # delete
            d_res = await server.mcp.call_tool("fs_delete", {"path": copy_file})
            assert not d_res.is_error
            assert not os.path.exists(copy_file)

        finally:
            shutil.rmtree(test_dir, ignore_errors=True)

    async def test_process_run_and_list(self):
        run_res = await server.mcp.call_tool("process_run", {"command": "echo", "args": ["hello_mcp"]})
        assert not run_res.is_error
        assert "hello_mcp" in run_res.content[0].text

        list_res = await server.mcp.call_tool("process_list", {})
        assert not list_res.is_error

    async def test_shortcuts_list_and_wait(self):
        w_res = await server.mcp.call_tool("wait_ms", {"ms": 100})
        assert not w_res.is_error

        s_res = await server.mcp.call_tool("shortcut_list", {})
        assert not s_res.is_error

    async def test_window_management(self):
        apps_res = await server.mcp.call_tool("list_apps", {})
        assert not apps_res.is_error
        wins_res = await server.mcp.call_tool("list_windows", {})
        assert not wins_res.is_error

    async def test_applescript(self):
        as_res = await server.mcp.call_tool("run_applescript", {"script": 'return "applescript_ok"'})
        assert not as_res.is_error
        assert "applescript_ok" in as_res.content[0].text
