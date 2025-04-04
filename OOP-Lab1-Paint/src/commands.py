from canvas import Canvas
from shapes import Shape

class Command:
    def execute(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError

# Команда AddShapeCommand
class AddShapeCommand(Command):
    def __init__(self, canvas, shape):
        self.canvas = canvas
        self.shape = shape

    def execute(self):
        self.canvas.add_shape(self.shape)

    def undo(self):
        self.canvas.remove_shape(self.shape.id)

# Команда RemoveShapeCommand
class RemoveShapeCommand(Command):
    def __init__(self, canvas, shape_id):
        self.canvas = canvas
        self.shape_id = shape_id
        self.shape = next((s for s in canvas.shapes if s.id == shape_id), None)
        self.index = canvas.shapes.index(self.shape) if self.shape else None

    def execute(self):
        if self.shape:
            self.canvas.shapes.pop(self.index)

    def undo(self):
        if self.shape:
            self.canvas.shapes.insert(self.index, self.shape)

# Команда MoveShapeCommand
class MoveShapeCommand(Command):
    def __init__(self, shape, dx, dy):
        self.shape = shape
        self.dx = dx
        self.dy = dy

    def execute(self):
        self.shape.move(self.dx, self.dy)

    def undo(self):
        self.shape.move(-self.dx, -self.dy)

# Команда SetBackgroundCommand
class SetBackgroundCommand(Command):
    def __init__(self, shape, new_fill_char):
        self.shape = shape
        self.new_fill_char = new_fill_char
        self.old_fill_char = shape.fill_char if hasattr(shape, 'fill_char') else None

    def execute(self):
        if hasattr(self.shape, 'set_background'):
            self.shape.set_background(self.new_fill_char)

    def undo(self):
        if hasattr(self.shape, 'set_background'):
            self.shape.set_background(self.old_fill_char)

# Команда SetCharCommand
class SetCharCommand(Command):
    def __init__(self, shape, new_char):
        self.shape = shape
        self.new_char = new_char
        self.old_char = shape.char

    def execute(self):
        self.shape.char = self.new_char

    def undo(self):
        self.shape.char = self.old_char