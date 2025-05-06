from core.canvas import Canvas
from shapes.circle import Circle

def test_add_shape():
    canvas = Canvas(width=80, height=18)
    shape = Circle(40, 9, 3, '*')
    canvas.add_shape(shape)
    assert len(canvas.shapes) == 1
    assert canvas.shapes[0].id == 1

def test_remove_shape():
    canvas = Canvas(width=80, height=18)
    shape = Circle(40, 9, 3, '*')
    canvas.add_shape(shape)
    canvas.remove_shape(1)
    assert len(canvas.shapes) == 0

def test_get_shape_by_id():
    canvas = Canvas(width=80, height=18)
    shape = Circle(40, 9, 3, '*')
    canvas.add_shape(shape)
    retrieved = canvas.get_shape_by_id(1)
    assert retrieved == shape
    assert canvas.get_shape_by_id(999) is None

def test_render():
    canvas = Canvas(width=80, height=18)
    shape = Circle(40, 9, 1, '*')
    canvas.add_shape(shape)
    canvas.render()
    assert canvas._grid[8][40] == '*'  # Проверяем точку выше центра (на контуре)
    assert canvas._grid[10][40] == '*'  # Проверяем точку ниже центра