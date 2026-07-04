from pathlib import Path
import shutil
from .action import Action

class DeleteDir(Action):
    def __init__(self, src: Path):
        super().__init__(src, None)

    def execute(self) -> None:
        shutil.rmtree(self.src)

# Same as the MoveFile action just in case I need some diffrent behavior in the future
class MoveDir(Action):
    def __init__(self, src: Path, dest: Path):
        super().__init__(src, dest)

    def execute(self) -> None:
        dir_name = self.src.name
        self.dest.mkdir(parents=True, exist_ok=True)
        dest_dir = self.dest / dir_name
        if dest_dir.exists():
            new_name = self.auto_rename(dir_name)
            dest_dir = self.dest / f"{new_name}"

        shutil.move(self.src, dest_dir)

class CopyDir(Action):
    def __init__(self, src: Path, dest: Path):
        super().__init__(src, dest)
    
    def execute(self) -> None:
        dir_name = self.src.name
        self.dest.mkdir(parents=True, exist_ok=True)
        dest_dir = self.dest / dir_name
        print(dir_name)
        if dest_dir.exists():
            new_name = self.auto_rename(dir_name)
            dest_dir = self.dest / f"{new_name}"

        shutil.copytree(self.src, dest_dir)