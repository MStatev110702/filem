from PyQt6 import QtCore, QtGui, QtWidgets
from .create_window import CreateWindow
from .error_window import ErrorWindow
from .table_model import TableModel
from .database.queries import db_call, get_selected_entry, delete_entry
from .entry import Entry

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # general window settings
        self.setObjectName("main_window")
        self.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        main_layout = QtWidgets.QHBoxLayout(self.centralwidget)
        left_layout = QtWidgets.QVBoxLayout()

        # search input
        search_layout = QtWidgets.QHBoxLayout()
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setObjectName("search_input")

        self.search_btn = QtWidgets.QToolButton()
        self.search_btn.setObjectName("search_btn")
        self.search_btn.setIcon(QtGui.QIcon.fromTheme("system-search"))
        self.search_btn.clicked.connect(self.search_entries)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)

        # table
        self.script_table = QtWidgets.QTableView()
        self.script_table.setObjectName("script_table")

        self.model = TableModel()
        self.script_table.setModel(self.model)
        self.script_table.doubleClicked.connect(self.open_edit_window)
        self.script_table.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )

        left_layout.addLayout(search_layout)
        left_layout.addWidget(self.script_table)

        # buttons
        right_layout = QtWidgets.QVBoxLayout()

        self.create_btn = QtWidgets.QPushButton()
        self.create_btn.setObjectName("create_btn")
        self.create_btn.clicked.connect(self.open_create_window)

        self.delete_btn = QtWidgets.QPushButton()
        self.delete_btn.setObjectName("delete_btn")
        self.delete_btn.clicked.connect(self.delete_selected_entry)

        self.edit_btn = QtWidgets.QPushButton()
        self.edit_btn.setObjectName("edit_btn")
        self.edit_btn.clicked.connect(self.open_edit_window)

        self.start_btn = QtWidgets.QPushButton()
        self.start_btn.setObjectName("start_btn")

        self.start_all_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_all_btn.setObjectName("start_all_btn")

        right_layout.addWidget(self.create_btn)
        right_layout.addWidget(self.delete_btn)
        right_layout.addWidget(self.edit_btn)
        right_layout.addWidget(self.start_btn)
        right_layout.addWidget(self.start_all_btn)

        right_layout.addStretch()
        main_layout.addLayout(left_layout, stretch=4)
        main_layout.addLayout(right_layout, stretch=1)

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
        result = db_call(delete_entry, row_id)
        if not result.get("success"):
            ErrorWindow(f"There was an error while trying to delete the entry with the id: {result.get("error")}").exec()
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
        result = db_call(get_selected_entry, row_id)

        if not result.get("success"):
            ErrorWindow(f"Failed to retrieve the entry with the id: {row_id}").exec()
            return

        entry = Entry.from_row(result.get("data"))
        
        self.window = CreateWindow(self, entry)
        self.window.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.window.show()


        
