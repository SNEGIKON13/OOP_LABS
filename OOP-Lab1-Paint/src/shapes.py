class Shape:
    def __init__(self, char='*'):
        self.id = None
        self.char = char

    def move(self, dx, dy):
        raise NotImplementedError

    def to_dict(self):
        raise NotImplementedError

    @staticmethod
    def from_dict(data):
        shape = None
        if data['type'] == 'Circle':
            shape = Circle.from_dict(data)
        elif data['type'] == 'Line':
            shape = Line.from_dict(data)
        elif data['type'] == 'Rectangle':
            shape = Rectangle.from_dict(data)
        else:
            raise ValueError(f"Unknown shape type: {data['type']}")
        return shape

    def __str__(self):
        raise NotImplementedError

# Класс Circle
class Circle(Shape):
    def __init__(self, x, y, radius, char='*', fill_char=None):
        super().__init__(char)
        self.x = x
        self.y = y
        self.radius = radius
        self.fill_char = fill_char

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def set_background(self, fill_char):
        self.fill_char = fill_char

    def to_dict(self):
        return {'type': 'Circle', 'x': self.x, 'y': self.y, 'radius': self.radius, 'char': self.char, 'fill_char': self.fill_char}

    @staticmethod
    def from_dict(data):
        return Circle(data['x'], data['y'], data['radius'], data['char'], data.get('fill_char'))

    def __str__(self):
        return f"Circle at ({self.x},{self.y}) with radius={self.radius} and char='{self.char}' and fill='{self.fill_char}'"

# Класс Line
class Line(Shape):
    def __init__(self, x1, y1, x2, y2, char='-'):
        super().__init__(char)
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2

    def move(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def to_dict(self):
        return {'type': 'Line', 'x1': self.x1, 'y1': self.y1, 'x2': self.x2, 'y2': self.y2, 'char': self.char}

    @staticmethod
    def from_dict(data):
        return Line(data['x1'], data['y1'], data['x2'], data['y2'], data['char'])

    def __str__(self):
        return f"Line from ({self.x1},{self.y1}) to ({self.x2},{self.y2}) with char='{self.char}'"

# Класс Rectangle
class Rectangle(Shape):
    def __init__(self, x1, y1, x2, y2, border_char='*', fill_char=None):
        super().__init__(border_char)
        self.x1, self.y1 = min(x1, x2), min(y1, y2)
        self.x2, self.y2 = max(x1, x2), max(y1, y2)
        self.fill_char = fill_char

    def move(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def set_background(self, fill_char):
        self.fill_char = fill_char

    def to_dict(self):
        return {'type': 'Rectangle', 'x1': self.x1, 'y1': self.y1, 'x2': self.x2, 'y2': self.y2,
                'border_char': self.char, 'fill_char': self.fill_char}

    @staticmethod
    def from_dict(data):
        return Rectangle(data['x1'], data['y1'], data['x2'], data['y2'], data['border_char'], data.get('fill_char'))

    def __str__(self):
        return f"Rectangle from ({self.x1},{self.y1}) to ({self.x2},{self.y2}) with border='{self.char}' and fill='{self.fill_char}'"