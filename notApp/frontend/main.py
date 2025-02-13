from PyQt6.QtWidgets import QApplication
from Registration import RegistrateWindow
from Authorization import Authorization
from backend.json_work import JSONWork

if __name__ == '__main__':
    js = JSONWork()

    app = QApplication([])
    if js.get_open() == 0:
        window = RegistrateWindow()
    else:
        window = Authorization()
    window.show()
    app.exec()