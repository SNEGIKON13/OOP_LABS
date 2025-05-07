from .base import Command


class MoveShapeCommand(Command):
    def __init__(self, canvas, shape, dx, dy):
        self.canvas = canvas
        self.shape = shape
        self.dx = dx
        self.dy = dy

    def execute(self) -> None:
        self.shape.move(self.dx, self.dy)

    def undo(self) -> None:
        self.shape.move(-self.dx, -self.dy)
