from .rule import Rule
from pathlib import Path

class AllDirs(Rule):
    def match(self, path: Path) -> bool:
        return path.is_dir()

class EmptyDirs(Rule):
    def match(self, path: Path) -> bool:
        return path.is_dir() and not any(path.iterdir())
    
class FilledDirs(Rule):
    def match(self, path: Path) -> bool:
        return path.is_dir() and any(path.iterdir())