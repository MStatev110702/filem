from PyQt6 import QtCore, QtGui, QtWidgets
from enum import Enum

class TypeComboValues(Enum):
    COPY = "copy"
    DELETE = "delete"
    MOVE = "move"

class IntervalTypeComboValues(Enum):
    S = "seconds"
    MIN = "minutes"
    H = "hours"
    D = "days"
    MON = "months"

class CreateWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        # general window settings
        self.setObjectName("create_window")
        self.resize(800, 550)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        # name, description and type input fields with their labels
        self.name_label = QtWidgets.QLabel(self.centralwidget)
        self.name_label.setGeometry(QtCore.QRect(20, 20, 70, 16))
        self.name_label.setObjectName("name_label")

        self.name_input = QtWidgets.QLineEdit(self.centralwidget)
        self.name_input.setGeometry(QtCore.QRect(130, 20, 500, 22))
        self.name_input.setObjectName("name_input")

        self.desc_label = QtWidgets.QLabel(self.centralwidget)
        self.desc_label.setGeometry(QtCore.QRect(20, 60, 70, 16))
        self.desc_label.setObjectName("desc_label")

        self.desc_input = QtWidgets.QTextEdit(self.centralwidget)
        self.desc_input.setGeometry(QtCore.QRect(130, 60, 500, 64))
        self.desc_input.setObjectName("desc_input")

        self.type_label = QtWidgets.QLabel(self.centralwidget)
        self.type_label.setGeometry(QtCore.QRect(20, 140, 70, 16))
        self.type_label.setObjectName("type_label")

        self.type_combo = QtWidgets.QComboBox(self.centralwidget)
        self.type_combo.setGeometry(QtCore.QRect(124, 140, 514, 22))
        self.type_combo.setObjectName("type_combo")
        self.load_combo_values(self.type_combo, TypeComboValues)
        self.type_combo.currentIndexChanged.connect(self.type_combo_changed)

        self.init_main_radio_ui()
        self.init_tab_bar()
        self.retranslate_ui()

    def init_main_radio_ui(self):
        # radio menu for selecting the start of the script
        self.main_manual_radio = QtWidgets.QRadioButton(self.centralwidget)
        self.main_manual_radio.setGeometry(QtCore.QRect(20, 180, 97, 21))
        self.main_manual_radio.setObjectName("main_manual_radio")
        self.main_manual_radio.setChecked(True)

        self.main_interval_radio = QtWidgets.QRadioButton(self.centralwidget)
        self.main_interval_radio.setGeometry(QtCore.QRect(140, 180, 97, 21))
        self.main_interval_radio.setObjectName("main_interval_radio")

        self.main_datetime_radio = QtWidgets.QRadioButton(self.centralwidget)
        self.main_datetime_radio.setGeometry(QtCore.QRect(240, 180, 97, 21))
        self.main_datetime_radio.setObjectName("main_datetime_radio")

        self.main_newest_radio = QtWidgets.QRadioButton(self.centralwidget)
        self.main_newest_radio.setGeometry(QtCore.QRect(340, 180, 97, 21))
        self.main_newest_radio.setObjectName("main_newest_radio")
        
        main_radio_group = QtWidgets.QButtonGroup(self.centralwidget)
        main_radio_group.setExclusive(True)
        main_radio_group.addButton(self.main_manual_radio, 1)
        main_radio_group.addButton(self.main_interval_radio, 2)
        main_radio_group.addButton(self.main_datetime_radio, 3)
        main_radio_group.addButton(self.main_newest_radio, 4)
        main_radio_group.buttonClicked.connect(self.main_radio_changed)

        # interval fields
        self.repeat_label = QtWidgets.QLabel(self.centralwidget)
        self.repeat_label.setGeometry(QtCore.QRect(20, 230, 91, 16))
        self.repeat_label.setObjectName("repeat_label")

        self.repeat_spin = QtWidgets.QSpinBox(self.centralwidget)
        self.repeat_spin.setGeometry(QtCore.QRect(120, 230, 42, 22))
        self.repeat_spin.setObjectName("repeat_spin")

        self.interval_type_combo = QtWidgets.QComboBox(self.centralwidget)
        self.interval_type_combo.setGeometry(QtCore.QRect(220, 230, 100, 22))
        self.interval_type_combo.setObjectName("interval_type_combo")
        self.load_combo_values(self.interval_type_combo, IntervalTypeComboValues)

        # date/time fields
        self.day_month_label = QtWidgets.QLabel(self.centralwidget)
        self.day_month_label.setGeometry(QtCore.QRect(20, 230, 81, 16))
        self.day_month_label.setObjectName("day_month_label")

        self.day_month_spin = QtWidgets.QSpinBox(self.centralwidget)
        self.day_month_spin.setGeometry(QtCore.QRect(120, 230, 42, 22))
        self.day_month_spin.setObjectName("day_month_spin")

        self.time_label = QtWidgets.QLabel(self.centralwidget)
        self.time_label.setGeometry(QtCore.QRect(210, 230, 60, 16))
        self.time_label.setObjectName("time_label")

        self.time_edit = QtWidgets.QTimeEdit(self.centralwidget)
        self.time_edit.setGeometry(QtCore.QRect(210, 230, 118, 22))
        self.time_edit.setObjectName("time_edit")

        # statusbar
        self.save_btn = QtWidgets.QPushButton(self.centralwidget)
        self.save_btn.setGeometry(QtCore.QRect(600, 515, 81, 30))
        self.save_btn.setObjectName("save_btn")
        self.save_btn.clicked.connect(self.save_entry)

        self.cancel_btn = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_btn.setGeometry(QtCore.QRect(700, 515, 81, 30))
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.clicked.connect(self.close_window)
        
        self.main_radio_changed(self.main_manual_radio)

    def init_tab_bar(self):
        # start of the tab widget
        self.tab_bar = QtWidgets.QTabWidget(self.centralwidget)
        self.tab_bar.setGeometry(QtCore.QRect(10, 260, 771, 211))
        self.tab_bar.setObjectName("tab_bar")

        self.dir_tab = QtWidgets.QWidget()
        self.dir_tab.setObjectName("dir_tab")

        self.files_tab = QtWidgets.QWidget()
        self.files_tab.setObjectName("files_tab")

        self.tab_bar.addTab(self.dir_tab, "")
        self.tab_bar.addTab(self.files_tab, "")
        self.tab_bar.setCurrentIndex(0)

        self.init_dir_tab()
        self.init_files_tab()

    def init_dir_tab(self):
        # originpath
        self.origin_label = QtWidgets.QLabel(self.dir_tab)
        self.origin_label.setGeometry(QtCore.QRect(10, 10, 91, 22))
        self.origin_label.setObjectName("origin_label")

        self.origin_input = QtWidgets.QLineEdit(self.dir_tab)
        self.origin_input.setGeometry(QtCore.QRect(120, 10, 441, 22))
        self.origin_input.setObjectName("origin_input")

        self.origin_tool_btn = QtWidgets.QToolButton(self.dir_tab)
        self.origin_tool_btn.setGeometry(QtCore.QRect(570, 11, 19, 18))
        self.origin_tool_btn.setObjectName("origin_tool_btn")
        self.origin_tool_btn.clicked.connect(self.open_file_explorer)
        
        # destinationpath
        self.dest_label = QtWidgets.QLabel(self.dir_tab)
        self.dest_label.setGeometry(QtCore.QRect(10, 40, 101, 22))
        self.dest_label.setObjectName("dest_label")

        self.dest_input = QtWidgets.QLineEdit(self.dir_tab)
        self.dest_input.setGeometry(QtCore.QRect(120, 40, 441, 22))
        self.dest_input.setObjectName("dest_input")

        self.dest_tool_btn = QtWidgets.QToolButton(self.dir_tab)
        self.dest_tool_btn.setGeometry(QtCore.QRect(570, 41, 19, 18))
        self.dest_tool_btn.setObjectName("dest_tool_btn")
        self.dest_tool_btn.clicked.connect(self.open_file_explorer)

        # include directory radio buttons
        self.include_dir_label = QtWidgets.QLabel(self.dir_tab)
        self.include_dir_label.setGeometry(QtCore.QRect(10, 80, 161, 22))
        self.include_dir_label.setObjectName("include_dir_label")

        self.dir_none_radio = QtWidgets.QRadioButton(self.dir_tab)
        self.dir_none_radio.setGeometry(QtCore.QRect(10, 120, 97, 21))
        self.dir_none_radio.setObjectName("dir_none_radio")
        self.dir_none_radio.setChecked(True)

        self.dir_empty_radio = QtWidgets.QRadioButton(self.dir_tab)
        self.dir_empty_radio.setGeometry(QtCore.QRect(100, 120, 97, 21))
        self.dir_empty_radio.setObjectName("dir_empty_radio")

        self.dir_filled_radio = QtWidgets.QRadioButton(self.dir_tab)
        self.dir_filled_radio.setGeometry(QtCore.QRect(210, 120, 97, 21))
        self.dir_filled_radio.setObjectName("dir_filled_radio")

        self.dir_all_radio = QtWidgets.QRadioButton(self.dir_tab)
        self.dir_all_radio.setGeometry(QtCore.QRect(310, 120, 97, 21))
        self.dir_all_radio.setObjectName("dir_all_radio")

        dir_btn_group = QtWidgets.QButtonGroup(self.dir_tab)
        dir_btn_group.setExclusive(True)
        dir_btn_group.addButton(self.dir_none_radio)
        dir_btn_group.addButton(self.dir_empty_radio)
        dir_btn_group.addButton(self.dir_filled_radio)
        dir_btn_group.addButton(self.dir_all_radio)

    def init_files_tab(self):
        # files radio buttons
        self.files_none_radio = QtWidgets.QRadioButton(self.files_tab)
        self.files_none_radio.setGeometry(QtCore.QRect(20, 20, 121, 21))
        self.files_none_radio.setObjectName("files_none_radio")
        self.files_none_radio.setChecked(True)

        self.files_selected_radio = QtWidgets.QRadioButton(self.files_tab)
        self.files_selected_radio.setGeometry(QtCore.QRect(20, 50, 121, 21))
        self.files_selected_radio.setObjectName("files_selected_radio")

        self.files_exclude_radio = QtWidgets.QRadioButton(self.files_tab)
        self.files_exclude_radio.setGeometry(QtCore.QRect(20, 80, 121, 21))
        self.files_exclude_radio.setObjectName("files_exclude_radio")

        self.files_all_radio = QtWidgets.QRadioButton(self.files_tab)
        self.files_all_radio.setGeometry(QtCore.QRect(20, 110, 121, 21))
        self.files_all_radio.setObjectName("files_all_radio")

        files_btn_group = QtWidgets.QButtonGroup(self.files_tab)
        files_btn_group.setExclusive(True)
        files_btn_group.addButton(self.files_none_radio)
        files_btn_group.addButton(self.files_selected_radio)
        files_btn_group.addButton(self.files_exclude_radio)
        files_btn_group.addButton(self.files_all_radio)

        # type list and combobox
        self.listView = QtWidgets.QListView(self.files_tab)
        self.listView.setGeometry(QtCore.QRect(210, 10, 221, 161))
        self.listView.setObjectName("listView")

        self.files_combo = QtWidgets.QComboBox(self.files_tab)
        self.files_combo.setGeometry(QtCore.QRect(470, 80, 161, 22))
        self.files_combo.setObjectName("files_combo")

        self.add_btn = QtWidgets.QPushButton(self.files_tab)
        self.add_btn.setGeometry(QtCore.QRect(660, 77, 81, 26))
        self.add_btn.setObjectName("add_btn")

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("create_window", "create"))

        # labels
        self.name_label.setText(_translate("create_window", "Name"))
        self.desc_label.setText(_translate("create_window", "Description"))
        self.repeat_label.setText(_translate("create_window", "Repeat every"))
        self.type_label.setText(_translate("create_window", "Type"))
        self.time_label.setText(_translate("create_window", "Time"))
        self.day_month_label.setText(_translate("create_window", "Day of month"))
        self.origin_label.setText(_translate("create_window", "Originpath"))
        self.include_dir_label.setText(_translate("create_window", "Include directories?"))
        self.dest_label.setText(_translate("create_window", "Destinationpath"))

        # buttons
        self.save_btn.setText(_translate("create_window", "save"))
        self.cancel_btn.setText(_translate("create_window", "cancel"))
        self.origin_tool_btn.setText(_translate("create_window", "..."))
        self.dest_tool_btn.setText(_translate("create_window", "..."))
        self.add_btn.setText(_translate("create_window", "Add"))

        # tabs
        self.tab_bar.setTabText(self.tab_bar.indexOf(self.dir_tab), _translate("create_window", "Directory"))
        self.tab_bar.setTabText(self.tab_bar.indexOf(self.files_tab), _translate("create_window", "Files"))

        # radio buttons
        self.main_manual_radio.setText(_translate("create_window", "Manual"))
        self.main_interval_radio.setText(_translate("create_window", "Interval"))
        self.main_datetime_radio.setText(_translate("create_window", "Date/Time"))
        self.main_newest_radio.setText(_translate("create_window", "Newest"))
        self.dir_none_radio.setText(_translate("create_window", "None"))
        self.dir_empty_radio.setText(_translate("create_window", "Empty"))
        self.dir_filled_radio.setText(_translate("create_window", "Filled"))
        self.dir_all_radio.setText(_translate("create_window", "All"))
        self.files_none_radio.setText(_translate("create_window", "None"))
        self.files_selected_radio.setText(_translate("create_window", "Selected types"))
        self.files_exclude_radio.setText(_translate("create_window", "Exclude types"))
        self.files_all_radio.setText(_translate("create_window", "All"))

    def load_combo_values(self, combobox: QtWidgets.QComboBox, values: type[Enum]) -> None:
        combobox.clear()

        for value in values:
            combobox.addItem(value.value, value)

    def close_window(self) -> None:
        self.close()

    def save_entry(self) -> None:
        name = self.name_input.text()
        print(name)
        self.close_window()

    def type_combo_changed(self, index:int) -> None:
        value = self.type_combo.currentData()
        enabled = value != TypeComboValues.DELETE
        self.dest_label.setEnabled(enabled)
        self.dest_input.setEnabled(enabled)
        self.dest_tool_btn.setEnabled(enabled)

    def main_radio_changed(self, button: QtWidgets.QAbstractButton) -> None:
        group = button.group()
        btn_id = group.id(button)
        is_interval_btn = btn_id != 2
        is_date_time_btn = btn_id != 3

        self.repeat_label.setHidden(is_interval_btn)
        self.repeat_spin.setHidden(is_interval_btn)
        self.interval_type_combo.setHidden(is_interval_btn)

        self.day_month_label.setHidden(is_date_time_btn)
        self.day_month_spin.setHidden(is_date_time_btn)
        self.time_label.setHidden(is_date_time_btn)
        self.time_edit.setHidden(is_date_time_btn)

    def open_file_explorer(self):
        file_dialog = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select directory",
            directory="",
            options=QtWidgets.QFileDialog.Option.DontUseNativeDialog,
        )

        if file_dialog.strip() == "":
            return

        button = self.sender()
        if button == self.origin_tool_btn:
            self.origin_input.setText(file_dialog)
        else:
            self.dest_input.setText(file_dialog)

