from pathlib import Path
import shutil
from .action import Action

class DeleteDir(Action):
    def __init__(self):
        super().__init__()

    def execute(self, src: Path) -> None:
        shutil.rmtree(src)

# Same as the MoveFile action just in case I need some diffrent behavior in the future
class MoveDir(Action):
    def __init__(self, dest: Path):
        super().__init__(dest)

    def execute(self, src: Path) -> None:
        dir_name = src.name
        self.dest.mkdir(parents=True, exist_ok=True)
        dest_dir = self.dest / dir_name
        if dest_dir.exists():
            new_name = self.auto_rename(dir_name)
            dest_dir = self.dest / f"{new_name}"

        shutil.move(src, dest_dir)

class CopyDir(Action):
    def __init__(self, dest: Path):
        super().__init__(dest)
    
    def execute(self, src: Path) -> None:
        dir_name = src.name
        self.dest.mkdir(parents=True, exist_ok=True)
        dest_dir = self.dest / dir_name
        print(dir_name)
        if dest_dir.exists():
            new_name = self.auto_rename(dir_name)
            dest_dir = self.dest / f"{new_name}"

        shutil.copytree(src, dest_dir)