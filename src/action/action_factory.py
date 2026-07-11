from pathlib import Path
from ..entities.entry import Entry
from .action import Action
from .file_actions import CopyFile, MoveFile, DeleteFile
from .dir_actions import CopyDir, MoveDir, DeleteDir

class FileActionFactory:
    @staticmethod
    def create(entry: Entry) -> Action:
        if entry.type == "DELETE":
            return DeleteFile() 
        
        dest = Path(entry.destpath.strip())

        if entry.type == "MOVE":
            return MoveFile(dest)
        elif entry.type == "COPY":
            return CopyFile(dest)
        else:
            raise ValueError("Type is not implemented")
        

class DirActionFactory:
    @staticmethod
    def create(entry: Entry) -> Action:
        if entry.type == "DELETE":
            return DeleteDir() 
        
        dest = Path(entry.destpath.strip())
 
        if entry.type == "MOVE":
            return MoveDir(dest)
        elif entry.type == "COPY":
            return CopyDir(dest)
        else:
            raise ValueError("Type is not implemented") 