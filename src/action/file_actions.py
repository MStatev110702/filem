from pathlib import Path
import shutil
from .action import Action

class DeleteFile(Action):
    def __init__(self, src: Path):
        super().__init__(src, None)

    def execute(self) -> None:
        self.src.unlink()

class MoveFile(Action):
    def __init__(self, src: Path, dest: Path):
        super().__init__(src, dest)

    def execute(self) -> None:
        file_name = self.src.name
        self.dest.mkdir(parents=True, exist_ok=True)
        dest_file = self.dest / file_name

        if dest_file.exists():
            new_name = self.auto_rename(self.src.stem, self.src.suffix)
            dest_file = self.dest / f"{new_name}"

        shutil.move(self.src, dest_file)

class CopyFile(Action):
    def __init__(self, src: Path, dest: Path):
        super().__init__(src, dest)
    
    def execute(self) -> None:
        file_name = self.src.name
        self.dest.mkdir(parents=True, exist_ok=True)
        dest_file = self.dest / file_name

        if dest_file.exists():
            new_name = self.auto_rename(self.src.stem, self.src.suffix)
            dest_file = self.dest / f"{new_name}"

        shutil.copy(self.src, dest_file)