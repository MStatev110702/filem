from pathlib import Path

class AllFiles():
    def match(self, path: Path) -> bool:
        return path.is_file()

class IncludeTypes():
    def __init__(self, extensions: list[str]):
        self.extensions = [e.lower() for e in extensions]

    def match(self, path: Path) -> bool:
        return path.is_file() and path.suffix.lower() in self.extensions
    
class ExcludeTypes():
    def __init__(self, extensions: list[str]):
        self.extensions = [e.lower() for e in extensions]

    def match(self, path: Path) -> bool:
        return path.is_file() and path.suffix.lower() not in self.extensions