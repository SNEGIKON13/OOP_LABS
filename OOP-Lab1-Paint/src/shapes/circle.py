from shapes.shape import Shape

class Circle(Shape):
    def __init__(self, x, y, radius, char='*', fill_char=None):
        if radius <= 0:
            raise ValueError(f"Radius must be positive. You entered: {radius}")
        if radius < 0:
            raise ValueError(f"Radius must be non-negative. You entered: {radius}")
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