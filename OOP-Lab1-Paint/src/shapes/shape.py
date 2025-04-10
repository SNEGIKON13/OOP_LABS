from abc import ABC, abstractmethod

class Shape(ABC):
    def __init__(self, char='*'):
        self._validate_char(char, "char")
        self._id = None
        self.char = char

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @staticmethod
    def _validate_char(value, name, allow_empty=False):
        if not isinstance(value, str):
            raise ValueError(f"{name} должен быть строкой. Введено: {value}")
        if not value and allow_empty:
            return None
        if not value:
            raise ValueError(f"{name} не может быть пустым.")
        if len(value) != 1:
            raise ValueError(f"{name} должен быть одним символом. Введено: '{value}'")
        return value

    @abstractmethod
    def move(self, dx, dy):
        pass

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def draw(self, canvas):
        pass

    @abstractmethod
    def __str__(self):
        pass