from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QTableView, QSizePolicy, QPushButton, QToolButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # general window settings
        self.setObjectName("main_window")
        self.resize(800, 600)

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        self.model = None

        main_layout = QHBoxLayout(self.centralwidget)
        left_layout = QVBoxLayout()

        # search input
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setObjectName("search_input")

        self.search_btn = QToolButton()
        self.search_btn.setObjectName("search_btn")
        self.search_btn.setIcon(QtGui.QIcon.fromTheme("system-search"))

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)

        # table
        self.script_table = QTableView()
        self.script_table.setObjectName("script_table")

        self.script_table.setModel(self.model)
        self.script_table.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        left_layout.addLayout(search_layout)
        left_layout.addWidget(self.script_table)

        # buttons
        right_layout = QVBoxLayout()

        self.create_btn = QPushButton()
        self.create_btn.setObjectName("create_btn")

        self.delete_btn = QPushButton()
        self.delete_btn.setObjectName("delete_btn")

        self.edit_btn = QPushButton()
        self.edit_btn.setObjectName("edit_btn")

        self.start_btn = QPushButton()
        self.start_btn.setObjectName("start_btn")

        self.start_all_btn = QPushButton(self.centralwidget)
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

    def set_model(self, model):
        self.script_table.setModel(model)

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