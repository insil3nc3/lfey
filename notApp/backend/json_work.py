import ctypes
import json
import os

def set_hidden_windows(filename):
    """Делает файл скрытым в Windows"""
    FILE_ATTRIBUTE_HIDDEN = 0x02
    ctypes.windll.kernel32.SetFileAttributesW(filename, FILE_ATTRIBUTE_HIDDEN)

class JSONWork:
    def __init__(self, filename="data.json"):
        if filename is None:
            self.filename = ".data.json" if os.name != 'nt' else "data.json"
        else:
            self.filename = filename

        self.default_data = {
            "pcNumber": None,
            "Open": 0
        }

    def create_json_if_not_exists(self):
        """Создает JSON-файл с базовой структурой, если он не существует"""
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(self.default_data.copy(), file, ensure_ascii=False, indent=4)

            # Делаем файл скрытым в Windows
            if os.name == "nt":
                set_hidden_windows(self.filename)

    def _safe_read_data(self):
        """
        Внутренний метод для безопасного чтения данных
        """
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return self.default_data.copy()

    def get_pc_number(self):
        """Возвращает значение pcNumber или None при ошибках"""
        data = self._safe_read_data()
        return data.get("pcNumber")

    def set_pc_number(self, value):
        """Устанавливает новое значение для pcNumber"""
        data = self._safe_read_data()
        data["pcNumber"] = value
        with open(self.filename, "w") as file:
            json.dump(data, file)

    def get_open(self):
        """Возвращает значение Open или 0 по умолчанию"""
        data = self._safe_read_data()
        return data.get("Open", 0)

    def set_open(self, value):
        """Устанавливает новое значение для Open"""
        data = self._safe_read_data()
        data["Open"] = value
        with open(self.filename, "w") as file:
            json.dump(data, file)