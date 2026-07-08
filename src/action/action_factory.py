from pathlib import Path
from ..entry import Entry
from .action import Action
from .file_actions import CopyFile, MoveFile, DeleteFile
from .dir_actions import CopyDir, MoveDir, DeleteDir

class ActionFactory():
    @staticmethod
    def create(entry: Entry, src: Path) -> Action:
        dest = entry.destpath.strip()

        if entry.type in ("COPY", "MOVE"):
            if dest == "":
                raise ValueError("The destination should'nt be empty if the type is COPY or MOVE")
            elif dest.startswith("."):
                raise ValueError("The paths should'nt be relative")
        
        if str(src).startswith("."):
            raise ValueError("The paths should'nt be relative")

        dest_path = Path(dest) 

        if not src.exists():
            raise FileExistsError("The originpath does not exist")

        if src.is_file():
            if entry.type == "DELETE":
                return DeleteFile(src) 
            elif entry.type == "MOVE":
                return MoveFile(src, dest_path)
            elif entry.type == "COPY":
                return CopyFile(src, dest_path)
            else:
                raise ValueError("Type is not implemented")
        elif src.is_dir():
            if entry.type == "DELETE":
                return DeleteDir(src) 
            elif entry.type == "MOVE":
                return MoveDir(src, dest_path)
            elif entry.type == "COPY":
                return CopyDir(src, dest_path)
            else:
                raise ValueError("Type is not implemented") 