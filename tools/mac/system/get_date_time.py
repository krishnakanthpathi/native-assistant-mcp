import json
from datetime import datetime, timezone
import sys
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def get_date_time() -> str:
        """Retrieve the current local date, time, and timezone information from the host system."""
        now = datetime.now()
        result = {
            'localTime': str(now),
            'isoString': datetime.now(timezone.utc).isoformat(),
            'timeZone': datetime.now().astimezone().tzinfo.tzname(None) if hasattr(datetime.now().astimezone().tzinfo, 'tzname') else 'UTC',
            'epochMs': int(now.timestamp() * 1000)
        }
        return json.dumps(result, indent=2)
