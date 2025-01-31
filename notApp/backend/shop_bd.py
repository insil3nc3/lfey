from requests import Session
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Modules(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"{self.name}"

engine = create_engine("sqlite:///modules.db")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class ModulesManager:
    def __init__(self):
        global session
        self.session = session

    def add_module(self, name):
        new_module = Modules(name=name)
        self.session.add(new_module)
        self.session.commit()

    def delete_module(self, module_id):
        module = self.session.query(Modules).filter(Modules.id == module_id).first()
        self.session.delete(module)
        self.session.commit()

    def get_module(self, module_id):
        """Возвращает модуль по его ID."""
        module = self.session.query(Modules).filter(Modules.id == module_id).first()
        if module:
            print(f"Найден модуль: {module}")
        else:
            print(f"Модуль с id {module_id} не найден.")
        return module

    def get_all_modules(self):
        """Возвращает все модули из базы данных."""
        modules = self.session.query(Modules).all()
        return modules

    def update_module(self, module_id, new_name):
        """Обновляет имя модуля по его ID."""
        module = self.session.query(Modules).filter(Modules.id == module_id).first()
        if module:
            module.name = new_name
            self.session.commit()
            print(f"Модуль обновлен: {module}")
        else:
            print(f"Модуль с id {module_id} не найден.")