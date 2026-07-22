from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def fs_edit(path: str, old_string: str, new_string: str) -> str:
        """Replaces instances of old_string with new_string in target file."""
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if old_string not in content:
            return f"Target string not found in {path}."
        new_content = content.replace(old_string, new_string)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return f"Successfully updated {path}."
