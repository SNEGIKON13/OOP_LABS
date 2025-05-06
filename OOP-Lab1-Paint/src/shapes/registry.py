from typing import Type
from .shape import Shape


class ShapeRegistry:
    _map: dict[str, Type[Shape]] = {}

    @classmethod
    def register(cls, key: str, shape_cls: Type[Shape]) -> None:
        cls._map[key] = shape_cls

    @classmethod
    def create(cls, data: dict) -> Shape:
        if not isinstance(data, dict):
            raise ValueError("Данные должны быть словарём")
        key = data.get('type')
        if key not in cls._map:
            raise ValueError(f"Неизвестный тип фигуры: {key!r}")
        return cls._map[key].from_dict(data)
