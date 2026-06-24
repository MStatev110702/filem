from PyQt6 import QtCore

class TypeListModel(QtCore.QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.types = self._load()

    def _load(self) -> list:
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
        