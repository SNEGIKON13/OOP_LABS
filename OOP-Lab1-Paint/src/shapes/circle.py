from .shape import Shape
from .registry import ShapeRegistry


class Circle(Shape):
    def __init__(
            self,
            x: int,
            y: int,
            radius: int,
            char: str = '*',
            fill_char: str | None = None
    ):
        if radius <= 0:
            raise ValueError(f"Радиус должен быть >0, а не {radius}")
        super().__init__(char)
        if fill_char is not None:
            self._validate_char(fill_char, "fill_char")
        self.x = x
        self.y = y
        self.radius = radius
        self.fill_char = fill_char

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

    def to_dict(self) -> dict:
        return {
            'type': 'Circle',
            'x': self.x,
            'y': self.y,
            'radius': self.radius,
            'char': self.char,
            'fill_char': self.fill_char,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Circle':
        return cls(
            data['x'], data['y'], data['radius'],
            data.get('char', '*'),
            data.get('fill_char')
        )

    def is_within_bounds(self, width: int, height: int) -> bool:
        return (
                self.radius <= self.x < width - self.radius and
                self.radius <= self.y < height - self.radius
        )

    def draw(self, grid: list[list[str]]) -> None:
        h = len(grid)
        w = len(grid[0]) if h else 0

        # заливка
        if self.fill_char:
            for dy in range(-self.radius, self.radius + 1):
                for dx in range(-self.radius, self.radius + 1):
                    if dx * dx + dy * dy <= self.radius * self.radius:
                        px, py = self.x + dx, self.y + dy
                        if 0 <= px < w and 0 <= py < h:
                            grid[py][px] = self.fill_char

        # контур (алгоритм Брезенхэма)
        x0, y0 = self.x, self.y
        x = self.radius
        y = 0
        err = 0
        while x >= y:
            for sx, sy in ((x, y), (-x, y), (x, -y), (-x, -y), (y, x), (-y, x), (y, -x), (-y, -x)):
                px, py = x0 + sx, y0 + sy
                if 0 <= px < w and 0 <= py < h:
                    grid[py][px] = self.char
            y += 1
            err += 1 + 2 * y
            if 2 * (err - x) + 1 > 0:
                x -= 1
                err += 1 - 2 * x

    def __str__(self) -> str:
        return (
            f"Circle(id={self.id}, center=({self.x},{self.y}), "
            f"r={self.radius}, char='{self.char}', fill='{self.fill_char}')"
        )


# Автоматическая регистрация
ShapeRegistry.register('Circle', Circle)
