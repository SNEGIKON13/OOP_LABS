from shapes.shape import Shape

class Line(Shape):
    def __init__(self, x1, y1, x2, y2, char='-'):
        super().__init__(char)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def move(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def to_dict(self):
        return {'type': 'Line', 'x1': self.x1, 'y1': self.y1, 'x2': self.x2, 'y2': self.y2, 'char': self.char}

    def draw(self, canvas):
        dx = abs(self.x2 - self.x1)
        dy = abs(self.y2 - self.y1)
        sx = 1 if self.x1 < self.x2 else -1
        sy = 1 if self.y1 < self.y2 else -1
        err = dx - dy
        x, y = self.x1, self.y1
        while True:
            if 0 <= x < canvas.width and 0 <= y < canvas.height:
                canvas.set_pixel(y, x, self.char)
            if x == self.x2 and y == self.y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def __str__(self):
        return f"Линия от ({self.x1},{self.y1}) до ({self.x2},{self.y2}) с символом='{self.char}'"