from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QFileDialog, QWidget
from pathlib import Path
import platform
from pathvalidate import is_valid_filepath
from datetime import datetime, timedelta
from calendar import monthrange
from ..views.create_window import CreateWindow
from ..database.queries import db_call, create_entry, edit_entry, get_file_types, create_file_types, edit_file_types
from ..entities.entry import Entry
from ..entities.enums import TypeComboValues, IntervalTypeComboValues
from ..models.create_window_model import TypeListModel
from ..models.main_window_model import TableModel
from ..views.error_window import ErrorWindow
from ..utils.calculate_next_run import calculate_next_run

class CreateController:
    def __init__(self, parent: QWidget, table_model: TableModel, row: Entry | None = None):
        self.parent = parent
        self.row = row
        self.mode = "create" if not row else "edit"

        self.view = CreateWindow()
        self.model = self._create_type_model()
        self.parent_model = table_model

        self.view.set_model(self.model)

        self._connect_signals()
        self._setup_initial_state()

    def _create_type_model(self) -> TypeListModel:
        if self.mode == "create":
            return TypeListModel()
        
        result = db_call(get_file_types, self.row.id)
        if not result.get("success"):
            ErrorWindow(f"Failed to load file types.\n{result.get('error')}").exec()
            return TypeListModel()

        data = [r[0] for r in result.get("data")]
        return TypeListModel(data)
    
    def _connect_signals(self):
        self.view.type_combo.currentIndexChanged.connect(self.type_combo_changed)
        self.view.main_radio_group.buttonClicked.connect(self.main_radio_changed)

        self.view.origin_tool_btn.clicked.connect(self.open_file_explorer)
        self.view.dest_tool_btn.clicked.connect(self.open_file_explorer)

        self.view.add_btn.clicked.connect(self.add_type_to_list)
        self.view.type_list.doubleClicked.connect(self.remove_type)

        self.view.save_btn.clicked.connect(self.save_entry)
        self.view.cancel_btn.clicked.connect(self.view.close)

    def _setup_initial_state(self):
        self.view.load_combo_values(self.view.type_combo, TypeComboValues)
        self.view.load_combo_values(self.view.interval_type_combo, IntervalTypeComboValues)
        self.view.set_radio_by_text(self.view.main_radio_group, "manually")

        if self.mode == "edit":
            self.update_fields()

    def type_combo_changed(self) -> None:
        value = self.view.type_combo.currentData()
        enabled = value != TypeComboValues.DELETE

        if not enabled:
            self.view.remove_required_field(self.view.dest_input)
        else:
            self.view.add_required_field(self.view.dest_input)

    def main_radio_changed(self, button: QtWidgets.QAbstractButton) -> None:
        v = self.view
        group = button.group()
        btn_id = group.id(button)
        v.stack_widget.hide()

        if btn_id == 2: # interval
            v.config_stack.setCurrentIndex(0)
            v.stack_widget.show()
        elif btn_id == 3: # date/time
            v.config_stack.setCurrentIndex(1)
            v.stack_widget.show()

    def open_file_explorer(self) -> None:
        v = self.view
        file_dialog = QFileDialog.getExistingDirectory(
            parent=v,
            caption="Select directory",
            directory="",
            options=QFileDialog.Option.DontUseNativeDialog,
        )

        if file_dialog.strip() == "":
            return

        button = v.sender()
        if button == v.origin_tool_btn:
            v.origin_input.setText(file_dialog)
        else:
            v.dest_input.setText(file_dialog)

    def add_type_to_list(self) -> None:
        value = self.view.files_combo.currentText().strip().lower().replace(" ", "")
        
        if not value.startswith(".") and value != "":
            value = "." + value

        if value not in self.model.types:
            self.model.add(value)
            self.view.files_combo.setCurrentText("")

    def remove_type(self, index: QtCore.QModelIndex) -> None:
        self.model.delete(index.row())

    def update_fields(self) -> None:
        v = self.view
        v.name_input.setText(self.row.name.strip())
        v.desc_input.insertPlainText(self.row.description.strip())
        v.set_combo_value(v.type_combo, TypeComboValues[self.row.type.strip()])
        v.activate_check.setChecked(True if self.row.state != 0 else False)
        v.set_radio_by_text(v.main_radio_group, self.row.interval_type.strip())
        
        if self.row.interval_type.strip() == "interval":
            v.repeat_spin.setValue(self.row.schedule_value)
            v.set_combo_value(v.interval_type_combo, IntervalTypeComboValues[self.row.schedule_type.strip()])
        elif self.row.interval_type.strip() == "date/time":
            v.day_month_spin.setValue(self.row.schedule_value)
            v.time_edit.setTime(QtCore.QTime.fromString(self.row.schedule_type.strip(), "HH:mm:ss"))

        v.origin_input.setText(self.row.originpath.strip())

        if self.row.destpath.strip() != "":
            v.dest_input.setText(self.row.destpath.strip())

        v.set_radio_by_text(v.dir_btn_group, self.row.include_dir.strip())
        v.set_radio_by_text(v.files_btn_group, self.row.include_files.strip())

    def save_entry(self) -> None:
        v = self.view
        required_fields = v.get_required_fields()
        if not self.form_is_valid():
            ErrorWindow("Please ensure that all required (*) fields are filled.").exec()
            return
        
        dest_path = v.dest_input.text().strip()
        origin_path = v.origin_input.text().strip()

        if v.dest_input in required_fields and dest_path == origin_path:
            ErrorWindow("Please ensure that the destination- and originpath are not the same.").exec()
            return 
        
        dest_valid = self.path_is_valid(dest_path)
        origin_valid = self.path_is_valid(origin_path)

        if (not dest_valid and v.desc_input in required_fields) or not origin_valid:
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

        main_group = v.main_radio_group.checkedButton().text() 

        if main_group == "interval":
            schedule_value = v.repeat_spin.value()
            schedule_type = v.interval_type_combo.currentData().name
        elif main_group == "date/time":
            schedule_value = v.day_month_spin.value()
            schedule_type = v.time_edit.time().toString("HH:mm:ss")

        if v.dest_input in required_fields:
            destpath = v.dest_input.text().strip()

        entry = Entry(
            id = None,
            name=v.name_input.text(),
            description=v.desc_input.toPlainText().strip(),
            type=v.type_combo.currentData().name,
            interval_type=main_group,
            schedule_type=schedule_type,
            schedule_value=schedule_value,
            originpath=v.origin_input.text().strip(),
            destpath=destpath,
            include_dir=v.dir_btn_group.checkedButton().text(),
            include_files=v.files_btn_group.checkedButton().text(),
            state=1 if v.activate_check.isChecked() else 0
        )
        file_types = self.model.get_data()
        next_run = calculate_next_run(main_group, schedule_type, schedule_value) if main_group != "manually" else None

        if self.mode == "create":
            result = db_call(create_entry, entry, next_run)

            if not result.get("success"):
                ErrorWindow(f"Something went wrong while creating the entry.\n{result.get("error")}").exec()
                return
            
            file_type_result = db_call(create_file_types, result.get("data"), file_types)

            if not file_type_result.get("success"):
                ErrorWindow(f"Something went wrong while creating the file types.\n{file_type_result.get("error")}").exec()
                return 
        else: 
            entry.id = self.row.id
            result = db_call(edit_entry, entry, next_run) 

            if not result.get("success"):
                ErrorWindow(f"Something went wrong while editing the entry.\n{result.get("error")}").exec()
                return
            
            file_type_result = db_call(edit_file_types, self.row.id, file_types)

            if not file_type_result.get("success"):
                ErrorWindow(f"Something went wrong while editing the file types.\n{file_type_result.get("error")}").exec()
                return 

        v.close()
        self.parent_model.load()

    def form_is_valid(self) -> bool:
        for field in self.view.get_required_fields():
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
        
        return is_valid_filepath(path, platform=user_platform)