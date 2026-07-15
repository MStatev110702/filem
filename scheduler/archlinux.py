from pathlib import Path
import subprocess
from .paths import PROJECT_DIR

def main():
    file_input = f"""[Unit]
Description=Filemanager job

[Service]
WorkingDirectory={PROJECT_DIR}
ExecStart="{str(PROJECT_DIR)}/.venv/bin/python" -m scripts.entry_job

[Install]
WantedBy=default.target"""

    file_name = "filemanager.service"
    systemd_path = Path(f"~/.config/systemd/user").expanduser()
    systemd_path.parent.mkdir(parents=True, exist_ok=True)

    (systemd_path / file_name).write_text(file_input)

    timer_input = """[Unit]
Description=Run Filemanager job every minute

[Timer]
OnBootSec=60s
OnUnitActiveSec=60s

[Install]
WantedBy=timers.target"""

    timer_name = "filemanager.timer"
    (systemd_path / timer_name).write_text(timer_input)
    
    subprocess.run(["systemctl", "--user", "daemon-reload"])
    subprocess.run(["systemctl", "--user", "enable", file_name])
    subprocess.run(["systemctl", "--user", "enable", "--now", timer_name])

if __name__ == "__main__":
    main()