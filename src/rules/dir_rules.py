from pathlib import Path

class AllDirs():
    def match(self, path: Path) -> bool:
        return path.is_dir()

class EmptyDirs():
    def match(self, path: Path) -> bool:
        return path.is_dir() and not any(path.iterdir())
    
class FilledDirs():
    def match(self, path: Path) -> bool:
        return path.is_dir() and any(path.iterdir())