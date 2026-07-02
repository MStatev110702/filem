from pathlib import Path
from .rule import Rule

class AllFiles(Rule):
    def match(self, path: Path) -> bool:
        return path.is_file()

class IncludeTypes(Rule):
    def __init__(self, extensions: list[str]):
        self.extensions = [e.lower() for e in extensions]

    def match(self, path: Path) -> bool:
        return path.is_file() and path.suffix.lower() in self.extensions
    
class ExcludeTypes(Rule):
    def __init__(self, extensions: list[str]):
        self.extensions = [e.lower() for e in extensions]

    def match(self, path: Path) -> bool:
        return path.is_file() and path.suffix.lower() not in self.extensions