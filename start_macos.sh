python -m scheduler.macos
sleep 2
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.filem.job.plist
launchctl list | grep filem