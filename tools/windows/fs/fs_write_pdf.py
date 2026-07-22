import os
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def fs_write_pdf(path: str, text: str) -> str:
        """Writes plain text content to a basic formatted PDF file on Windows."""
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        # Standard PDF simple text generator snippet
        header = "%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj 3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<</Font<</F1 4 0 R>>>>/Contents 5 0 R>>endobj 4 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj\n"
        escaped_text = text.replace('(', '\\(').replace(')', '\\)')
        content_stream = f"BT /F1 12 Tf 50 750 Td ({escaped_text}) Tj ET"
        stream_obj = f"5 0 obj<</Length {len(content_stream)}>>stream\n{content_stream}\nendstream\nendobj\n"
        xref = f"xref\n0 6\n0000000000 65535 f \n0000000010 00000 n \n0000000060 00000 n \n0000000115 00000 n \n0000000222 00000 n \n0000000299 00000 n \ntrailer<</Size 6/Root 1 0 R>>\nstartxref\n{len(header) + len(stream_obj)}\n%%EOF"
        
        with open(path, 'wb') as f:
            f.write((header + stream_obj + xref).encode('latin-1'))
        return f"PDF successfully written to {path}."
