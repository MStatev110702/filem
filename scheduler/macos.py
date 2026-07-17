from pathlib import Path
from .paths import PROJECT_DIR

def main():

    file_input = f"""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">

<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.filem.job</string>
    <key>RunAtLoad</key>
    <true/>
    <key>ProgramArguments</key>
    <array>
        <string>{str(PROJECT_DIR)}/.venv/bin/python</string>
        <string>-m</string>
        <string>scripts.entry_job</string>
    </array>

    <key>WorkingDirectory</key>
    <string>{PROJECT_DIR}</string>

    <key>StartInterval</key>
    <integer>60</integer>

    <key>StandardOutPath</key>
    <string>/tmp/filem_job.log</string>

    <key>StandardErrorPath</key>
    <string>/tmp/filem_job_error.log</string>

</dict>
</plist>"""

    file_path = Path("~/Library/LaunchAgents/com.filem.job.plist").expanduser()

    file_path.write_text(file_input)

if __name__ == "__main__":
    main()