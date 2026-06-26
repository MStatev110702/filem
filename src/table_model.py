from PyQt6 import QtCore
from PyQt6.QtCore import Qt

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._data = []

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0]) if len(self._data) > 0 else 0

    