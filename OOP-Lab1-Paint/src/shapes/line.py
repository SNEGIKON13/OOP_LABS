from .shape import Shape
from .registry import ShapeRegistry


class Line(Shape):
    def __init__(
            self,
            x1: int, y1: int,
            x2: int, y2: int,
            char: str = '-'
    ):
        super().__init__(char)
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2

    def move(self, dx: int, dy: int) -> None:
        self.x1 += dx
        self.x2 += dx
        self.y1 += dy
        self.y2 += dy

    def to_dict(self) -> dict:
        return {
            'type': 'Line',
            'x1': self.x1, 'y1': self.y1,
            'x2': self.x2, 'y2': self.y2,
            'char': self.char,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Line':
        return cls(
            data['x1'], data['y1'],
            data['x2'], data['y2'],
            data.get('char', '-')
        )

    def is_within_bounds(self, width: int, height: int) -> bool:
        return all(0 <= v < width for v in (self.x1, self.x2)) and \
            all(0 <= v < height for v in (self.y1, self.y2))

    def draw(self, grid: list[list[str]]) -> None:
        h = len(grid)
        w = len(grid[0]) if h else 0
        dx = abs(self.x2 - self.x1)
        dy = abs(self.y2 - self.y1)
        sx = 1 if self.x1 < self.x2 else -1
        sy = 1 if self.y1 < self.y2 else -1
        err = dx - dy
        x, y = self.x1, self.y1

        while True:
            if 0 <= x < w and 0 <= y < h:
                grid[y][x] = self.char
            if x == self.x2 and y == self.y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def __str__(self) -> str:
        return (
            f"Line(id={self.id}, start=({self.x1},{self.y1}), "
            f"end=({self.x2},{self.y2}), char='{self.char}')"
        )


ShapeRegistry.register('Line', Line)
