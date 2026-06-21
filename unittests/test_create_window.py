import unittest
from pathlib import Path 
from PyQt6 import QtWidgets
import sys
from create_window import CreateWindow
from create_window_enums import TypeComboValues

app = QtWidgets.QApplication(sys.argv)

class TestCreateWindow(unittest.TestCase):
    def test_form_is_valid_copy_valid_case(self):
        window = CreateWindow()
        window.name_input.setText("Test Case")
        window.desc_input.setText("Test")
        window.type_combo.setCurrentIndex(window.type_combo.findData(TypeComboValues.COPY))
        window.origin_input.setText(str(Path().absolute()))
        window.dest_input.setText(str(Path("ui").absolute()))
        self.assertEqual(window.form_is_valid(), True)

    def test_form_is_valid_copy_empty_values_case(self):
        window = CreateWindow()
        window.name_input.setText("")
        window.desc_input.setText("Test")
        window.type_combo.setCurrentIndex(window.type_combo.findData(TypeComboValues.COPY))
        window.origin_input.setText("")
        window.dest_input.setText("")
        self.assertEqual(window.form_is_valid(), False)

    def test_form_is_valid_copy_empty_spaces_case(self):
        window = CreateWindow()
        window.name_input.setText("Test Case")
        window.desc_input.setText("Test")
        window.type_combo.setCurrentIndex(window.type_combo.findData(TypeComboValues.COPY))
        window.origin_input.setText(str(Path("ui").absolute()))
        window.dest_input.setText("  ")
        self.assertEqual(window.form_is_valid(), False)

    def test_form_is_valid_move_valid_case(self):
        window = CreateWindow()
        window.name_input.setText("Test Case")
        window.desc_input.setText("")
        window.type_combo.setCurrentIndex(window.type_combo.findData(TypeComboValues.MOVE))
        window.origin_input.setText(str(Path().absolute()))
        window.dest_input.setText(str(Path("ui").absolute()))
        self.assertEqual(window.form_is_valid(), True)

    def test_form_is_valid_move_empty_values_case(self):
        window = CreateWindow()
        window.name_input.setText("")
        window.desc_input.setText("Test")
        window.type_combo.setCurrentIndex(window.type_combo.findData(TypeComboValues.MOVE))
        window.origin_input.setText(str(Path().absolute()))
        window.dest_input.setText("")
        self.assertEqual(window.form_is_valid(), False)

    def test_form_is_valid_move_empty_spaces_case(self):
        window = CreateWindow()
        window.name_input.setText("    ")
        window.desc_input.setText("Test")
        window.type_combo.setCurrentIndex(window.type_combo.findData(TypeComboValues.MOVE))
        window.origin_input.setText(str(Path("ui").absolute()))
        window.dest_input.setText(str(Path().absolute()))
        self.assertEqual(window.form_is_valid(), False)
    
    def test_form_is_valid_delete_valid_case(self):
        window = CreateWindow()
        window.name_input.setText("Test Case3")
        window.desc_input.setText("Test123")
        window.type_combo.setCurrentIndex(window.type_combo.findData(TypeComboValues.DELETE))
        print(window.required_fields)
        window.origin_input.setText(str(Path().absolute()))
        self.assertEqual(window.form_is_valid(), True)

    def test_form_is_valid_delete_empty_values_case(self):
        window = CreateWindow()
        window.name_input.setText("")
        window.desc_input.setText("Test")
        window.type_combo.setCurrentIndex(window.type_combo.findData(TypeComboValues.DELETE))
        window.origin_input.setText(str(Path().absolute()))
        self.assertEqual(window.form_is_valid(), False)

    def test_form_is_valid_delete_empty_spaces_case(self):
        window = CreateWindow()
        window.name_input.setText("Test123")
        window.desc_input.setText("Test")
        window.type_combo.setCurrentIndex(window.type_combo.findData(TypeComboValues.DELETE))
        window.origin_input.setText("  ")
        self.assertEqual(window.form_is_valid(), False)
    


if __name__ == "__main__":
    unittest.main()