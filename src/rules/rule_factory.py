from .entry_rule import EntryRule
from .dir_rules import AllDirs, EmptyDirs, FilledDirs
from .file_rules import AllFiles, ExcludeTypes, IncludeTypes
from ..entities.entry import Entry

class RuleFactory():
    @staticmethod
    def create(entry: Entry, file_types: list[str]) -> EntryRule:
        file_rule = None
        dir_rule = None

        if entry.include_files == "all":
            file_rule = AllFiles()
        elif entry.include_files == "selected types":
            file_rule = IncludeTypes(file_types)
        elif entry.include_files == "exclude types":
            file_rule = ExcludeTypes(file_types)

        if entry.include_dir == "all":
            dir_rule = AllDirs()
        elif entry.include_dir == "empty":
            dir_rule = EmptyDirs()
        elif entry.include_dir == "filled":
            dir_rule = FilledDirs()

        return EntryRule(file_rule=file_rule, dir_rule=dir_rule)