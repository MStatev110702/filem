from pathlib import Path
from .rule import Rule

class EntryRule():
    def __init__(self, file_rule: Rule|None, dir_rule: Rule|None):
        self.file_rule = file_rule
        self.dir_rule = dir_rule
    
    def match(self, path: Path) -> bool:
        if path.is_file() and self.file_rule:
            return self.file_rule.match(path)
        
        if path.is_dir() and self.dir_rule:
            return self.dir_rule.match(path)

        return False