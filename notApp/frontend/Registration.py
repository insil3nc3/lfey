import json
import sys
import re
from langdetect import detect
import requests
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer
from backend.lfeyAPI import APIservice
from core import MainWindow
from code_verif_window import CodeVerifWindow
import logging
from backend.json_work import JSONWork


api = APIservice("http://bore.pub:63156")
# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат логов
    filename="app.log",  # Имя файла для записи логов
    filemode="w",  # Режим записи (перезапись файла)
)

js = JSONWork()

class RegistrateWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        x = 700
        y = 400
        x1 = int((1920 - x) // 2)
        y1 = int((1080 - y) // 2)
        self.setWindowTitle("Registration")
        self.setGeometry(x1, y1, x, y)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.addStretch()
        self.label = QLabel("Registration")
        self.label.setFont(QFont("Arial", 24))
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.error_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.mail = QLineEdit()
        self.edit_editLine(self.mail, "email")
        layout.addWidget(self.mail, alignment=Qt.AlignmentFlag.AlignCenter)

        self.password = QLineEdit()
        self.edit_editLine(self.password, "password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password, alignment=Qt.AlignmentFlag.AlignCenter)

        self.confirm_password = QLineEdit()
        self.edit_editLine(self.confirm_password, "confirm password")
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_password, alignment=Qt.AlignmentFlag.AlignCenter)

        self.registration_button = QPushButton("Registration")
        self.registration_button.setMinimumSize(300, 50)
        self.registration_button.clicked.connect(self.validate_input)
        layout.addWidget(self.registration_button, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()

        central_widget.setLayout(layout)

    def edit_editLine(self, EditLine, PlaceholderText):
        EditLine.setFixedWidth(300)
        EditLine.setFixedHeight(40)
        EditLine.setFont(QFont("Arial", 16))
        EditLine.setPlaceholderText(PlaceholderText)

    def validate_input(self):
        logging.debug("Starting input validation...")
        email = self.mail.text()
        password = self.password.text()
        confirm_password = self.confirm_password.text()

        # Валидация email
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, email):
            logging.error("Invalid email format!")
            self.show_message("Invalid email format!", "Error")
            return

        # Валидация пароля
        if len(password) < 6:
            logging.error("Password too short!")
            self.show_message("Password must be at least 6 characters long!", "Error")
            return


        if password != confirm_password:
            logging.error("Passwords do not match!")
            self.show_message("Passwords do not match!", "Error")
            return

        logging.debug("Input validation successful!")

        self.show_message("Registration successful!", "Success")
        self.send_user_data(email, password)
        js.set_open(1)
        self.open_code_verif_menu()

    def show_message(self, message, message_type):
        self.error_label.setText(message)
        if message_type == "Error":
            self.error_label.setStyleSheet("color: red;")
        else:
            self.error_label.setStyleSheet("color: green;")
        # Устанавливаем таймер для очистки текста через 3 секунды
        timer = QTimer(self)
        timer.singleShot(3000, self.clear_message)

    def clear_message(self):
        self.error_label.setText("")

    def send_user_data(self, email, password):
        logging.debug("Sending user data...")
        try:
            api.send_user_data(email, password)
            logging.debug("User data sent successfully!")
        except Exception as e:
            logging.error(f"Error sending user data: {e}")
            raise

    def open_main_menu(self):
        self.main_menu = MainWindow()
        self.main_menu.show()
        self.close()  # Закрываем окно регистрации

    def open_code_verif_menu(self):
        logging.debug("Opening code verification window...")
        try:
            # Передаем email и код в конструктор
            self.code_menu = CodeVerifWindow(email=self.mail.text(), api=api)  # Замените "123456" на реальный код
            self.code_menu.show()
            self.close()
            logging.debug("Code verification window opened successfully!")
        except Exception as e:
            logging.error(f"Error opening code verification window: {e}")
            raise
