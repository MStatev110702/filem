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

    @staticmethod
    def from_row(row) -> "Entry":
        return Entry(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            type=row["type"],
            interval_type=row["interval_type"],
            schedule_type=row["schedule_type"],
            schedule_value=row["schedule_value"],
            originpath=row["originpath"],
            destpath=row["destpath"],
            include_dir=row["include_dir"],
            include_files=row["include_files"],
        )