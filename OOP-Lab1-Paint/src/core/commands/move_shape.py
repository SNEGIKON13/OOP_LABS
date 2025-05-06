from .base import Command

class MoveShapeCommand(Command):
    def __init__(self, canvas, shape, dx, dy):
        self.canvas = canvas
        self.shape = shape
        self.dx = dx
        self.dy = dy
        self._old_x = None
        self._old_y = None

    def execute(self):
        self._old_x, self._old_y = self.shape.x, self.shape.y
        self.shape.move(self.dx, self.dy)

    def undo(self):
        self.shape.move(self._old_x - self.shape.x, self._old_y - self.shape.y)