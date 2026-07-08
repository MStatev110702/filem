import unittest
from unittest.mock import patch
from pathlib import Path 
from PyQt6 import QtWidgets
import sys
from src.create_window import CreateWindow
from src.main_window import MainWindow
from src.create_window_enums import TypeComboValues

app = QtWidgets.QApplication(sys.argv)

class TestCreateWindow(unittest.TestCase):
    def test_form_is_valid_copy_valid_case(self):
        window = CreateWindow(MainWindow())
        window.name_input.setText("Test Case")
        window.desc_input.setText("Test")
        window.type_combo.setCurrentIndex(window.type_combo.findData(TypeComboValues.COPY))
        window.origin_input.setText(str(Path().absolute()))
        window.dest_input.setText(str(Path("ui").absolute()))
        self.assertEqual(window.form_is_valid(), True)

    def test_form_is_valid_copy_empty_values_case(self):
        window = CreateWindow(MainWindow())
        window.name_input.setText("")
        window.desc_input.setText("Test")
        window.type_combo.setCurrentIndex(window.type_combo.findData(TypeComboValues.COPY))
        window.origin_input.setText("")
        window.dest_input.setText("")
        self.assertEqual(window.form_is_valid(), False)

    def test_form_is_valid_copy_empty_spaces_case(self):
        window = CreateWindow(MainWindow())
        window.name_input.setText("Test Case")
        window.desc_input.setText("Test")
        window.type_combo.setCurrentIndex(window.type_combo.findData(TypeComboValues.COPY))
        window.origin_input.setText(str(Path("ui").absolute()))
        window.dest_input.setText("  ")
        self.assertEqual(window.form_is_valid(), False)

    def test_form_is_valid_move_valid_case(self):
        window = CreateWindow(MainWindow())
        window.name_input.setText("Test Case")
        window.desc_input.setText("")
        window.type_combo.setCurrentIndex(window.type_combo.findData(TypeComboValues.MOVE))
        window.origin_input.setText(str(Path().absolute()))
        window.dest_input.setText(str(Path("ui").absolute()))
        self.assertEqual(window.form_is_valid(), True)

    def test_form_is_valid_move_empty_values_case(self):
        window = CreateWindow(MainWindow())
        window.name_input.setText("")
        window.desc_input.setText("Test")
        window.type_combo.setCurrentIndex(window.type_combo.findData(TypeComboValues.MOVE))
        window.origin_input.setText(str(Path().absolute()))
        window.dest_input.setText("")
        self.assertEqual(window.form_is_valid(), False)

    def test_form_is_valid_move_empty_spaces_case(self):
        window = CreateWindow(MainWindow())
        window.name_input.setText("    ")
        window.desc_input.setText("Test")
        window.type_combo.setCurrentIndex(window.type_combo.findData(TypeComboValues.MOVE))
        window.origin_input.setText(str(Path("ui").absolute()))
        window.dest_input.setText(str(Path().absolute()))
        self.assertEqual(window.form_is_valid(), False)
    
    def test_form_is_valid_delete_valid_case(self):
        window = CreateWindow(MainWindow())
        window.name_input.setText("Test Case3")
        window.desc_input.setText("Test123")
        window.type_combo.setCurrentIndex(window.type_combo.findData(TypeComboValues.DELETE))
        window.origin_input.setText(str(Path().absolute()))
        self.assertEqual(window.form_is_valid(), True)

    def test_form_is_valid_delete_empty_values_case(self):
        window = CreateWindow(MainWindow())
        window.name_input.setText("")
        window.desc_input.setText("Test")
        window.type_combo.setCurrentIndex(window.type_combo.findData(TypeComboValues.DELETE))
        window.origin_input.setText(str(Path().absolute()))
        self.assertEqual(window.form_is_valid(), False)

    def test_form_is_valid_delete_empty_spaces_case(self):
        window = CreateWindow(MainWindow())
        window.name_input.setText("Test123")
        window.desc_input.setText("Test")
        window.type_combo.setCurrentIndex(window.type_combo.findData(TypeComboValues.DELETE))
        window.origin_input.setText("  ")
        self.assertEqual(window.form_is_valid(), False)
    
    @patch("platform.system", return_value="Darwin")
    def test_path_is_valid_valid_macos(self, _):
        window = CreateWindow(MainWindow())
        self.assertTrue(window.path_is_valid("/Users/test"))

    @patch("platform.system", return_value="Darwin")
    def test_path_is_valid_filepath_macos(self, _):
        window = CreateWindow(MainWindow())
        self.assertFalse(window.path_is_valid("/Users/test.txt"))

    @patch("platform.system", return_value="Darwin")
    def test_path_is_valid_invalid_macos(self, _):
        window = CreateWindow(MainWindow())
        self.assertFalse(window.path_is_valid(":Users/"))

    @patch("platform.system", return_value="Windows")
    def test_path_is_valid_valid_windows(self, _):
        window = CreateWindow(MainWindow())
        self.assertTrue(window.path_is_valid(r"C:\Users\test"))

    @patch("platform.system", return_value="Windows")
    def test_path_is_valid_filepath_windows(self, _):
        window = CreateWindow(MainWindow())
        self.assertFalse(window.path_is_valid(r"C:\Users\test.txt"))

    @patch("platform.system", return_value="Windows")
    def test_path_is_valid_invalid_windows(self, _):
        window = CreateWindow(MainWindow())
        self.assertFalse(window.path_is_valid("C:Users/test"))

    @patch("platform.system", return_value="Linux")
    def test_path_is_valid_valid_linux(self, _):
        window = CreateWindow(MainWindow())
        self.assertTrue(window.path_is_valid("/home/test"))

    @patch("platform.system", return_value="Linux")
    def test_path_is_valid_filepath_linux(self, _):
        window = CreateWindow(MainWindow())
        self.assertFalse(window.path_is_valid("/home/test.txt"))

    @patch("platform.system", return_value="Linux")
    def test_path_is_valid_invalid_linux(self, _):
        window = CreateWindow(MainWindow())
        self.assertFalse(window.path_is_valid("home/test"))

    @patch("platform.system", return_value="Universal")
    def test_path_is_valid_universal(self, _):
        window = CreateWindow(MainWindow())
        self.assertFalse(window.path_is_valid("home/test"))

if __name__ == "__main__":
    unittest.main()