# FiLem

An open-source, cross-platform file management tool that automates file organization by moving, copying, or deleting files and directories whenever they match user defined conditions.

# Motivation

I'm not great at keeping my storage organized.

My desktop usually ends up covered with files I haven't touched in months, my Downloads folder slowly fills with ZIP archives and installers, and I only remember to empty the Recycle Bin when it starts complaining about running out of space.

Especially after game modding sessions. If you've ever managed multiple modpacks of one game that require different versions of the same mods, you know how easy it is to end up downloading the same file two or three times.

Once I started using Windows, Linux, and macOS regularly, I realized I had the same problem on three different systems.

I wanted something that could clean up after me automatically. Instead of manually organizing files every few weeks, I wanted to define a few simple rules for example, move certain files or delete temporary files after a while and let the application take care of the rest.

However most tools I found were either limited to one operating system or had some paid subscription models to use all features

So I decided to build one myself. That way I can use one free tool for all of my devices.

# Quick Start

## Installation

This assumes that you already have python version 3.14 installed.

### MacOS/Linux

```bash
git clone https://github.com/MStatev110702/filem.git
cd filem
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows

#### Powershell

```powershell
git clone https://github.com/MStatev110702/filem.git
cd filem
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### Cmd

```cmd
git clone https://github.com/MStatev110702/filem.git
cd filem
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

In case you lack privileges to execute the .sh files execute this command:

```bash
chmod +x main.sh
chmod +x start_archlinux.sh
chmod +x stop_archlinux.sh
chmod +x start_macos.sh
chmod +x stop_macos.sh
```

Start the gui by using the following command

```bash
sh main.sh
```

or

```bash
python -m src.main
```

## How to use it

Once you're in the GUI, use the **Create** button to add an entry.

After creating an entry, it will appear in the grid on the main window. From there, you can use the **Edit** button to modify its configuration or the **Delete** button to remove it.

## Automation setup

### Windows

1. Run `windows.bat` as an administrator
2. You should see the message: `"Task successfully created!"`
3. Press `Windows + R`
4. Type `taskschd.msc` and press **Enter**
5. Select **Task Scheduler Library**
6. There should be an entry named **Filem job** that runs every 60 seconds
7. You can `right-click` it and edit it to your liking
8. To turn it off `right-click` the task and select **Disable**
9. To turn it back on just `right-click` the task and select **enable**

#### Troubleshooting: Invalid Argument Error

Sometimes you may encounter the following error:

```
An error has occurred for task Filem job. Error message: One or more of the specified arguments are not valid.
```

In this case, the **user** account configured to run the task is either not an administrator or does not have sufficient privileges.

1. Go into the **General** tab
2. Click **Change User or Group...**
3. Click **Advanced**
4. Click **Find Now**
5. At the bottom, you will see the search results. Select either an **administrator** account or **SYSTEM**
6. Click OK and try saving the task again

### MacOS

1. Run the agent setup script

```bash
sh start_macos.sh
```

You should get an output similar to this:

```bash
87944   0       com.filem.job
```

2. This creates the launch agent `com.filem.job.plist` in `~/Library/LaunchAgents` (default interval is 60 seconds)
3. In case you want to change something in the agent refer to the docs [launchd.info](https://www.launchd.info/)
4. To stop the agent run the stop script

```bash
sh stop_macos.sh
```

or just enter the following command

```bash
launchctl bootout gui/$(id -u)/com.filem.job
```

5. If you changed something in the agent file and want to restart it **do not** use the start script it will overwrite your file instead use this command

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.filem.job.plist
launchctl list | grep filem
```

### Linux

1. Run the setup script

```bash
sh start_linux.sh
```

You should get an output similar to this

```bash
Created symlink '/home/username/.config/systemd/user/default.target.wants/filem.service' → '/home/username/.config/systemd/user/filem.service'.
Created symlink '/home/username/.config/systemd/user/timers.target.wants/filem.timer' → '/home/username/.config/systemd/user/filem.timer'.
```

With more detailed information below. Press Q when your done.

2. This creates a `filem.service` and `filem.timer` file in `~/.config/systemd/user` (default interval is 60 seconds)
3. If you want to change something please refer to the respective docs [systemd.servie](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html) and [systermd.timer](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.htmla)
4. To stop it use the stop script

```bash
sh stop_linux.sh
```

or

```bash
systemctl --user daemon-reload
systemctl --user stop filem.timer
systemctl --user disable filem.timer
```

5. In case you changed something and want to restart the service use the following command

```bash
systemctl --user daemon-reload
systemctl --user enable filem.service
systemctl --user enable --now filem.timer
systemctl --user start filem.service
systemctl --user status filem.service
systemctl --user status filem.timer
```

### Custom

If you want to use your own task scheduler, feel free to do so. The most important requirement is that your scheduler executes the scripts.entry_job file using the virtual environment.

## Usage

### Main window

The grid displayed on the main window contains the details of your created entries, as well as the timestamps for the last and next time each entry will be run.

You can use the search bar at the top of the grid to filter entries by the name you assigned to them.

To edit existing entries you can either use the **Edit** button or double click the entry in the grid.

If you want to remove an entry you can use the **Delete** button.

The **Start** button can start any kind of entry as long it is active.

The **Start all** button can start all entries that are active.

### Create/Edit window

Inside the **Create Entry** window, you can configure the settings for an entry.

1. **Name:** A required field that helps you easily distinguish your entries from one another.

2. **Description:** An optional field where you can add a detailed description of the entry.

3. **Type:** Select the action the entry should perform.
   - **Move:** Moves files or directories from the specified source path to the specified destination path if they match the configured rules.
   - **Copy:** Copies files or directories from the specified source path to the specified destination path if they match the configured rules.
   - **Delete:** Deletes files or directories from the specified source path if they match the configured rules.

4. **Activate:** A checkbox that allows you to enable or disable the entry. Disabled entries will not be run.

5. **Interval Type:** A set of radio buttons used to choose how the entry is triggered.
   - **Manually:** Entries with this option can only be started through the GUI and are ignored by the automation scripts.
   - **Interval:** Entries with this option are run automatically at the configured interval.
   - **Date/Time:** Entries with this option run once on the selected day of the month and time. If the selected day does not exist in the current month, the last valid day of the month will be used automatically.

6. **Directories** tab
   - **Origin Path:** The directory where the action will be performed. This must be an absolute path.
   - **Destination Path:** Required only when **Copy** or **Move** is selected. This is the directory where files or directories will be copied or moved. In case the directory doesn't exist yet it will be created with all it's parents.
   - **Directory Handling:** A set of radio buttons that determines which directories the entry should process.
     1. **None:** Ignores all directories.
     2. **Empty:** Processes only empty directories.
     3. **Filled:** Processes only directories that contain files or subdirectories.
     4. **All:** Processes all directories in the source path.

7. **Files** tab
   - **File Type Filter:** A set of radio buttons that determines how file types are handled.
     1. **None:** Ignores all files.
     2. **Selected Types:** Processes only files with the specified file types.
     3. **Exclude Types:** Processes all files except those with the specified file types.
     4. **All:** Processes all files.

   - **File Type Input:** A field where you can enter a file type (for example, `txt` or `png`).

   - **Add:** Adds the entered file type to the list.

   - **File Type List:** Displays all added file types. You can remove a file type by double-clicking it.

### Example

For example if you want to create an entry that should move all `png` and `jpg` files into a diffrent folder you can set it up like this:

1. **Name**: `Move pictures from A to B`
2. **Description**: `This entry automaticlly moves all pictures from path A to the path B because path A is filled with too much clutter`
3. **Type**: `move`
4. **Interval Type**: `interval`
5. Set the interval to repeat every `5 minutes`
6. **Activate**: Should be checked

**Directory** tab

7. **Origin Path**: absolute path of directory A
8. **Destination Path**: absoulte path of directory B
9. **Directory Handling**: `None`

**Files** tab

10. **File Type Filter**: `Selected Types`
11. Add `png` and `jpg` to the file list
12. Save the Entry
