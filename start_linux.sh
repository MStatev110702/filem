python -m scheduler.linux
systemctl --user daemon-reload
systemctl --user enable filem.service
systemctl --user enable --now filem.timer
systemctl --user start filem.service
systemctl --user status filem.service
systemctl --user status filem.timer