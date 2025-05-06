from .base import Command

class SetCharCommand(Command):
    def __init__(self, canvas, shape, new_char):
        self.canvas = canvas
        self.shape = shape
        self.new_char = new_char
        self._old_char = None

    def execute(self):
        self._old_char = self.shape.char
        self.shape.char = self.new_char

    def undo(self):
        self.shape.char = self._old_char