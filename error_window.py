from PyQt6 import QtCore, QtGui, QtWidgets

class ErrorWindow(QtWidgets.QDialog):
    def __init__(self, text: str):
        super().__init__()

        self.setWindowTitle("Error")

        layout = QtWidgets.QVBoxLayout()

        message = QtWidgets.QLabel(text)
        
        ok_button = QtWidgets.QPushButton("OK")
        ok_button.clicked.connect(self.accept)

        layout.addWidget(message)
        layout.addWidget(ok_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)