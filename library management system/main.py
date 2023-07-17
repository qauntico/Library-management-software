from PyQt6.QtWidgets import QMainWindow, QApplication
from system import MainWindow
import sys

app = QApplication(sys.argv)
mw = MainWindow()
mw.show()
sys.exit(app.exec())