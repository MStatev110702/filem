import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path 
from PyQt6 import QtWidgets
import sys
from src.controllers.create_window_controller import CreateController
from src.entities.enums import TypeComboValues

app = QtWidgets.QApplication(sys.argv)

class TestCreateWindow(unittest.TestCase):
    def setUp(self):
        self.main_view = MagicMock()
        self.main_model = MagicMock()
        self.controller = CreateController(self.main_view, self.main_model)
        self.view = self.controller.view

    #--- form validation tests ---

    def test_form_is_valid_valid_default_fields(self):
        self.view.name_input.setText("Test Case")
        self.view.origin_input.setText("/valid/path")
        self.view.required_fields = [
            self.view.name_input, 
            self.view.origin_input
        ]

        self.assertTrue(self.controller.form_is_valid())

    def test_form_is_valid_valid(self):
        self.view.name_input.setText("Test Case")
        self.view.origin_input.setText("/valid/path")
        self.view.dest_input.setText("/valid/dest")
        self.view.required_fields = [
            self.view.name_input, 
            self.view.origin_input, 
            self.view.dest_input
        ]

        self.assertTrue(self.controller.form_is_valid())

    def test_form_is_valid_empty_values(self):       
        self.view.name_input.setText("")
        self.view.origin_input.setText("")
        self.view.dest_input.setText("")
        self.view.required_fields = [
            self.view.name_input, 
            self.view.origin_input, 
            self.view.dest_input
        ]

        self.assertFalse(self.controller.form_is_valid())

    def test_form_is_valid_copy_invalid(self):       
        self.view.origin_input.setText("/valid/path")
        self.view.required_fields = [
            self.view.origin_input, 
            self.view.dest_input
        ]

        self.assertFalse(self.controller.form_is_valid())
    
    #--- path validationn tests ---
    @patch("platform.system", return_value="Darwin")
    def test_path_is_valid_valid_macos(self, _):
        self.assertTrue(self.controller.path_is_valid("/Users/test"))

    @patch("platform.system", return_value="Darwin")
    def test_path_is_valid_filepath_macos(self, _):
        self.assertFalse(self.controller.path_is_valid("/Users/test.txt"))

    @patch("platform.system", return_value="Darwin")
    def test_path_is_valid_invalid_macos(self, _):
        self.assertFalse(self.controller.path_is_valid(":Users/"))

    @patch("platform.system", return_value="Windows")
    def test_path_is_valid_valid_windows(self, _):
        self.assertTrue(self.controller.path_is_valid(r"C:\Users\test"))

    @patch("platform.system", return_value="Windows")
    def test_path_is_valid_filepath_windows(self, _):
        self.assertFalse(self.controller.path_is_valid(r"C:\Users\test.txt"))

    @patch("platform.system", return_value="Windows")
    def test_path_is_valid_invalid_windows(self, _):
        self.assertFalse(self.controller.path_is_valid("C:Users/test"))

    @patch("platform.system", return_value="Linux")
    def test_path_is_valid_valid_linux(self, _):
        self.assertTrue(self.controller.path_is_valid("/home/test"))

    @patch("platform.system", return_value="Linux")
    def test_path_is_valid_filepath_linux(self, _):
        self.assertFalse(self.controller.path_is_valid("/home/test.txt"))

    @patch("platform.system", return_value="Linux")
    def test_path_is_valid_invalid_linux(self, _):
        self.assertFalse(self.controller.path_is_valid("home/test"))

    @patch("platform.system", return_value="Universal")
    def test_path_is_valid_universal(self, _):
        self.assertFalse(self.controller.path_is_valid("home/test"))

    #--- required fields tests ---
    def test_add_required_field_new_field(self):
        self.view.required_fields = [
            self.view.name_input,
            self.view.origin_input
        ]
        self.view.add_required_field(self.view.dest_input)

        self.assertEqual(self.view.required_fields, [
            self.view.name_input,
            self.view.origin_input,
            self.view.dest_input 
        ])

    def test_add_required_field_duplicate_field(self):
        self.view.required_fields = [
            self.view.name_input,
            self.view.origin_input,
            self.view.dest_input
        ]
        self.view.add_required_field(self.view.dest_input)

        self.assertEqual(self.view.required_fields, [
            self.view.name_input,
            self.view.origin_input,
            self.view.dest_input 
        ])

    def test_remove_required_field_field_exists(self):
        self.view.required_fields = [
            self.view.name_input,
            self.view.origin_input
        ]
        self.view.remove_required_field(self.view.origin_input)

        self.assertEqual(self.view.required_fields, [
            self.view.name_input
        ])

    def test_remove_required_field_field_not_exists(self):
        self.view.required_fields = [
            self.view.name_input,
            self.view.origin_input
        ]
        self.view.remove_required_field(self.view.dest_input)

        self.assertEqual(self.view.required_fields, [
            self.view.name_input,
            self.view.origin_input
        ])

    def test_get_required_fields(self):
        self.view.required_fields = [
            self.view.name_input,
            self.view.origin_input
        ]
        actual = self.view.get_required_fields()

        self.assertEqual(actual, [
            self.view.name_input,
            self.view.origin_input
        ])

if __name__ == "__main__":
    unittest.main()