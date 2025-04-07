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
        # Локальные импорты внутри метода
        from shapes.circle import Circle
        from shapes.line import Line
        from shapes.rectangle import Rectangle

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