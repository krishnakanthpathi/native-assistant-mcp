import subprocess
import json
from fastmcp import FastMCP


def register(mcp: FastMCP):
    @mcp.tool()
    def calendar(action: str, title: str = None, start_date: str = None, end_date: str = None) -> str:
        """Manage Calendar.app events: create calendar events or list events scheduled for today."""
        if action == 'create-event':
            if not title or not start_date or not end_date:
                raise ValueError('title, start_date, and end_date are required to create an event')
            
            script = f'''
tell application "Calendar"
    tell calendar 1
        make new event with properties {{summary:"{title}", start date:date "{start_date}", end date:date "{end_date}"}}
    end tell
end tell
'''
            subprocess.run(['osascript', '-e', script], check=True)
            return f'Event "{title}" created successfully in Calendar.app.'
        
        elif action == 'list-today':
            script = '''
tell application "Calendar"
    set outputText to ""
    try
        set todayStart to (current date)
        set time of todayStart to 0
        set todayEnd to todayStart + 1 * days
        
        tell calendar 1
            set todayEvents to (every event whose start date is greater than or equal to todayStart and start date is less than todayEnd)
            set summaries to summary of todayEvents
            set startDates to start date of todayEvents
            set endDates to end date of todayEvents
            
            set itemCount to count of summaries
            repeat with i from 1 to itemCount
                set outputText to outputText & (item i of summaries) & ";" & (item i of startDates as string) & ";" & (item i of endDates as string) & "\\n"
            end repeat
        end tell
    end try
    return outputText
end tell
'''
            res = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
            if not res.stdout.strip():
                return 'No events scheduled for today.'
            
            events = []
            for line in res.stdout.strip().split('\n'):
                parts = line.split(';')
                if len(parts) >= 3:
                    events.append({'summary': parts[0], 'start': parts[1], 'end': parts[2]})
            return json.dumps(events, indent=2)
