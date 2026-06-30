from PyQt6 import QtCore
from .sqlite import get_file_types

class TypeListModel(QtCore.QAbstractListModel):
    def __init__(self, file_types: list[str]=[]):
        super().__init__()
        self.types = file_types
        
    def _load(self) -> list[str]:
        return []

    def data(self, index:QtCore.QModelIndex, role: int) -> any:
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.types[index.row()]
    
    def rowCount(self, index: int|None) -> None:
        return len(self.types)
    
    def add(self, text: str) -> None:
        row = len(self.types)
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self.types.append(text)
        self.endInsertRows()

    def delete(self, index: int) -> None:
        try:
            self.beginRemoveRows(QtCore.QModelIndex(), index, index)
            self.types.pop(index)
            self.endRemoveRows()
        except IndexError:
            return   

    def get_data(self) -> list[str]:
        return list(self.types)