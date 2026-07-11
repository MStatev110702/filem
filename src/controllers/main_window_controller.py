from PyQt6.QtCore import Qt
from .create_window_controller import CreateController
from ..entities.entry import Entry
from ..database.queries import db_call, get_selected_entry, delete_entry
from ..models.main_window_model import TableModel
from ..views.main_window import MainWindow
from ..views.error_window import ErrorWindow
from ..utils.start_entry import start_entry

class MainController:
    def __init__(self):
        self.view = MainWindow()
        self.model = TableModel()
        self.create_controller = None

        self.view.set_model(self.model)

        self.view.search_btn.clicked.connect(self.search_entries)
        self.view.create_btn.clicked.connect(self.open_create_window)
        self.view.delete_btn.clicked.connect(self.delete_selected_entry)
        self.view.edit_btn.clicked.connect(self.open_edit_window)
        self.view.start_btn.clicked.connect(self.start_selected_entry)
        self.view.script_table.doubleClicked.connect(self.open_edit_window)

    def open_create_window(self):
        self.create_controller = CreateController(self.view, self.model)
        self.create_controller.view.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.create_controller.view.show()

    def delete_selected_entry(self):
        index = self.view.script_table.selectionModel().currentIndex()

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
        self.model.load(self.view.search_input.text().strip())

    def open_edit_window(self):
        index = self.view.script_table.selectionModel().currentIndex()

        if index.row() == -1:
            ErrorWindow("Please select one row in the table.").exec()
            return
        
        row_id = self.model.get_row_id(index)
        result = db_call(get_selected_entry, row_id)

        if not result.get("success"):
            ErrorWindow(f"Failed to retrieve the entry with the id: {row_id}").exec()
            return

        entry = Entry.from_row(result.get("data"))
        
        self.create_controller = CreateController(self.view, self.model, entry)
        self.create_controller.view.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.create_controller.view.show()

    def start_selected_entry(self):
        index = self.view.script_table.selectionModel().currentIndex()

        if index.row() == -1:
            ErrorWindow("Please select one row in the table.").exec()
            return
        
        row_id = self.model.get_row_id(index)
        start_entry(row_id)
        
