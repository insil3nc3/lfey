from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtWidgets import (
    QWidget, QApplication, QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QMainWindow, QFrame
)
from PyQt6.QtCore import Qt, QSize, QEvent
import sys
from shop import ShopLayout  # Импортируем ShopLayout из shop.py

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройка размеров и положения окна
        x = 1100
        y = 700
        x1 = int((1920 - x) / 2)
        y1 = int((1080 - y) / 2)
        self.setWindowTitle("NotApp")
        self.setGeometry(x1, y1, x, y)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setStyleSheet("background-color: white;")

        # Основной горизонтальный макет
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)  # Убираем отступы между виджетами
        main_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы вокруг макета
        central_widget.setLayout(main_layout)

        # Создаем боковую панель и основную область
        self.side_bar = self.create_side_bar()
        self.content_area = self.create_content_area()

        # Добавляем боковую панель и основную область в главный макет
        main_layout.addWidget(self.side_bar)
        main_layout.addWidget(self.content_area)

        # Изначально добавляем основной макет в content_area
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.content_area.setLayout(self.main_layout)

        # Пример добавления контента в основную область
        self.label = QLabel("Основной контент")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.label)

    def create_side_bar(self):
        # Боковая панель (меню)
        side_bar = QFrame()
        side_bar.setStyleSheet("""
            background-color: #2E3440;
            border: none;  /* Убираем границу */
        """)
        side_bar.setFixedWidth(60)  # Ширина боковой панели

        # Вертикальный макет для боковой панели
        side_layout = QVBoxLayout()
        side_layout.setSpacing(10)
        side_layout.setContentsMargins(0, 0, 0, 0)
        side_bar.setLayout(side_layout)

        # Список иконок и соответствующих им действий
        buttons = [
            {
                "icon_path": r"C:\Users\minec\OneDrive\Рабочий стол\zetcorddev\notApp\icons\settings.png",
                "hover_icon_path": r"C:\Users\minec\OneDrive\Рабочий стол\zetcorddev\notApp\icons\settings_pressed.png",
                "tooltip": "Settings",
                "action": self.settings_action
            },
            {
                "icon_path": r"C:\Users\minec\OneDrive\Рабочий стол\zetcorddev\notApp\icons\shop.png",
                "hover_icon_path": r"C:\Users\minec\OneDrive\Рабочий стол\zetcorddev\notApp\icons\shop_pressed.png",
                "tooltip": "Shop",
                "action": self.shop_action
            },
            {
                "icon_path": r"C:\Users\minec\OneDrive\Рабочий стол\zetcorddev\notApp\icons\my_modules.png",
                "hover_icon_path": r"C:\Users\minec\OneDrive\Рабочий стол\zetcorddev\notApp\icons\my_modules_pressed.png",
                "tooltip": "My Modules",
                "action": self.my_modules_action
            },
        ]

        for btn_info in buttons:
            button = QPushButton()
            button.setIcon(QIcon(btn_info["icon_path"]))
            button.setIconSize(QSize(50, 50))
            button.setToolTip(btn_info["tooltip"])
            button.setFixedSize(50, 50)
            button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
            """)
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            button.clicked.connect(btn_info["action"])
            button.setObjectName(btn_info["icon_path"])  # Устанавливаем objectName

            # Обработка событий наведения и выхода курсора
            button.enterEvent = lambda event, btn=button: self.on_enter(btn)
            button.leaveEvent = lambda event, btn=button: self.on_leave(btn)

            side_layout.addWidget(button)

        side_layout.addStretch()

        return side_bar

    def on_enter(self, button):
        # Изменяем иконку на иконку при наведении
        button.setIcon(QIcon(button.objectName().replace(".png", "_pressed.png")))
        button.setIconSize(QSize(40, 40))

    def on_leave(self, button):
        # Возвращаем исходную иконку
        button.setIcon(QIcon(button.objectName()))
        button.setIconSize(QSize(40, 40))

    def settings_action(self):
        print("Settings button pressed")

    def shop_action(self):
        self.show_shop_layout()

    def my_modules_action(self):
        print("My Modules button pressed")

    def show_shop_layout(self):
        print("Showing shop layout")
        self.shop_layout = ShopLayout(self)
        self.clear_content()
        self.main_layout.addWidget(self.shop_layout)
        self.shop_layout.show()

    def show_main_layout(self):
        print("Showing main layout")
        self.clear_content()
        self.label = QLabel("Основной контент")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.label)

    def clear_content(self):
        print("Clearing content")
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

    def create_content_area(self):
        # Основная область контента
        content_area = QFrame()
        content_area.setStyleSheet("""
            background-color: #ECEFF4;
            border: none;  /* Убираем границу */
        """)
        content_layout = QVBoxLayout()
        content_layout.setSpacing(0)  # Убираем отступы между элементами
        content_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы внутри области
        content_area.setLayout(content_layout)

        return content_area


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())