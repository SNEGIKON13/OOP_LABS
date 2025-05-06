from .base import Command

class SetBackgroundCommand(Command):
    def __init__(self, canvas, shape, new_fill_char):
        self.canvas = canvas
        self.shape = shape
        self.new_fill_char = new_fill_char
        self._old_fill_char = None

    def execute(self):
        self._old_fill_char = getattr(self.shape, 'fill_char', None)
        self.shape.set_background(self.new_fill_char)

    def undo(self):
        self.shape.set_background(self._old_fill_char)