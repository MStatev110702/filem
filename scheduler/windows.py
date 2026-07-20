from win32com import client
from datetime import datetime, timedelta
from .paths import PROJECT_DIR

def main():
    python_exe = PROJECT_DIR / ".venv" / "Scripts" / "pythonw.exe"

    scheduler = client.Dispatch("Schedule.Service")
    scheduler.Connect()

    root_folder = scheduler.GetFolder("\\")

    task = scheduler.NewTask(0)

    principal = task.Principal
    principal.LogonType = 3 
    principal.RunLevel = 0  

    action = task.Actions.Create(0)
    action.Path = str(python_exe)
    action.Arguments = "-m scripts.entry_job"
    action.WorkingDirectory = str(PROJECT_DIR)

    trigger = task.Triggers.Create(2)

    start = datetime.now() + timedelta(minutes=1)

    trigger.StartBoundary = start.strftime("%Y-%m-%dT%H:%M:%S")

    repetition = trigger.Repetition
    repetition.Interval = "PT1M"
    repetition.StopAtDurationEnd = False

    settings = task.Settings
    settings.Enabled = True
    settings.Hidden = False
    settings.StartWhenAvailable = True
    settings.ExecutionTimeLimit = "PT0S"

    root_folder.RegisterTaskDefinition(
        "Filem job",
        task,
        6,
        None,
        None,
        3
    )

if __name__ == "__main__":
    main()