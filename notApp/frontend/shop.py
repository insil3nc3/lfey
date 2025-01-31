# shop.py
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton

class ShopLayout(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            background-color: #D8DEE9;
            border: none;  /* Убираем границу */
        """)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.layout)

        label = QLabel("Добро пожаловать в магазин!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(label)

        # Пример кнопки для возврата
        back_button = QPushButton("Назад")
        back_button.setFixedSize(100, 40)
        back_button.clicked.connect(self.back)
        self.layout.addWidget(back_button)

    def back(self):
        # Метод для возврата к предыдущему макету
        self.parent().show_main_layout()

    def show(self):
        self.setVisible(True)

    def hide(self):
        self.setVisible(False)