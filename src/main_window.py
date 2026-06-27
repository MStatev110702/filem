from PyQt6 import QtCore, QtGui, QtWidgets
from .create_window import CreateWindow
from .error_window import ErrorWindow
from .table_model import TableModel
from .sqlite import delete_entry, get_selected_entry

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # general window settings
        self.setObjectName("main_window")
        self.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        # menubar
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")

        # statusbar
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")

        self.setCentralWidget(self.centralwidget)
        self.setMenuBar(self.menubar)
        self.setStatusBar(self.statusbar)

        # search input
        self.search_input = QtWidgets.QLineEdit(self.centralwidget)
        self.search_input.setGeometry(QtCore.QRect(30, 20, 591, 21))
        self.search_input.setObjectName("search_input")

        self.search_btn = QtWidgets.QToolButton(self.centralwidget)
        self.search_btn.setGeometry(QtCore.QRect(650, 20, 26, 22))
        self.search_btn.setObjectName("search_btn")
        self.search_btn.setIcon(QtGui.QIcon.fromTheme("system-search"))
        self.search_btn.clicked.connect(self.search_entries)

        # table
        self.script_table = QtWidgets.QTableView(self.centralwidget)
        self.script_table.setGeometry(QtCore.QRect(30, 60, 591, 441))
        self.script_table.setObjectName("script_table")

        self.model = TableModel()
        self.script_table.setModel(self.model)
        self.script_table.doubleClicked.connect(self.open_edit_window)

        # buttons
        self.create_btn = QtWidgets.QPushButton(self.centralwidget)
        self.create_btn.setGeometry(QtCore.QRect(650, 70, 113, 32))
        self.create_btn.setObjectName("create_btn")
        self.create_btn.clicked.connect(self.open_create_window)

        self.delete_btn = QtWidgets.QPushButton(self.centralwidget)
        self.delete_btn.setGeometry(QtCore.QRect(650, 110, 113, 32))
        self.delete_btn.setObjectName("delete_btn")
        self.delete_btn.clicked.connect(self.delete_selected_entry)

        self.edit_btn = QtWidgets.QPushButton(self.centralwidget)
        self.edit_btn.setGeometry(QtCore.QRect(650, 150, 113, 32))
        self.edit_btn.setObjectName("edit_btn")
        self.edit_btn.clicked.connect(self.open_edit_window)

        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setGeometry(QtCore.QRect(650, 190, 113, 32))
        self.start_btn.setObjectName("start_btn")

        self.start_all_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_all_btn.setGeometry(QtCore.QRect(650, 230, 113, 32))
        self.start_all_btn.setObjectName("start_all_btn")

        self.retranslate_ui()

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Main Window"))
        
        # buttons
        self.search_btn.setText(_translate("MainWindow", "..."))
        self.create_btn.setText(_translate("MainWindow", "Create"))
        self.delete_btn.setText(_translate("MainWindow", "Delete"))
        self.edit_btn.setText(_translate("MainWindow", "Edit"))
        self.start_btn.setText(_translate("MainWindow", "Start"))
        self.start_all_btn.setText(_translate("MainWindow", "Start all"))

    def open_create_window(self):
        self.window = CreateWindow(self)
        self.window.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.window.show()

    def delete_selected_entry(self):
        index = self.script_table.selectionModel().currentIndex()

        if index.row() == -1:
            ErrorWindow("Please select one row in the table.").exec()
            return

        row_id = self.model.get_row_id(index)

        if not delete_entry(row_id):
            ErrorWindow(f"There was an error while trying to delete the entry with the id: {row_id}").exec()
            return
        
        self.search_entries()

    def search_entries(self):
        name = self.search_input.text().strip()
        self.model.load(name)

    def open_edit_window(self):
        index = self.script_table.selectionModel().currentIndex()

        if index.row() == -1:
            ErrorWindow("Please select one row in the table.").exec()
            return
        
        row_id = self.model.get_row_id(index)
        entry = get_selected_entry(row_id)

        if not entry:
            ErrorWindow(f"Failed to retieve the entry with the id: {row_id}").exec()
            return
        
        self.window = CreateWindow(self, entry)
        self.window.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.window.show()


        
