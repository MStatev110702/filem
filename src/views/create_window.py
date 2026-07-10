from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QStackedLayout, QLabel, QLineEdit, QSizePolicy, QTextEdit, QComboBox, QSpinBox, QRadioButton, QButtonGroup, QTimeEdit, QTabWidget, QListView, QToolButton, QPushButton, QCheckBox
from enum import Enum
from ..models.create_window_model import TypeListModel
from ..entities.enums import TypeComboValues

class CreateWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.required_fields = []
        self.init_ui()
        self._setup_required_field()
    
    def init_ui(self) -> None:
        # general window settings
        self.setObjectName("create_window")
        self.resize(750, 550)

        main_layout = QVBoxLayout(self)

        # name, description and type input fields with their labels
        form = QGridLayout()
        
        self.name_label = QLabel()
        self.name_label.setObjectName("name_label")

        self.name_input = QLineEdit()
        self.name_input.setObjectName("name_input")
        self.name_input.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        self.desc_label = QLabel()
        self.desc_label.setObjectName("desc_label")

        self.desc_input = QTextEdit()
        self.desc_input.setObjectName("desc_input")

        self.type_label = QLabel()
        self.type_label.setObjectName("type_label")

        self.type_combo = QComboBox()
        self.type_combo.setObjectName("type_combo")
        self.type_combo.currentIndexChanged.connect(self.type_combo_changed)

        self.activate_check = QCheckBox()
        self.activate_check.setObjectName("activate_check")
        self.activate_check.setChecked(True)

        form.addWidget(self.name_label, 0, 0)
        form.addWidget(self.name_input, 0, 1)

        form.addWidget(self.desc_label, 1, 0)
        form.addWidget(self.desc_input, 1, 1)

        form.addWidget(self.type_label, 2, 0)
        form.addWidget(self.type_combo, 2, 1)

        form.addWidget(self.activate_check)
        #--- main radio buttons ---
        radio_layout = QHBoxLayout()

        # radio menu for selecting the start of the script
        self.main_manual_radio = QRadioButton()
        self.main_manual_radio.setObjectName("main_manual_radio")
        self.main_manual_radio.setChecked(True)

        self.main_interval_radio = QRadioButton()
        self.main_interval_radio.setObjectName("main_interval_radio")

        self.main_datetime_radio = QRadioButton()
        self.main_datetime_radio.setObjectName("main_datetime_radio")

        #self.main_newest_radio = QRadioButton()
        #self.main_newest_radio.setObjectName("main_newest_radio")

        radio_layout.addWidget(self.main_manual_radio)
        radio_layout.addWidget(self.main_interval_radio)
        radio_layout.addWidget(self.main_datetime_radio)
        #radio_layout.addWidget(self.main_newest_radio)
        radio_layout.addStretch()

        #--- main radio group ---
        self.main_radio_group = QButtonGroup()
        self.main_radio_group.setExclusive(True)
        self.main_radio_group.addButton(self.main_manual_radio, 1)
        self.main_radio_group.addButton(self.main_interval_radio, 2)
        self.main_radio_group.addButton(self.main_datetime_radio, 3)
        #self.main_radio_group.addButton(self.main_newest_radio, 4)

        self.config_stack = QStackedLayout()

        #--- interval fields ---
        interval_page = QWidget()
        interval_layout = QHBoxLayout(interval_page)

        self.repeat_label = QLabel()
        self.repeat_label.setObjectName("repeat_label")

        self.repeat_spin = QSpinBox()
        self.repeat_spin.setObjectName("repeat_spin")
        self.repeat_spin.setMinimum(1)

        self.interval_type_combo = QComboBox()
        self.interval_type_combo.setObjectName("interval_type_combo")

        interval_layout.addWidget(self.repeat_label)
        interval_layout.addWidget(self.repeat_spin)
        interval_layout.addWidget(self.interval_type_combo)

        #--- date/time fields ---
        datetime_page = QWidget()
        datetime_layout = QHBoxLayout(datetime_page)

        self.day_month_label = QLabel()
        self.day_month_label.setObjectName("day_month_label")

        self.day_month_spin = QSpinBox()
        self.day_month_spin.setObjectName("day_month_spin")
        self.day_month_spin.setMinimum(1)
        self.day_month_spin.setMaximum(31)

        self.time_label = QLabel()
        self.time_label.setObjectName("time_label")

        self.time_edit = QTimeEdit()
        self.time_edit.setObjectName("time_edit")

        datetime_layout.addWidget(self.day_month_label)
        datetime_layout.addWidget(self.day_month_spin)
        datetime_layout.addWidget(self.time_label)
        datetime_layout.addWidget(self.time_edit)

        self.config_stack.addWidget(interval_page)
        self.config_stack.addWidget(datetime_page)

        self.stack_widget = QWidget()
        self.stack_widget.setLayout(self.config_stack)

        # start of the tab widget
        self.tab_bar = QTabWidget()
        self.tab_bar.setObjectName("tab_bar")

        self.dir_tab = QWidget()
        self.dir_tab.setObjectName("dir_tab")

        self.files_tab = QWidget()
        self.files_tab.setObjectName("files_tab")

        self.tab_bar.addTab(self.dir_tab, "")
        self.tab_bar.addTab(self.files_tab, "")
        self.tab_bar.setCurrentIndex(0)

        #--- directory tab ---
        dir_layout = QGridLayout(self.dir_tab)

        # originpath
        self.origin_label = QLabel(self.dir_tab)
        self.origin_label.setObjectName("origin_label")

        self.origin_input = QLineEdit(self.dir_tab)
        self.origin_input.setObjectName("origin_input")

        self.origin_tool_btn = QToolButton(self.dir_tab)
        self.origin_tool_btn.setObjectName("origin_tool_btn")

        # destinationpath
        self.dest_label = QLabel(self.dir_tab)
        self.dest_label.setObjectName("dest_label")

        self.dest_input = QLineEdit(self.dir_tab)
        self.dest_input.setObjectName("dest_input")

        self.dest_tool_btn = QToolButton(self.dir_tab)
        self.dest_tool_btn.setObjectName("dest_tool_btn")

        dir_layout.addWidget(self.origin_label, 0, 0)
        dir_layout.addWidget(self.origin_input, 0, 1)
        dir_layout.addWidget(self.origin_tool_btn, 0, 2)

        dir_layout.addWidget(self.dest_label, 1, 0)
        dir_layout.addWidget(self.dest_input, 1, 1)
        dir_layout.addWidget(self.dest_tool_btn, 1, 2)

        # include directory radio buttons
        dir_radio_layout = QHBoxLayout()

        self.dir_none_radio = QRadioButton(self.dir_tab)
        self.dir_none_radio.setObjectName("dir_none_radio")
        self.dir_none_radio.setChecked(True)

        self.dir_empty_radio = QRadioButton(self.dir_tab)
        self.dir_empty_radio.setObjectName("dir_empty_radio")

        self.dir_filled_radio = QRadioButton(self.dir_tab)
        self.dir_filled_radio.setObjectName("dir_filled_radio")

        self.dir_all_radio = QRadioButton(self.dir_tab)
        self.dir_all_radio.setObjectName("dir_all_radio")

        dir_radio_layout.addWidget(self.dir_none_radio)
        dir_radio_layout.addWidget(self.dir_empty_radio)
        dir_radio_layout.addWidget(self.dir_filled_radio)
        dir_radio_layout.addWidget(self.dir_all_radio)

        dir_layout.addLayout(dir_radio_layout, 2, 0, 1, 3)

        self.dir_btn_group = QButtonGroup(self.dir_tab)
        self.dir_btn_group.setExclusive(True)
        self.dir_btn_group.addButton(self.dir_none_radio)
        self.dir_btn_group.addButton(self.dir_empty_radio)
        self.dir_btn_group.addButton(self.dir_filled_radio)
        self.dir_btn_group.addButton(self.dir_all_radio)

        #--- files tab ---
        files_layout = QGridLayout(self.files_tab)
        
        # files radio buttons
        self.files_none_radio = QRadioButton(self.files_tab)
        self.files_none_radio.setObjectName("files_none_radio")
        self.files_none_radio.setChecked(True)

        self.files_selected_radio = QRadioButton(self.files_tab)
        self.files_selected_radio.setObjectName("files_selected_radio")

        self.files_exclude_radio = QRadioButton(self.files_tab)
        self.files_exclude_radio.setObjectName("files_exclude_radio")

        self.files_all_radio = QRadioButton(self.files_tab)
        self.files_all_radio.setObjectName("files_all_radio")

        files_radio_layout = QHBoxLayout()
        files_radio_layout.addWidget(self.files_none_radio)
        files_radio_layout.addWidget(self.files_selected_radio)
        files_radio_layout.addWidget(self.files_exclude_radio)
        files_radio_layout.addWidget(self.files_all_radio)

        self.files_btn_group = QButtonGroup(self.files_tab)
        self.files_btn_group.setExclusive(True)
        self.files_btn_group.addButton(self.files_none_radio)
        self.files_btn_group.addButton(self.files_selected_radio)
        self.files_btn_group.addButton(self.files_exclude_radio)
        self.files_btn_group.addButton(self.files_all_radio)

        # type list and combobox
        self.type_list = QListView(self.files_tab)
        self.type_list.setObjectName("type_list")
        self.type_list.setModel(None)

        self.files_combo = QComboBox(self.files_tab)
        self.files_combo.setObjectName("files_combo")
        self.files_combo.setEditable(True)

        self.add_btn = QPushButton(self.files_tab)
        self.add_btn.setObjectName("add_btn")

        files_layout.addWidget(self.type_list, 0, 0, 3, 1)
        files_layout.addWidget(self.files_combo, 0, 1)
        files_layout.addWidget(self.add_btn, 1, 1)
        files_layout.addLayout(files_radio_layout, 2, 1)

        self.dir_tab.setLayout(dir_layout)
        self.files_tab.setLayout(files_layout)

        #--- statusbar ---
        statusbar_layout = QHBoxLayout()
        self.save_btn = QPushButton()
        self.save_btn.setObjectName("save_btn")

        self.cancel_btn = QPushButton()
        self.cancel_btn.setObjectName("cancel_btn")

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
        #self.main_newest_radio.setText(_translate("create_window", "newest"))
        self.dir_none_radio.setText(_translate("create_window", "none"))
        self.dir_empty_radio.setText(_translate("create_window", "empty"))
        self.dir_filled_radio.setText(_translate("create_window", "filled"))
        self.dir_all_radio.setText(_translate("create_window", "all"))
        self.files_none_radio.setText(_translate("create_window", "none"))
        self.files_selected_radio.setText(_translate("create_window", "selected types"))
        self.files_exclude_radio.setText(_translate("create_window", "exclude types"))
        self.files_all_radio.setText(_translate("create_window", "all"))

        #checkbox
        self.activate_check.setText(_translate("create_window", "activate"))

    def _setup_required_field(self):
        self.required_fields = [
            self.name_input,
            self.origin_input,
        ]

    def add_required_field(self, widget):
        if widget not in self.required_fields:
            self.required_fields.append(widget)

    def remove_required_field(self, widget):
        if widget in self.required_fields:
            self.required_fields.remove(widget)

    def get_required_fields(self) -> list:
        return self.required_fields

    def set_model(self, model: TypeListModel):
        self.type_list.setModel(model)

    def load_combo_values(self, combobox: QComboBox, values: type[Enum]) -> None:
        combobox.clear()

        for value in values:
            combobox.addItem(value.value, value)
    
    def set_combo_value(self, combobox: QComboBox, value: type[Enum]) -> None:
        index = combobox.findData(value)

        if index != -1:
            combobox.setCurrentIndex(index)

    def set_radio_by_text(self, group: QButtonGroup, text: str):
        for button in group.buttons():
            if button.text() == text:
                button.click()

    def type_combo_changed(self) -> None:
        value = self.type_combo.currentData()
        enabled = value != TypeComboValues.DELETE
        
        self.dest_label.setEnabled(enabled)
        self.dest_input.setEnabled(enabled)
        self.dest_tool_btn.setEnabled(enabled)