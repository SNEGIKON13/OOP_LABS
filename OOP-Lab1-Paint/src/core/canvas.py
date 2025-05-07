# core/canvas.py

from collections import deque
from shapes import Shape


class Canvas:
    def __init__(self, width=80, height=18, bg_char='.', fill_char='#'):
        self.width = width
        self.height = height
        self.bg_char = bg_char  # фон холста
        self.fill_char = fill_char  # символ автоматической заливки
        self._shapes = []  # список Shape
        self._next_id = 1

    @property
    def shapes(self):
        return list(self._shapes)

    def get_max_shape_id(self):
        return self._next_id - 1

    def add_shape(self, shape: Shape):
        if not shape.is_within_bounds(self.width, self.height):
            raise ValueError(f"Фигура {shape} выходит за пределы холста {self.width}×{self.height}")
        shape.id = self._next_id
        self._shapes.append(shape)
        self._next_id += 1

    def remove_shape(self, shape_id: int):
        self._shapes = [s for s in self._shapes if s.id != shape_id]

    def get_shape_by_id(self, shape_id: int):
        return next((s for s in self._shapes if s.id == shape_id), None)

    def clear_shapes(self):
        self._shapes.clear()
        self._next_id = 1

    def render_data(self) -> list[str]:
        # создаём пустую сетку
        grid = [[self.bg_char for _ in range(self.width)]
                for _ in range(self.height)]
        # рисуем все фигуры
        for shape in self._shapes:
            shape.draw(grid)
        # автоматическая заливка замкнутых областей
        self._fill_enclosed(grid)
        # конвертируем в строки
        return [''.join(row) for row in grid]

    def _fill_enclosed(self, grid):
        h, w = self.height, self.width
        bg, fill_ch = self.bg_char, self.fill_char

        # 1) Рисунок уже нанесён, всё, что != bg, считаем контуром
        # (этот set здесь уже не нужен, поэтому убираем переменную)

        # 2) BFS из всех пустых клеток на границе
        visited = [[False] * w for _ in range(h)]
        q = deque()

        # Добавляем на очередь все bg-клетки по периметру
        for x in range(w):
            if grid[0][x] == bg and not visited[0][x]:
                visited[0][x] = True
                q.append((0, x))
            if grid[h - 1][x] == bg and not visited[h - 1][x]:
                visited[h - 1][x] = True
                q.append((h - 1, x))
        for y in range(h):
            if grid[y][0] == bg and not visited[y][0]:
                visited[y][0] = True
                q.append((y, 0))
            if grid[y][w - 1] == bg and not visited[y][w - 1]:
                visited[y][w - 1] = True
                q.append((y, w - 1))

        # 3) Обычный BFS по 4‑м направлениям
        while q:
            y, x = q.popleft()
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w \
                        and not visited[ny][nx] \
                        and grid[ny][nx] == bg:
                    visited[ny][nx] = True
                    q.append((ny, nx))

        # 4) Всё, что осталось bg и не visited — внутренняя область
        for y in range(h):
            for x in range(w):
                if grid[y][x] == bg and not visited[y][x]:
                    grid[y][x] = fill_ch