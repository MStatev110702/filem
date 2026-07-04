from abc import ABC, abstractmethod
from pathlib import Path

class Action():
    def __init__(self, src: Path, dest: Path|None = None):
        self.src = src
        self.dest = dest

    @abstractmethod
    def execute(self) -> None:
        ...

    def auto_rename(self, name: str, suffix: str = "") -> str:
        dest_file = self.dest / name
        stem = dest_file.stem

        i = 1
        while True:
            file_name = f"{stem} ({i}){suffix}" 
            dest_file = self.dest / file_name
            if not dest_file.exists():
                return file_name
            i+= 1