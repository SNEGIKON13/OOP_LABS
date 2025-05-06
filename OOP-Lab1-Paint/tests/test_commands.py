from command_factory import CommandFactory
from command_manager import CommandManager
from core.canvas import Canvas
from shapes.circle import Circle

def test_add_shape_command():
    canvas = Canvas(width=80, height=18)
    manager = CommandManager()
    shape = Circle(40, 9, 3, '*')
    cmd = CommandFactory.create_add_shape_command(canvas, shape)
    manager.execute(cmd)
    assert len(canvas.shapes) == 1