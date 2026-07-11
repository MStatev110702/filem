from pathlib import Path
import shutil
from .action import Action

class DeleteFile(Action):
    def __init__(self):
        super().__init__()

    def execute(self, src: Path) -> None:
        src.unlink()

class MoveFile(Action):
    def __init__(self, dest: Path):
        super().__init__(dest)

    def execute(self, src: Path) -> None:
        file_name = src.name
        self.dest.mkdir(parents=True, exist_ok=True)
        dest_file = self.dest / file_name

        if dest_file.exists():
            new_name = self.auto_rename(src.stem, src.suffix)
            dest_file = self.dest / f"{new_name}"

        shutil.move(src, dest_file)

class CopyFile(Action):
    def __init__(self, dest: Path):
        super().__init__(dest)
    
    def execute(self, src: Path) -> None:
        file_name = src.name
        self.dest.mkdir(parents=True, exist_ok=True)
        dest_file = self.dest / file_name

        if dest_file.exists():
            new_name = self.auto_rename(src.stem, src.suffix)
            dest_file = self.dest / f"{new_name}"

        shutil.copy(src, dest_file)