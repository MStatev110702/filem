from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from .sqlite import get_all_entries

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._data = []
        self.headers = [
            "id",
            "name",
            "description",
            "type",
            "interval type",
            "schedule type",
            "schedule value",
            "originpath",
            "destpath",
            "include dir",
            "include files",
            "file types",
            "state"
        ]
        self.load()

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self.headers)

    def headerData(self, section, orientation, role):
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            return self.headers[section]

        return section + 1

    def load(self, name: str = ""):
        self.beginResetModel()
        self._data = get_all_entries(name)
        self.endResetModel()
    
    def get_row_id(self, index):
        return self._data[index.row()][0]