import logging
from PyQt6.QtGui import QIcon, QCursor, QFont
from PyQt6.QtWidgets import (
    QWidget, QApplication, QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QMainWindow, QFrame, QLineEdit
)
from PyQt6.QtCore import Qt, QSize, QEvent
import sys

from core import MainWindow

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат логов
    filename="code_verif_window.log",  # Имя файла для записи логов
    filemode="w",  # Режим записи (перезапись файла)
)

class CodeVerifWindow(QMainWindow):
    def __init__(self, email, api):
        super().__init__()
        self.email = email  # Сохраняем email
        self.api = api  # Сохраняем API
        logging.debug(f"Initializing CodeVerifWindow with email: {email}")

        x = 700
        y = 400
        x1 = int((1920 - x) // 2)
        y1 = int((1080 - y) // 2)
        self.setWindowTitle("Registration")
        self.setGeometry(x1, y1, x, y)
        logging.debug(f"Window geometry set to: x={x1}, y={y1}, width={x}, height={y}")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.addStretch()
        self.label = QLabel("Code verification")

        self.label.setFont(QFont("Arial", 24))
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.code_input = QLineEdit()  # Поле для ввода кода
        self.edit_editLine(self.code_input, "code input")
        self.code_input.setMaxLength(6)
        self.code_input.setFixedSize(225, 50)
        self.code_input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                color: #FFFFFF;
                border: 2px solid #555555;
                border-radius: 8px;
                padding-left: 10px;
                letter-spacing: 10px;
            }
            QLineEdit:focus {
                border: 2px solid #888888;
            }
        """)
        layout.addWidget(self.code_input, alignment=Qt.AlignmentFlag.AlignCenter)
        logging.debug("Code input field created and styled")

        self.confirm_button = QPushButton("confirm")
        self.confirm_button.setFont(QFont("Arial", 30, QFont.Weight.ExtraBold))
        self.confirm_button.setFixedSize(225, 50)
        self.confirm_button.clicked.connect(self.confirm_code)  # Подключаем кнопку к методу
        layout.addWidget(self.confirm_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        self.resend_button = QPushButton("resend code")


        logging.debug("Confirm button created and connected to confirm_code method")

        central_widget.setLayout(layout)
        logging.debug("Layout set for central widget")

    def edit_editLine(self, EditLine, PlaceholderText):
        EditLine.setFixedWidth(300)
        EditLine.setFixedHeight(40)
        EditLine.setFont(QFont("Arial", 30, QFont.Weight.ExtraBold))
        EditLine.setPlaceholderText(PlaceholderText)
        logging.debug(f"EditLine configured with placeholder: {PlaceholderText}")

    def confirm_code(self):
        # Получаем введенный код
        user_code = self.code_input.text()
        logging.debug(f"Confirming code for email: {self.email}, code: {user_code}")

        try:
            # Вызываем API для подтверждения кода
            logging.debug(f"Calling API to confirm code for email: {self.email}")
            jwt_token = self.api.confirm_password(self.email, user_code)

            if jwt_token:
                logging.debug("Code confirmed successfully! JWT token received.")
                print(f"JWT Token: {jwt_token}")
                self.save_jwt_token(jwt_token)  # Сохраняем токен
                self.open_main_menu()  # Переход на следующее окно
            else:
                logging.error("Failed to confirm code. Invalid response from API.")
                # Здесь можно показать сообщение об ошибке пользователю
        except Exception as e:
            logging.error(f"Error confirming code: {e}")
            # Здесь можно показать сообщение об ошибке пользователю
            raise

    def save_jwt_token(self, jwt_token):
        # Сохраняем токен в файл или в память
        with open("jwt_token.json", "w") as f:
            f.write(jwt_token)
        logging.debug("JWT token saved.")

    def open_main_menu(self):
        self.main_menu = MainWindow()
        self.main_menu.show()
        self.close()