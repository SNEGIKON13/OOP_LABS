from shapes.shape import Shape

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