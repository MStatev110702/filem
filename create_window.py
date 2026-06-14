from PyQt5 import QtCore, QtGui, QtWidgets

class UiCreateWindow(object):
    def setup_ui(self, main_window):
        # general window settings
        main_window.setObjectName("main_window")
        main_window.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")

        # statusbar
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        
        self.save_btn = QtWidgets.QPushButton(self.centralwidget)
        self.save_btn.setGeometry(QtCore.QRect(600, 520, 81, 26))
        self.save_btn.setObjectName("save_btn")

        self.cancel_btn = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_btn.setGeometry(QtCore.QRect(700, 520, 81, 26))
        self.cancel_btn.setObjectName("cancel_btn")

        self.statusbar.addPermanentWidget(self.save_btn)
        self.statusbar.addPermanentWidget(self.cancel_btn)
        
        main_window.setStatusBar(self.statusbar)
        main_window.setCentralWidget(self.centralwidget)

        # name, description and type input fields with their labels
        self.name_label = QtWidgets.QLabel(self.centralwidget)
        self.name_label.setGeometry(QtCore.QRect(20, 20, 60, 16))
        self.name_label.setObjectName("name_label")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(130, 20, 481, 22))
        self.lineEdit.setObjectName("lineEdit")

        self.desc_label = QtWidgets.QLabel(self.centralwidget)
        self.desc_label.setGeometry(QtCore.QRect(20, 80, 81, 16))
        self.desc_label.setObjectName("desc_label")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(130, 60, 481, 64))
        self.textEdit.setObjectName("textEdit")

        self.type_label = QtWidgets.QLabel(self.centralwidget)
        self.type_label.setGeometry(QtCore.QRect(20, 150, 60, 16))
        self.type_label.setObjectName("type_label")

        self.type_combo = QtWidgets.QComboBox(self.centralwidget)
        self.type_combo.setGeometry(QtCore.QRect(130, 140, 481, 22))
        self.type_combo.setObjectName("type_combo")


        # radio menu for selecting the start of the skript
        self.main_interval_radio = QtWidgets.QRadioButton(self.centralwidget)
        self.main_interval_radio.setGeometry(QtCore.QRect(10, 190, 97, 21))
        self.main_interval_radio.setObjectName("main_interval_radio")

        self.main_datetime_radio = QtWidgets.QRadioButton(self.centralwidget)
        self.main_datetime_radio.setGeometry(QtCore.QRect(10, 230, 97, 21))
        self.main_datetime_radio.setObjectName("main_datetime_radio")

        self.main_newest_radio = QtWidgets.QRadioButton(self.centralwidget)
        self.main_newest_radio.setGeometry(QtCore.QRect(10, 270, 97, 21))
        self.main_newest_radio.setObjectName("main_newest_radio")

        # interval fields
        self.repeat_label = QtWidgets.QLabel(self.centralwidget)
        self.repeat_label.setGeometry(QtCore.QRect(110, 190, 91, 16))
        self.repeat_label.setObjectName("repeat_label")

        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(210, 190, 42, 22))
        self.spinBox.setObjectName("spinBox")

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(300, 190, 81, 22))
        self.comboBox.setObjectName("comboBox")

        # date/time fields
        self.day_month_label = QtWidgets.QLabel(self.centralwidget)
        self.day_month_label.setGeometry(QtCore.QRect(110, 230, 81, 16))
        self.day_month_label.setObjectName("day_month_label")

        self.day_month_spin = QtWidgets.QSpinBox(self.centralwidget)
        self.day_month_spin.setGeometry(QtCore.QRect(210, 230, 42, 22))
        self.day_month_spin.setObjectName("day_month_spin")

        self.time_label = QtWidgets.QLabel(self.centralwidget)
        self.time_label.setGeometry(QtCore.QRect(290, 230, 60, 16))
        self.time_label.setObjectName("time_label")

        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setGeometry(QtCore.QRect(350, 230, 118, 22))
        self.timeEdit.setObjectName("timeEdit")
        
        # start of the tab widget
        self.tab_bar = QtWidgets.QTabWidget(self.centralwidget)
        self.tab_bar.setGeometry(QtCore.QRect(10, 300, 771, 211))
        self.tab_bar.setObjectName("tab_bar")

        self.dir_tab = QtWidgets.QWidget()
        self.dir_tab.setObjectName("dir_tab")

        self.files_tab = QtWidgets.QWidget()
        self.files_tab.setObjectName("files_tab")

        self.tab_bar.addTab(self.dir_tab, "")
        self.tab_bar.addTab(self.files_tab, "")
        self.tab_bar.setCurrentIndex(0)

        # directory tab
        # originpath
        self.origin_label = QtWidgets.QLabel(self.dir_tab)
        self.origin_label.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.origin_label.setObjectName("origin_label")

        self.origin_input = QtWidgets.QLineEdit(self.dir_tab)
        self.origin_input.setGeometry(QtCore.QRect(120, 10, 441, 22))
        self.origin_input.setObjectName("origin_input")

        self.origin_tool_btn = QtWidgets.QToolButton(self.dir_tab)
        self.origin_tool_btn.setGeometry(QtCore.QRect(570, 10, 23, 18))
        self.origin_tool_btn.setObjectName("origin_tool_btn")
        
        # destinationpath
        self.dest_label = QtWidgets.QLabel(self.dir_tab)
        self.dest_label.setGeometry(QtCore.QRect(10, 40, 101, 16))
        self.dest_label.setObjectName("dest_label")

        self.dest_input = QtWidgets.QLineEdit(self.dir_tab)
        self.dest_input.setGeometry(QtCore.QRect(120, 40, 441, 22))
        self.dest_input.setObjectName("dest_input")

        self.dest_tool_btn = QtWidgets.QToolButton(self.dir_tab)
        self.dest_tool_btn.setGeometry(QtCore.QRect(570, 40, 23, 18))
        self.dest_tool_btn.setObjectName("dest_tool_btn")

        # include directory radio buttons
        self.include_dir_label = QtWidgets.QLabel(self.dir_tab)
        self.include_dir_label.setGeometry(QtCore.QRect(10, 80, 161, 16))
        self.include_dir_label.setObjectName("include_dir_label")

        self.dir_none_radio = QtWidgets.QRadioButton(self.dir_tab)
        self.dir_none_radio.setGeometry(QtCore.QRect(10, 120, 97, 21))
        self.dir_none_radio.setObjectName("dir_none_radio")

        self.dir_empty_radio = QtWidgets.QRadioButton(self.dir_tab)
        self.dir_empty_radio.setGeometry(QtCore.QRect(100, 120, 97, 21))
        self.dir_empty_radio.setObjectName("dir_empty_radio")

        self.dir_filled_radio = QtWidgets.QRadioButton(self.dir_tab)
        self.dir_filled_radio.setGeometry(QtCore.QRect(210, 120, 97, 21))
        self.dir_filled_radio.setObjectName("dir_filled_radio")

        self.dir_all_radio = QtWidgets.QRadioButton(self.dir_tab)
        self.dir_all_radio.setGeometry(QtCore.QRect(310, 110, 97, 21))
        self.dir_all_radio.setObjectName("dir_all_radio")

        # files tab
        # files radio buttons
        self.files_none_radio = QtWidgets.QRadioButton(self.files_tab)
        self.files_none_radio.setGeometry(QtCore.QRect(20, 20, 97, 21))
        self.files_none_radio.setObjectName("files_none_radio")

        self.files_selected_radio = QtWidgets.QRadioButton(self.files_tab)
        self.files_selected_radio.setGeometry(QtCore.QRect(20, 50, 121, 21))
        self.files_selected_radio.setObjectName("files_selected_radio")

        self.files_exclude_radio = QtWidgets.QRadioButton(self.files_tab)
        self.files_exclude_radio.setGeometry(QtCore.QRect(20, 80, 111, 21))
        self.files_exclude_radio.setObjectName("files_exclude_radio")

        self.files_all_radio = QtWidgets.QRadioButton(self.files_tab)
        self.files_all_radio.setGeometry(QtCore.QRect(20, 110, 97, 21))
        self.files_all_radio.setObjectName("files_all_radio")

        # type list and combobox
        self.listView = QtWidgets.QListView(self.files_tab)
        self.listView.setGeometry(QtCore.QRect(210, 10, 221, 161))
        self.listView.setObjectName("listView")

        self.files_combo = QtWidgets.QComboBox(self.files_tab)
        self.files_combo.setGeometry(QtCore.QRect(470, 70, 161, 22))
        self.files_combo.setObjectName("files_combo")

        self.add_btn = QtWidgets.QPushButton(self.files_tab)
        self.add_btn.setGeometry(QtCore.QRect(660, 70, 81, 26))
        self.add_btn.setObjectName("add_btn")

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "create"))

        # labels
        self.name_label.setText(_translate("main_window", "Name"))
        self.desc_label.setText(_translate("main_window", "Description"))
        self.repeat_label.setText(_translate("main_window", "Repeat every"))
        self.type_label.setText(_translate("main_window", "Type"))
        self.time_label.setText(_translate("main_window", "Time"))
        self.day_month_label.setText(_translate("main_window", "Day of month"))
        self.origin_label.setText(_translate("main_window", "Originpath"))
        self.include_dir_label.setText(_translate("main_window", "Include directories?"))
        self.dest_label.setText(_translate("main_window", "Destinationpath"))

        # buttons
        self.save_btn.setText(_translate("main_window", "save"))
        self.cancel_btn.setText(_translate("main_window", "cancel"))
        self.origin_tool_btn.setText(_translate("main_window", "..."))
        self.dest_tool_btn.setText(_translate("main_window", "..."))
        self.add_btn.setText(_translate("main_window", "Add"))

        # tabs
        self.tab_bar.setTabText(self.tab_bar.indexOf(self.dir_tab), _translate("main_window", "Directory"))
        self.tab_bar.setTabText(self.tab_bar.indexOf(self.files_tab), _translate("main_window", "Files"))

        # radio buttons
        self.main_interval_radio.setText(_translate("main_window", "Interval"))
        self.main_datetime_radio.setText(_translate("main_window", "Date/Time"))
        self.main_newest_radio.setText(_translate("main_window", "Newest"))
        self.dir_none_radio.setText(_translate("main_window", "None"))
        self.dir_empty_radio.setText(_translate("main_window", "Empty"))
        self.dir_filled_radio.setText(_translate("main_window", "Filled"))
        self.dir_all_radio.setText(_translate("main_window", "All"))
        self.files_none_radio.setText(_translate("main_window", "None"))
        self.files_selected_radio.setText(_translate("main_window", "Selected types"))
        self.files_exclude_radio.setText(_translate("main_window", "Exclude types"))
        self.files_all_radio.setText(_translate("main_window", "All"))

