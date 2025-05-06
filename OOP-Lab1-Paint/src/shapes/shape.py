from abc import ABC, abstractmethod


class Shape(ABC):
    def __init__(self, char: str = '*'):
        self._validate_char(char, "char")
        self._id = None
        self.char = char

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @staticmethod
    def _validate_char(value: str, name: str, allow_empty: bool = False) -> None:
        if not isinstance(value, str):
            raise ValueError(f"{name} должен быть строкой. Введено: {value!r}")
        if not value and not allow_empty:
            raise ValueError(f"{name} не может быть пустым.")
        if len(value) != 1:
            raise ValueError(f"{name} должен быть одним символом. Введено: {value!r}")

    @abstractmethod
    def move(self, dx: int, dy: int) -> None:
        """Смещение фигуры на dx, dy."""
        ...

    @abstractmethod
    def to_dict(self) -> dict:
        """Сериализация в словарь для JSON."""
        ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> 'Shape':
        """Создать экземпляр из словаря данных."""
        ...

    @abstractmethod
    def draw(self, grid: list[list[str]]) -> None:
        """
        Нарисовать себя в двумерном списке grid.
        grid[y][x] = char или fill_char где нужно.
        """
        ...

    @abstractmethod
    def is_within_bounds(self, width: int, height: int) -> bool:
        """Проверить, что вся фигура помещается в холст заданного размера."""
        ...

    @abstractmethod
    def __str__(self) -> str:
        """Человекочитаемое описание фигуры."""
        ...
