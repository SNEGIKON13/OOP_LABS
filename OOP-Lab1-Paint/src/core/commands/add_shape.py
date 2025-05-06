from .base import Command

class AddShapeCommand(Command):
    def __init__(self, canvas, shape):
        self.canvas = canvas
        self.shape = shape

    def execute(self):
        self.canvas.add_shape(self.shape)

    def undo(self):
        self.canvas.remove_shape(self.shape.id)