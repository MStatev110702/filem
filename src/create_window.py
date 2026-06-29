from PyQt6 import QtCore, QtGui, QtWidgets
from enum import Enum
import platform
from pathlib import Path
from pathvalidate import is_valid_filepath
from .error_window import ErrorWindow
from .sqlite import create_entry, edit_entry
from .entry import Entry
from .create_window_enums import TypeComboValues, IntervalTypeComboValues
from .type_list_model import TypeListModel

class CreateWindow(QtWidgets.QWidget):
    def __init__(self, parent:QtWidgets.QWidget, row: Entry|None=None) -> None:
        super().__init__()
        self.init_ui()
        self.parent = parent
        self.mode = "create" if not row else "edit"
        self.row = row
        self.required_fields = [self.name_input, self.origin_input]
        self.main_manual_radio.click()
        if self.mode == "edit":
            self.update_fields()
        self.type_combo_changed()
    
    def init_ui(self) -> None:
        # general window settings
        self.setObjectName("create_window")
        self.resize(750, 550)

        main_layout = QtWidgets.QVBoxLayout(self)

        # name, description and type input fields with their labels
        form = QtWidgets.QGridLayout()
        
        self.name_label = QtWidgets.QLabel()
        self.name_label.setObjectName("name_label")

        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setObjectName("name_input")
        self.name_input.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Fixed
        )

        self.desc_label = QtWidgets.QLabel()
        self.desc_label.setObjectName("desc_label")

        self.desc_input = QtWidgets.QTextEdit()
        self.desc_input.setObjectName("desc_input")

        self.type_label = QtWidgets.QLabel()
        self.type_label.setObjectName("type_label")

        self.type_combo = QtWidgets.QComboBox()
        self.type_combo.setObjectName("type_combo")
        self.load_combo_values(self.type_combo, TypeComboValues)
        self.type_combo.currentIndexChanged.connect(self.type_combo_changed)

        form.addWidget(self.name_label, 0, 0)
        form.addWidget(self.name_input, 0, 1)

        form.addWidget(self.desc_label, 1, 0)
        form.addWidget(self.desc_input, 1, 1)

        form.addWidget(self.type_label, 2, 0)
        form.addWidget(self.type_combo, 2, 1)

        #--- main radio buttons ---
        radio_layout = QtWidgets.QHBoxLayout()

        # radio menu for selecting the start of the script
        self.main_manual_radio = QtWidgets.QRadioButton()
        self.main_manual_radio.setObjectName("main_manual_radio")

        self.main_interval_radio = QtWidgets.QRadioButton()
        self.main_interval_radio.setObjectName("main_interval_radio")

        self.main_datetime_radio = QtWidgets.QRadioButton()
        self.main_datetime_radio.setObjectName("main_datetime_radio")

        self.main_newest_radio = QtWidgets.QRadioButton()
        self.main_newest_radio.setObjectName("main_newest_radio")

        radio_layout.addWidget(self.main_manual_radio)
        radio_layout.addWidget(self.main_interval_radio)
        radio_layout.addWidget(self.main_datetime_radio)
        radio_layout.addWidget(self.main_newest_radio)
        radio_layout.addStretch()

        #--- main radio group ---
        self.main_radio_group = QtWidgets.QButtonGroup()
        self.main_radio_group.setExclusive(True)
        self.main_radio_group.addButton(self.main_manual_radio, 1)
        self.main_radio_group.addButton(self.main_interval_radio, 2)
        self.main_radio_group.addButton(self.main_datetime_radio, 3)
        self.main_radio_group.addButton(self.main_newest_radio, 4)
        self.main_radio_group.buttonClicked.connect(self.main_radio_changed)

        self.config_stack = QtWidgets.QStackedLayout()

        #--- interval fields ---
        interval_page = QtWidgets.QWidget()
        interval_layout = QtWidgets.QHBoxLayout(interval_page)

        self.repeat_label = QtWidgets.QLabel()
        self.repeat_label.setObjectName("repeat_label")

        self.repeat_spin = QtWidgets.QSpinBox()
        self.repeat_spin.setObjectName("repeat_spin")
        self.repeat_spin.setMinimum(1)

        self.interval_type_combo = QtWidgets.QComboBox()
        self.interval_type_combo.setObjectName("interval_type_combo")
        self.load_combo_values(self.interval_type_combo, IntervalTypeComboValues)

        interval_layout.addWidget(self.repeat_label)
        interval_layout.addWidget(self.repeat_spin)
        interval_layout.addWidget(self.interval_type_combo)

        #--- date/time fields ---
        datetime_page = QtWidgets.QWidget()
        datetime_layout = QtWidgets.QHBoxLayout(datetime_page)

        self.day_month_label = QtWidgets.QLabel()
        self.day_month_label.setObjectName("day_month_label")

        self.day_month_spin = QtWidgets.QSpinBox()
        self.day_month_spin.setObjectName("day_month_spin")
        self.day_month_spin.setMinimum(1)

        self.time_label = QtWidgets.QLabel()
        self.time_label.setObjectName("time_label")

        self.time_edit = QtWidgets.QTimeEdit()
        self.time_edit.setObjectName("time_edit")

        datetime_layout.addWidget(self.day_month_label)
        datetime_layout.addWidget(self.day_month_spin)
        datetime_layout.addWidget(self.time_label)
        datetime_layout.addWidget(self.time_edit)

        self.config_stack.addWidget(interval_page)
        self.config_stack.addWidget(datetime_page)

        self.stack_widget = QtWidgets.QWidget()
        self.stack_widget.setLayout(self.config_stack)

        # start of the tab widget
        self.tab_bar = QtWidgets.QTabWidget()
        self.tab_bar.setObjectName("tab_bar")

        self.dir_tab = QtWidgets.QWidget()
        self.dir_tab.setObjectName("dir_tab")

        self.files_tab = QtWidgets.QWidget()
        self.files_tab.setObjectName("files_tab")

        self.tab_bar.addTab(self.dir_tab, "")
        self.tab_bar.addTab(self.files_tab, "")
        self.tab_bar.setCurrentIndex(0)

        #--- directory tab ---
        dir_layout = QtWidgets.QGridLayout(self.dir_tab)

        # originpath
        self.origin_label = QtWidgets.QLabel(self.dir_tab)
        self.origin_label.setObjectName("origin_label")

        self.origin_input = QtWidgets.QLineEdit(self.dir_tab)
        self.origin_input.setObjectName("origin_input")

        self.origin_tool_btn = QtWidgets.QToolButton(self.dir_tab)
        self.origin_tool_btn.setObjectName("origin_tool_btn")
        self.origin_tool_btn.clicked.connect(self.open_file_explorer)

        # destinationpath
        self.dest_label = QtWidgets.QLabel(self.dir_tab)
        self.dest_label.setObjectName("dest_label")

        self.dest_input = QtWidgets.QLineEdit(self.dir_tab)
        self.dest_input.setObjectName("dest_input")

        self.dest_tool_btn = QtWidgets.QToolButton(self.dir_tab)
        self.dest_tool_btn.setObjectName("dest_tool_btn")
        self.dest_tool_btn.clicked.connect(self.open_file_explorer)

        dir_layout.addWidget(self.origin_label, 0, 0)
        dir_layout.addWidget(self.origin_input, 0, 1)
        dir_layout.addWidget(self.origin_tool_btn, 0, 2)

        dir_layout.addWidget(self.dest_label, 1, 0)
        dir_layout.addWidget(self.dest_input, 1, 1)
        dir_layout.addWidget(self.dest_tool_btn, 1, 2)

        # include directory radio buttons
        dir_radio_layout = QtWidgets.QHBoxLayout()

        self.dir_none_radio = QtWidgets.QRadioButton(self.dir_tab)
        self.dir_none_radio.setObjectName("dir_none_radio")
        self.dir_none_radio.setChecked(True)

        self.dir_empty_radio = QtWidgets.QRadioButton(self.dir_tab)
        self.dir_empty_radio.setObjectName("dir_empty_radio")

        self.dir_filled_radio = QtWidgets.QRadioButton(self.dir_tab)
        self.dir_filled_radio.setObjectName("dir_filled_radio")

        self.dir_all_radio = QtWidgets.QRadioButton(self.dir_tab)
        self.dir_all_radio.setObjectName("dir_all_radio")

        dir_radio_layout.addWidget(self.dir_none_radio)
        dir_radio_layout.addWidget(self.dir_empty_radio)
        dir_radio_layout.addWidget(self.dir_filled_radio)
        dir_radio_layout.addWidget(self.dir_all_radio)

        dir_layout.addLayout(dir_radio_layout, 2, 0, 1, 3)

        self.dir_btn_group = QtWidgets.QButtonGroup(self.dir_tab)
        self.dir_btn_group.setExclusive(True)
        self.dir_btn_group.addButton(self.dir_none_radio)
        self.dir_btn_group.addButton(self.dir_empty_radio)
        self.dir_btn_group.addButton(self.dir_filled_radio)
        self.dir_btn_group.addButton(self.dir_all_radio)

        #--- files tab ---
        files_layout = QtWidgets.QGridLayout(self.files_tab)
        
        # files radio buttons
        self.files_none_radio = QtWidgets.QRadioButton(self.files_tab)
        self.files_none_radio.setObjectName("files_none_radio")
        self.files_none_radio.setChecked(True)

        self.files_selected_radio = QtWidgets.QRadioButton(self.files_tab)
        self.files_selected_radio.setObjectName("files_selected_radio")

        self.files_exclude_radio = QtWidgets.QRadioButton(self.files_tab)
        self.files_exclude_radio.setObjectName("files_exclude_radio")

        self.files_all_radio = QtWidgets.QRadioButton(self.files_tab)
        self.files_all_radio.setObjectName("files_all_radio")

        files_radio_layout = QtWidgets.QHBoxLayout()
        files_radio_layout.addWidget(self.files_none_radio)
        files_radio_layout.addWidget(self.files_selected_radio)
        files_radio_layout.addWidget(self.files_exclude_radio)
        files_radio_layout.addWidget(self.files_all_radio)

        self.files_btn_group = QtWidgets.QButtonGroup(self.files_tab)
        self.files_btn_group.setExclusive(True)
        self.files_btn_group.addButton(self.files_none_radio)
        self.files_btn_group.addButton(self.files_selected_radio)
        self.files_btn_group.addButton(self.files_exclude_radio)
        self.files_btn_group.addButton(self.files_all_radio)

        # type list and combobox
        self.type_list = QtWidgets.QListView(self.files_tab)
        self.type_list.setObjectName("type_list")
        
        self.type_list_model = TypeListModel()
        self.type_list.setModel(self.type_list_model)
        self.type_list.doubleClicked.connect(self.remove_type)

        self.files_combo = QtWidgets.QComboBox(self.files_tab)
        self.files_combo.setObjectName("files_combo")
        self.files_combo.setEditable(True)

        self.add_btn = QtWidgets.QPushButton(self.files_tab)
        self.add_btn.setObjectName("add_btn")
        self.add_btn.clicked.connect(self.add_type_to_list)

        files_layout.addWidget(self.type_list, 0, 0, 3, 1)

        files_layout.addWidget(self.files_combo, 0, 1)
        files_layout.addWidget(self.add_btn, 1, 1)
        files_layout.addLayout(files_radio_layout, 2, 1)

        self.dir_tab.setLayout(dir_layout)
        self.files_tab.setLayout(files_layout)

        #--- statusbar ---
        statusbar_layout = QtWidgets.QHBoxLayout()
        self.save_btn = QtWidgets.QPushButton()
        self.save_btn.setObjectName("save_btn")
        self.save_btn.clicked.connect(self.save_entry)

        self.cancel_btn = QtWidgets.QPushButton()
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.clicked.connect(self.close_window)

        statusbar_layout.addStretch()
        statusbar_layout.addWidget(self.save_btn)
        statusbar_layout.addWidget(self.cancel_btn)

        main_layout.addLayout(form)
        main_layout.addLayout(radio_layout)
        main_layout.addWidget(self.stack_widget)
        main_layout.addWidget(self.tab_bar)
        main_layout.addLayout(statusbar_layout)

        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("create_window", "create"))

        # labels
        self.name_label.setText(_translate("create_window", "*Name"))
        self.desc_label.setText(_translate("create_window", "Description"))
        self.repeat_label.setText(_translate("create_window", "Repeat every"))
        self.type_label.setText(_translate("create_window", "Type"))
        self.time_label.setText(_translate("create_window", "Time"))
        self.day_month_label.setText(_translate("create_window", "Day of month"))
        self.origin_label.setText(_translate("create_window", "*Originpath"))
        self.dest_label.setText(_translate("create_window", "*Destinationpath"))

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
        self.main_manual_radio.setText(_translate("create_window", "manually"))
        self.main_interval_radio.setText(_translate("create_window", "interval"))
        self.main_datetime_radio.setText(_translate("create_window", "date/time"))
        self.main_newest_radio.setText(_translate("create_window", "newest"))
        self.dir_none_radio.setText(_translate("create_window", "none"))
        self.dir_empty_radio.setText(_translate("create_window", "empty"))
        self.dir_filled_radio.setText(_translate("create_window", "filled"))
        self.dir_all_radio.setText(_translate("create_window", "all"))
        self.files_none_radio.setText(_translate("create_window", "none"))
        self.files_selected_radio.setText(_translate("create_window", "selected types"))
        self.files_exclude_radio.setText(_translate("create_window", "exclude types"))
        self.files_all_radio.setText(_translate("create_window", "all"))

    def load_combo_values(self, combobox: QtWidgets.QComboBox, values: type[Enum]) -> None:
        combobox.clear()

        for value in values:
            combobox.addItem(value.value, value)

    def close_window(self) -> None:
        self.close()

    def save_entry(self) -> None:
        if not self.form_is_valid():
            ErrorWindow("Please ensure that all required (*) fields are filled.").exec()
            return
        
        dest_path = self.dest_input.text().strip()
        origin_path = self.origin_input.text().strip()

        if self.dest_input in self.required_fields and dest_path == origin_path:
            ErrorWindow("Please ensure that the destination- and originpath are not the same.").exec()
            return 
        
        dest_valid = self.path_is_valid(dest_path)
        origin_valid = self.path_is_valid(origin_path)

        if not dest_valid or not origin_valid:
            invalid_paths = []

            if not origin_valid:
                invalid_paths.append("originpath")

            if not dest_valid:
                invalid_paths.append("destinationpath")

            ErrorWindow(f"The {' and '.join(invalid_paths)} is/are invalid").exec()
            return  
        
        schedule_value = 0
        schedule_type = ""
        destpath = ""
        file_types = ""

        main_group = self.main_radio_group.checkedButton().text() 

        if main_group == "interval":
            schedule_value = self.repeat_spin.value()
            schedule_type = self.interval_type_combo.currentData().name
        elif main_group == "date/time":
            schedule_value = self.day_month_spin.value()
            schedule_type = self.time_edit.time().toString("HH:mm:ss")

        if self.dest_input in self.required_fields:
            destpath = self.dest_input.text().strip()

        entry = Entry(
            id = None,
            name=self.name_input.text(),
            description=self.desc_input.toPlainText().strip(),
            type=self.type_combo.currentData().name,
            interval_type=main_group,
            schedule_type=schedule_type,
            schedule_value=schedule_value,
            originpath=self.origin_input.text().strip(),
            destpath=destpath,
            include_dir=self.dir_btn_group.checkedButton().text(),
            include_files=self.files_btn_group.checkedButton().text(),
            file_types=file_types
        )

        if self.mode == "create":
            success = create_entry(entry) 
        else: 
            entry.id = self.row.id
            success = edit_entry(entry)

        if not success:
            ErrorWindow("Something went wrong while saving the entry.").exec()
            return 

        self.close_window()
        self.parent.model.load()

    def form_is_valid(self) -> bool:
        for field in self.required_fields:
            if field.text().strip() == "":
                return False

        return True
    
    def path_is_valid(self, path: str) -> bool:
        system = platform.system()

        if system == "Windows":
            user_platform = "windows"
            is_abs = path.startswith("\\") or (len(path) > 2 and path[1:3] == ":\\")
        elif system == "Linux":
            user_platform = "linux"
            is_abs = path.startswith("/")
        elif system == "Darwin":
            user_platform = "macos"
            is_abs = path.startswith("/")
        else:
            user_platform = "universal"
            return False

        if not is_abs:
            return False

        if "." in Path(path).name:
            return False
        
        return is_valid_filepath(path, platform=user_platform)
    def type_combo_changed(self) -> None:
        value = self.type_combo.currentData()
        enabled = value != TypeComboValues.DELETE
        
        self.dest_label.setEnabled(enabled)
        self.dest_input.setEnabled(enabled)
        self.dest_tool_btn.setEnabled(enabled)

        if not enabled and self.dest_input in self.required_fields:
            self.required_fields.remove(self.dest_input)
        else:
            self.required_fields.append(self.dest_input)

    def main_radio_changed(self, button: QtWidgets.QAbstractButton) -> None:
        group = button.group()
        btn_id = group.id(button)
        self.stack_widget.hide()

        if btn_id == 2:
            self.config_stack.setCurrentIndex(0)
            self.stack_widget.show()
        elif btn_id == 3:
            self.config_stack.setCurrentIndex(1)
            self.stack_widget.show()

    def open_file_explorer(self) -> None:
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

    def add_type_to_list(self) -> None:
        value = self.files_combo.currentText().strip()
        model = self.type_list_model
        if value not in model.types and value != "":
            model.add(value)
    
    def remove_type(self, index: QtCore.QModelIndex) -> None:
        self.type_list_model.delete(index.row())

    def set_combo_value(self, combobox: QtWidgets.QComboBox, value: type[Enum]) -> None:      
        index = combobox.findData(value)

        if index != -1:
            combobox.setCurrentIndex(index)

    def set_radio_by_text(self, group: QtWidgets.QButtonGroup, text: str):
        for button in group.buttons():
            if button.text() == text:
                button.click()
        
    def update_fields(self) -> None:
        self.name_input.setText(self.row.name.strip())
        self.desc_input.insertPlainText(self.row.description.strip())
        self.set_combo_value(self.type_combo, TypeComboValues[self.row.type.strip()])
        self.set_radio_by_text(self.main_radio_group, self.row.interval_type.strip())
        
        if self.row.interval_type.strip() == "interval":
            self.repeat_spin.setValue(self.row.schedule_value)
            self.set_combo_value(self.interval_type_combo, IntervalTypeComboValues[self.row.schedule_type.strip()])
        elif self.row.interval_type.strip() == "date/time":
            self.day_month_spin.setValue(self.row.schedule_value)
            self.time_edit.setTime(QtCore.QTime.fromString(self.row.schedule_type.strip(), "HH:mm:ss"))

        self.origin_input.setText(self.row.originpath.strip())

        if self.row.destpath.strip() != "":
            self.dest_input.setText(self.row.destpath.strip())

        self.set_radio_by_text(self.dir_btn_group, self.row.include_dir.strip())
        self.set_radio_by_text(self.files_btn_group, self.row.include_files.strip())

                