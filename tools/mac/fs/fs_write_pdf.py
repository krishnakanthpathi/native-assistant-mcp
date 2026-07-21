import os
import subprocess
from fastmcp import FastMCP

ALLOWED_ROOTS = ['/Users/krishnakanth']


def validate_path(target_path):
    resolved = os.path.abspath(target_path)
    allowed = any(resolved == root or resolved.startswith(root + os.sep) for root in ALLOWED_ROOTS)
    if not allowed:
        raise ValueError(f"Access denied to path: {target_path}. Only paths under /Users/krishnakanth are allowed.")
    return resolved


def register(mcp: FastMCP):
    @mcp.tool()
    def fs_write_pdf(path: str, text: str, paper_size: str = 'letter') -> str:
        """Render plain text to a PDF (letter / a4 / legal)."""
        if paper_size not in ['letter', 'a4', 'legal']:
            raise ValueError("paper_size must be 'letter', 'a4', or 'legal'")
        
        resolved_pdf = validate_path(path)
        
        temp_txt = os.path.join(os.path.dirname(resolved_pdf), f'temp-{int(os.times().elapsed * 1000)}.txt')
        with open(temp_txt, 'w', encoding='utf8') as f:
            f.write(text)
        
        try:
            subprocess.run([
                'cupsfilter', '-i', 'text/plain',
                '-o', f'media={paper_size}',
                '-o', 'document-format=application/pdf',
                temp_txt
            ], stdout=open(resolved_pdf, 'wb'), check=True)
        finally:
            if os.path.exists(temp_txt):
                os.unlink(temp_txt)
        
        return f'PDF generated successfully at {path}'
