import json
from shapes.circle import Circle
from shapes.line import Line
from shapes.rectangle import Rectangle
from shapes.factory import create_shape

class Canvas:
    def __init__(self, width=80, height=18):
        self.width = width
        self.height = height
        self.grid = [['.' for _ in range(width)] for _ in range(height)]
        self.shapes = []
        self.next_id = 1
        self.background_char = '.'

    def add_shape(self, shape):
        shape.id = self.next_id
        self.next_id += 1
        self.shapes.append(shape)

    def remove_shape(self, shape_id):
        self.shapes = [s for s in self.shapes if s.id != shape_id]

    def render(self):
        self.grid = [['.' for _ in range(self.width)] for _ in range(self.height)]
        for shape in self.shapes:
            if isinstance(shape, Circle):
                self.draw_circle(shape.x, shape.y, shape.radius, shape.char, shape.fill_char)
            elif isinstance(shape, Line):
                self.draw_line(shape.x1, shape.y1, shape.x2, shape.y2, shape.char)
            elif isinstance(shape, Rectangle):
                self.draw_rectangle(shape.x1, shape.y1, shape.x2, shape.y2, shape.char, shape.fill_char)

    def draw_circle(self, x, y, radius, char, fill_char=None):
        if radius < 0:
            return
        if fill_char:
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    if dx * dx + dy * dy <= radius * radius:
                        px, py = x + dx, y + dy
                        if 0 <= px < self.width and 0 <= py < self.height:
                            self.grid[py][px] = fill_char
        x_pos = radius
        y_pos = 0
        err = 0
        while x_pos >= y_pos:
            for dx, dy in [(x_pos, y_pos), (-x_pos, y_pos), (x_pos, -y_pos), (-x_pos, -y_pos),
                           (y_pos, x_pos), (-y_pos, x_pos), (y_pos, -x_pos), (-y_pos, -x_pos)]:
                px, py = x + dx, y + dy
                if 0 <= px < self.width and 0 <= py < self.height:
                    self.grid[py][px] = char
            y_pos += 1
            err += 1 + 2 * y_pos
            if 2 * (err - x_pos) + 1 > 0:
                x_pos -= 1
                err += 1 - 2 * x_pos

    def draw_line(self, x1, y1, x2, y2, char):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            if 0 <= x1 < self.width and 0 <= y1 < self.height:
                self.grid[y1][x1] = char
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def draw_rectangle(self, x1, y1, x2, y2, border_char, fill_char):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                if x == x1 or x == x2 or y == y1 or y == y2:
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.grid[y][x] = border_char
                elif fill_char:
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.grid[y][x] = fill_char

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
            print(''.join(self.grid[y]))
        print(f"Canvas size: {self.width}x{self.height}")

    def save(self, filename):
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump([shape.to_dict() for shape in self.shapes], f)

    def load(self, filename):
        try:
            if not filename.endswith('.json'):
                filename += '.json'
            with open(filename, 'r') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("File content must be a list of shapes.")
                if not data:
                    self.shapes = []
                    self.next_id = 1
                    return
                self.shapes = []
                self.next_id = 1
                for shape_data in data:
                    shape = create_shape(shape_data)  # Используем create_shape вместо Shape.from_dict
                    self.add_shape(shape)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File '{filename}' not found. Please check the filename.")
        except json.JSONDecodeError:
            raise ValueError(f"Error: File '{filename}' contains invalid JSON. Please check the file content.")
        except Exception as e:
            raise Exception(f"Error: Failed to load file '{filename}'. Reason: {str(e)}")

    def list_shapes(self):
        return [f"{s.id}: {s}" for s in self.shapes]