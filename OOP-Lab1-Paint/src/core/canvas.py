from shapes import Shape


class Canvas:
    def __init__(self, width: int = 80, height: int = 18, bg_char: str = '.'):
        self.width = width
        self.height = height
        self.bg_char = bg_char
        self._shapes = []
        self._next_id = 1

    @property
    def shapes(self) -> list[Shape]:
        return list(self._shapes)

    def get_max_shape_id(self) -> int:
        return self._next_id - 1

    def add_shape(self, shape: Shape) -> None:
        if not shape.is_within_bounds(self.width, self.height):
            raise ValueError(f"Фигура {shape} выходит за пределы холста {self.width}×{self.height}")
        shape.id = self._next_id
        self._shapes.append(shape)
        self._next_id += 1

    def remove_shape(self, shape_id: int) -> None:
        self._shapes = [s for s in self._shapes if s.id != shape_id]

    def get_shape_by_id(self, shape_id: int) -> Shape | None:
        return next((s for s in self._shapes if s.id == shape_id), None)

    def clear_shapes(self) -> None:
        self._shapes.clear()
        self._next_id = 1

    def render_data(self) -> list[str]:
        """
        Собирает и возвращает список строк — текущее ASCII-представление холста.
        Не печатает, не хранит состояние внутри.
        """
        # инициализируем «пустую» сетку
        grid: list[list[str]] = [
            [self.bg_char for _ in range(self.width)]
            for _ in range(self.height)
        ]
        # каждая фигура сама рисует себя в grid
        for shape in self._shapes:
            shape.draw(grid)
        # превращаем в строки
        return [''.join(row) for row in grid]
