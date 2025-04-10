from shapes.shape import Shape

class Rectangle(Shape):
    def __init__(self, x1, y1, x2, y2, border_char='*', fill_char=None):
        super().__init__(border_char)
        self.x1, self.y1 = min(x1, x2), min(y1, y2)
        self.x2, self.y2 = max(x1, x2), max(y1, y2)
        if self.x2 - self.x1 < 1 or self.y2 - self.y1 < 1:
            raise ValueError("Прямоугольник должен быть размером минимум 2x2.")
        if fill_char is not None:
            self._validate_char(fill_char, "fill_char")
        self.fill_char = fill_char

    def move(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def set_background(self, fill_char):
        self._validate_char(fill_char, "fill_char")
        self.fill_char = fill_char

    def to_dict(self):
        return {'type': 'Rectangle', 'x1': self.x1, 'y1': self.y1, 'x2': self.x2, 'y2': self.y2,
                'border_char': self.char, 'fill_char': self.fill_char}

    def draw(self, canvas):
        for x in range(self.x1, self.x2 + 1):
            for y in range(self.y1, self.y2 + 1):
                if x == self.x1 or x == self.x2 or y == self.y1 or y == self.y2:
                    if 0 <= x < canvas.width and 0 <= y < canvas.height:
                        canvas.set_pixel(y, x, self.char)
                elif self.fill_char:
                    if 0 <= x < canvas.width and 0 <= y < canvas.height:
                        canvas.set_pixel(y, x, self.fill_char)

    def __str__(self):
        return f"Прямоугольник от ({self.x1},{self.y1}) до ({self.x2},{self.y2}) с границей='{self.char}' и заливкой='{self.fill_char}'"