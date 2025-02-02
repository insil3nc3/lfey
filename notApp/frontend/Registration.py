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

api = APIservice("http://bore.pub:63156")

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
        email = self.mail.text()
        password = self.password.text()
        confirm_password = self.confirm_password.text()

        # Валидация email
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, email):
            self.show_message("Invalid email format!", "Error")
            return

        # Валидация пароля
        if len(password) < 6:
            self.show_message("Password must be at least 6 characters long!", "Error")
            return

        if detect(password) != "en":
            self.show_message("Password must be English!", "Error")
            return

        if password != confirm_password:
            self.show_message("Passwords do not match!", "Error")
            return

        # Если все проверки пройдены
        self.show_message("Registration successful!", "Success")
        self.send_user_data(email, password)
        self.open_main_menu()

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
        api.send_user_data(email, password)

    def open_main_menu(self):
        self.main_menu = MainWindow()
        self.main_menu.show()
        self.close()  # Закрываем окно регистрации

