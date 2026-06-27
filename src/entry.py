from dataclasses import dataclass

@dataclass
class Entry:
    id: int|None
    name: str
    description: str
    type: str
    interval_type: str
    schedule_type: str
    schedule_value: int
    originpath: str
    destpath: str
    include_dir: str
    include_files: str
    file_types: str