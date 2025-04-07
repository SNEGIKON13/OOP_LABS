from shapes.shape import Shape

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