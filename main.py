import sys

from PyQt5 import QtWidgets
from ui_control.main_window import MainWindow



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
