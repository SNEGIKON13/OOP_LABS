from shapes.circle import Circle
from shapes.line import Line
from shapes.rectangle import Rectangle

class Canvas:
    def __init__(self, width=80, height=18):
        self.width = width
        self.height = height
        self._grid = [['.' for _ in range(width)] for _ in range(height)]
        self._shapes = []
        self._next_id = 1

    @property
    def shapes(self):
        return self._shapes

    def add_shape(self, shape):
        if isinstance(shape, Circle):
            if not (0 <= shape.x < self.width and 0 <= shape.y < self.height):
                raise ValueError(f"Центр круга должен быть внутри холста (0-{self.width-1}, 0-{self.height-1}). Введено: ({shape.x}, {shape.y})")
        elif isinstance(shape, Rectangle):
            if not (0 <= shape.x1 < self.width and 0 <= shape.y1 < self.height and
                    0 <= shape.x2 < self.width and 0 <= shape.y2 < self.height):
                raise ValueError(f"Координаты прямоугольника должны быть внутри холста (0-{self.width-1}, 0-{self.height-1}). Введено: ({shape.x1}, {shape.y1}, {shape.x2}, {shape.y2})")
        elif isinstance(shape, Line):
            if not (0 <= shape.x1 < self.width and 0 <= shape.y1 < self.height and
                    0 <= shape.x2 < self.width and 0 <= shape.y2 < self.height):
                raise ValueError(f"Координаты линии должны быть внутри холста (0-{self.width-1}, 0-{self.height-1}). Введено: ({shape.x1}, {shape.y1}, {shape.x2}, {shape.y2})")
        shape.id = self._next_id
        self._shapes.append(shape)
        self._next_id += 1

    def remove_shape(self, shape_id):
        self._shapes = [s for s in self._shapes if s.id != shape_id]

    def get_shape_by_id(self, shape_id):
        return next((s for s in self._shapes if s.id == shape_id), None)

    def clear_shapes(self):
        self._shapes = []
        self._next_id = 1

    def render(self):
        self._grid = [['.' for _ in range(self.width)] for _ in range(self.height)]
        for shape in self._shapes:
            shape.draw(self)

    def set_pixel(self, y, x, char):
        if 0 <= x < self.width and 0 <= y < self.height:
            self._grid[y][x] = char

    def print_grid(self):
        col_nums = [' '] * (self.width + 3)
        for i in range(0, self.width, 10):
            num_str = str(i)
            col_nums[i + 3] = num_str[0]
            if i >= 10:
                col_nums[i + 4] = num_str[1]
        col_nums[-2] = '7'
        col_nums[-1] = '9'
        print(''.join(col_nums))
        for y in range(self.height):
            print(f'{y:2d} ', end='')
            print(''.join(self._grid[y]))
        print(f"Размер холста: {self.width}x{self.height}")

    def list_shapes(self):
        return [f"{s.id}: {s}" for s in self._shapes]