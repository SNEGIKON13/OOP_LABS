from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class AddShapeCommand(Command):
    def __init__(self, canvas, shape):
        self.canvas = canvas
        self.shape = shape

    def execute(self):
        self.canvas.add_shape(self.shape)
        self.canvas.render()

    def undo(self):
        self.canvas.remove_shape(self.shape.id)
        self.canvas.render()

class RemoveShapeCommand(Command):
    def __init__(self, canvas, shape_id):
        self.canvas = canvas
        self.shape_id = shape_id
        self.shape = self.canvas.get_shape_by_id(shape_id)

    def execute(self):
        if self.shape:
            self.canvas.remove_shape(self.shape_id)
            self.canvas.render()

    def undo(self):
        if self.shape:
            self.canvas.add_shape(self.shape)
            self.canvas.render()

class MoveShapeCommand(Command):
    def __init__(self, canvas, shape, dx, dy):
        self.canvas = canvas
        self.shape = shape
        self.dx = dx
        self.dy = dy

    def execute(self):
        self.shape.move(self.dx, self.dy)
        self.canvas.render()

    def undo(self):
        self.shape.move(-self.dx, -self.dy)
        self.canvas.render()

class SetBackgroundCommand(Command):
    def __init__(self, canvas, shape, new_fill_char):
        self.canvas = canvas
        self.shape = shape
        self.new_fill_char = new_fill_char
        self.old_fill_char = shape.fill_char if hasattr(shape, 'fill_char') else None

    def execute(self):
        if hasattr(self.shape, 'set_background'):
            self.shape.set_background(self.new_fill_char)
            self.canvas.render()

    def undo(self):
        if hasattr(self.shape, 'set_background'):
            self.shape.set_background(self.old_fill_char)
            self.canvas.render()

class SetCharCommand(Command):
    def __init__(self, canvas, shape, new_char):
        self.canvas = canvas
        self.shape = shape
        self.new_char = new_char
        self.old_char = shape.char

    def execute(self):
        self.shape.char = self.new_char
        self.canvas.render()

    def undo(self):
        self.shape.char = self.old_char
        self.canvas.render()