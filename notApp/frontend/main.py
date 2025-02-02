from PyQt6.QtWidgets import QApplication
from Registration import RegistrateWindow

if __name__ == '__main__':
    app = QApplication([])
    window = RegistrateWindow()
    window.show()
    app.exec()