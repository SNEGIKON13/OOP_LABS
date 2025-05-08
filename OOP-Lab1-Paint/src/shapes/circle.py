from .shape import Shape
from .registry import ShapeRegistry
from collections import deque


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
        x0, y0 = self.x, self.y

        # Множество для хранения клеток контура
        contour_cells = set()

        # Рисуем контур (алгоритм Брезенхэма)
        x = self.radius
        y = 0
        err = 0
        while x >= y:
            for sx, sy in ((x, y), (-x, y), (x, -y), (-x, -y), (y, x), (-y, x), (y, -x), (-y, -x)):
                px, py = x0 + sx, y0 + sy
                if 0 <= px < w and 0 <= py < h:
                    grid[py][px] = self.char
                    contour_cells.add((px, py))
            y += 1
            err += 1 + 2 * y
            if 2 * (err - x) + 1 > 0:
                x -= 1
                err += 1 - 2 * x

        # Заливка с помощью BFS, начиная из центра
        if self.fill_char and 0 <= x0 < w and 0 <= y0 < h and (x0, y0) not in contour_cells:
            q = deque([(y0, x0)])
            visited = {(y0, x0)}
            while q:
                cy, cx = q.popleft()
                if grid[cy][cx] != self.char and grid[cy][cx] != self.fill_char:
                    grid[cy][cx] = self.fill_char
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = cy + dy, cx + dx
                    if (0 <= nx < w and 0 <= ny < h and
                            (nx, ny) not in contour_cells and
                            (ny, nx) not in visited and
                            grid[ny][nx] != self.char):
                        q.append((ny, nx))
                        visited.add((ny, nx))

    def set_background(self, new_fill_char: str | None):
        if new_fill_char is not None:
            self._validate_char(new_fill_char, "fill_char")
        self.fill_char = new_fill_char

    def __str__(self) -> str:
        return (
            f"Circle(id={self.id}, center=({self.x},{self.y}), "
            f"r={self.radius}, char='{self.char}', fill='{self.fill_char}')"
        )


ShapeRegistry.register('Circle', Circle)
