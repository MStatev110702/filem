import sys
from PyQt6 import QtWidgets
from main_window import MainWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()