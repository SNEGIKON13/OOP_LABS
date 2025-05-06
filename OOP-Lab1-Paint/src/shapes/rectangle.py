from .shape import Shape
from .registry import ShapeRegistry


class Rectangle(Shape):
    def __init__(
            self,
            x1: int, y1: int,
            x2: int, y2: int,
            border_char: str = '*',
            fill_char: str | None = None
    ):
        super().__init__(border_char)
        self.x1, self.y1 = min(x1, x2), min(y1, y2)
        self.x2, self.y2 = max(x1, x2), max(y1, y2)
        if self.x2 - self.x1 < 1 or self.y2 - self.y1 < 1:
            raise ValueError("Rectangle must be at least 2×2 in size")
        if fill_char is not None:
            self._validate_char(fill_char, "fill_char")
        self.fill_char = fill_char

    def move(self, dx: int, dy: int) -> None:
        self.x1 += dx
        self.x2 += dx
        self.y1 += dy
        self.y2 += dy

    def to_dict(self) -> dict:
        return {
            'type': 'Rectangle',
            'x1': self.x1, 'y1': self.y1,
            'x2': self.x2, 'y2': self.y2,
            'char': self.char,
            'fill_char': self.fill_char,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Rectangle':
        return cls(
            data['x1'], data['y1'],
            data['x2'], data['y2'],
            data.get('char', '*'),
            data.get('fill_char')
        )

    def is_within_bounds(self, width: int, height: int) -> bool:
        return (
                0 <= self.x1 < width and
                0 <= self.x2 < width and
                0 <= self.y1 < height and
                0 <= self.y2 < height
        )

    def draw(self, grid: list[list[str]]) -> None:
        h = len(grid)
        w = len(grid[0]) if h else 0
        for y in range(self.y1, self.y2 + 1):
            for x in range(self.x1, self.x2 + 1):
                if y in (self.y1, self.y2) or x in (self.x1, self.x2):
                    if 0 <= x < w and 0 <= y < h:
                        grid[y][x] = self.char
                elif self.fill_char:
                    if 0 <= x < w and 0 <= y < h:
                        grid[y][x] = self.fill_char

    def __str__(self) -> str:
        return (
            f"Rectangle(id={self.id}, "
            f"({self.x1},{self.y1})→({self.x2},{self.y2}), "
            f"char='{self.char}', fill='{self.fill_char}')"
        )


ShapeRegistry.register('Rectangle', Rectangle)
