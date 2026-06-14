from PyQt5 import QtCore, QtGui, QtWidgets

class UiMainWindow(object):
    def setup_ui(self, main_window):
        # general window settings
        main_window.setObjectName("main_window")
        main_window.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        main_window.setCentralWidget(self.centralwidget)

        # menubar
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        
        main_window.setMenuBar(self.menubar)

        # statusbar
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")

        main_window.setStatusBar(self.statusbar)

        # search input
        self.search_input = QtWidgets.QLineEdit(self.centralwidget)
        self.search_input.setGeometry(QtCore.QRect(30, 20, 591, 21))
        self.search_input.setObjectName("search_input")

        self.search_btn = QtWidgets.QToolButton(self.centralwidget)
        self.search_btn.setGeometry(QtCore.QRect(650, 20, 26, 22))
        self.search_btn.setObjectName("search_btn")

        # table
        self.script_table = QtWidgets.QTableWidget(self.centralwidget)
        self.script_table.setGeometry(QtCore.QRect(30, 60, 591, 441))
        self.script_table.setObjectName("script_table")
        self.script_table.setColumnCount(0)
        self.script_table.setRowCount(0)

        # buttons
        self.create_btn = QtWidgets.QPushButton(self.centralwidget)
        self.create_btn.setGeometry(QtCore.QRect(650, 70, 113, 32))
        self.create_btn.setObjectName("create_btn")

        self.delete_btn = QtWidgets.QPushButton(self.centralwidget)
        self.delete_btn.setGeometry(QtCore.QRect(650, 110, 113, 32))
        self.delete_btn.setObjectName("delete_btn")

        self.edit_btn = QtWidgets.QPushButton(self.centralwidget)
        self.edit_btn.setGeometry(QtCore.QRect(650, 150, 113, 32))
        self.edit_btn.setObjectName("edit_btn")

        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setGeometry(QtCore.QRect(650, 190, 113, 32))
        self.start_btn.setObjectName("start_btn")

        self.start_all_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_all_btn.setGeometry(QtCore.QRect(650, 230, 113, 32))
        self.start_all_btn.setObjectName("start_all_btn")

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "main_window"))
        
        # buttons
        self.search_btn.setText(_translate("main_window", "..."))
        self.create_btn.setText(_translate("main_window", "Create"))
        self.delete_btn.setText(_translate("main_window", "Delete"))
        self.edit_btn.setText(_translate("main_window", "Edit"))
        self.start_btn.setText(_translate("main_window", "Start"))
        self.start_all_btn.setText(_translate("main_window", "Start all"))



