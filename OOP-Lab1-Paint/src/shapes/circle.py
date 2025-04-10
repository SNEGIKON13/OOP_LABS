from shapes.shape import Shape

class Circle(Shape):
    def __init__(self, x, y, radius, char='*', fill_char=None):
        if radius <= 0:
            raise ValueError(f"Радиус должен быть положительным. Введено: {radius}")
        if radius > 9:  # Ограничение для холста 80x18
            raise ValueError(f"Радиус не должен превышать 9. Введено: {radius}")
        super().__init__(char)
        if fill_char is not None:
            self._validate_char(fill_char, "fill_char")
        self.x = x
        self.y = y
        self.radius = radius
        self.fill_char = fill_char

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def set_background(self, fill_char):
        self._validate_char(fill_char, "fill_char")
        self.fill_char = fill_char

    def to_dict(self):
        return {'type': 'Circle', 'x': self.x, 'y': self.y, 'radius': self.radius, 'char': self.char, 'fill_char': self.fill_char}

    def draw(self, canvas):
        if self.radius <= 0:
            return
        if self.fill_char:
            for dy in range(-self.radius, self.radius + 1):
                for dx in range(-self.radius, self.radius + 1):
                    if dx * dx + dy * dy <= self.radius * self.radius:
                        px, py = self.x + dx, self.y + dy
                        if 0 <= px < canvas.width and 0 <= py < canvas.height:
                            canvas.set_pixel(py, px, self.fill_char)
        x_pos = self.radius
        y_pos = 0
        err = 0
        while x_pos >= y_pos:
            for dx, dy in [(x_pos, y_pos), (-x_pos, y_pos), (x_pos, -y_pos), (-x_pos, -y_pos),
                           (y_pos, x_pos), (-y_pos, x_pos), (y_pos, -x_pos), (-y_pos, -x_pos)]:
                px, py = self.x + dx, self.y + dy
                if 0 <= px < canvas.width and 0 <= py < canvas.height:
                    canvas.set_pixel(py, px, self.char)
            y_pos += 1
            err += 1 + 2 * y_pos
            if 2 * (err - x_pos) + 1 > 0:
                x_pos -= 1
                err += 1 - 2 * x_pos

    def __str__(self):
        return f"Круг в ({self.x},{self.y}) с радиусом={self.radius}, символ='{self.char}', заливка='{self.fill_char}'"