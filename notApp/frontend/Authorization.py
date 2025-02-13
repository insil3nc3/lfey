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
import requests
from backend.json_work import JSONWork
api = APIservice("http://bore.pub:63156")
js = JSONWork()

class Authorization(QMainWindow):
    def __init__(self):
        super().__init__()

        x = 700
        y = 400
        x1 = int((1920 - x) // 2)
        y1 = int((1080 - y) // 2)
        self.setWindowTitle("Authorization")
        self.setGeometry(x1, y1, x, y)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.addStretch()

        self.label = QLabel("Authorization")
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

        layout.addStretch()
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
        user_password = self.password.text()



        # Валидация email
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, email):
            logging.error("Invalid email format!")
            self.show_message("Invalid email format!", "Error")
            return


        a = api.login(email, user_password)
        print(a)
        if a:
            js.set_pc_number(a)
            logging.debug("Input validation successful!")
            self.show_message("Registration successful!", "Success")
        else:
            self.show_message("Registration failed!", "Error")


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
