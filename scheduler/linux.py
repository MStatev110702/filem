from pathlib import Path
from .paths import PROJECT_DIR

def main():
    file_input = f"""[Unit]
Description=Filem job

[Service]
WorkingDirectory={PROJECT_DIR}
ExecStart="{str(PROJECT_DIR)}/.venv/bin/python" -m scripts.entry_job

[Install]
WantedBy=default.target"""

    systemd_path = Path(f"~/.config/systemd/user").expanduser()
    systemd_path.parent.mkdir(parents=True, exist_ok=True)

    (systemd_path / "filem.service").write_text(file_input)

    timer_input = """[Unit]
Description=Run Filem job every minute

[Timer]
OnBootSec=60s
OnUnitActiveSec=60s

[Install]
WantedBy=timers.target"""

    (systemd_path / "filem.timer").write_text(timer_input)

if __name__ == "__main__":
    main()