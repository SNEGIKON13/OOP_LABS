import pytest
from shapes.line import Line
from canvas import Canvas

@pytest.fixture
def empty_canvas():
    """Фикстура для создания пустого холста 10x10."""
    return Canvas(10, 10)

def test_line_constructor():
    """Проверяем, что конструктор правильно устанавливает свойства."""
    line = Line(0, 0, 5, 5, '-')
    assert line.x1 == 0
    assert line.y1 == 0
    assert line.x2 == 5
    assert line.y2 == 5
    assert line.char == '-'

def test_line_draw(empty_canvas):
    """Проверяем, что линия правильно отрисовывается на холсте."""
    line = Line(0, 0, 4, 4, '*')
    empty_canvas.add_shape(line)
    empty_canvas.render()
    assert empty_canvas.grid[0][0] == '*'
    assert empty_canvas.grid[2][2] == '*'
    assert empty_canvas.grid[4][4] == '*'

def test_line_draw_horizontal(empty_canvas):
    """Проверяем отрисовку горизонтальной линии."""
    line = Line(0, 5, 9, 5, '*')
    empty_canvas.add_shape(line)
    empty_canvas.render()
    for i in range(10):
        assert empty_canvas.grid[5][i] == '*'

def test_line_draw_vertical(empty_canvas):
    """Проверяем отрисовку вертикальной линии."""
    line = Line(5, 0, 5, 9, '*')
    empty_canvas.add_shape(line)
    empty_canvas.render()
    for i in range(10):
        assert empty_canvas.grid[i][5] == '*'

def test_line_move():
    """Проверяем, что линия правильно перемещается."""
    line = Line(0, 0, 5, 5, '*')
    line.move(2, 3)
    assert line.x1 == 2
    assert line.y1 == 3
    assert line.x2 == 7
    assert line.y2 == 8

def test_line_remove(empty_canvas):
    """Проверяем, что линия удаляется с холста."""
    line = Line(0, 0, 4, 4, '*')
    empty_canvas.add_shape(line)
    empty_canvas.render()
    assert empty_canvas.grid[0][0] == '*'
    empty_canvas.remove_shape(line.id)
    empty_canvas.render()
    assert empty_canvas.grid[0][0] == '.'

def test_line_to_dict():
    """Проверяем, что метод to_dict возвращает правильный словарь."""
    line = Line(0, 0, 5, 5, '-')
    assert line.to_dict() == {
        'type': 'Line',
        'x1': 0,
        'y1': 0,
        'x2': 5,
        'y2': 5,
        'char': '-'
    }

def test_line_same_points(empty_canvas):
    """Проверяем линию с совпадающими точками."""
    line = Line(2, 2, 2, 2, '*')
    empty_canvas.add_shape(line)
    empty_canvas.render()
    assert empty_canvas.grid[2][2] == '*'

def test_line_partially_outside(empty_canvas):
    """Проверяем линию, частично выходящую за пределы холста."""
    line = Line(0, 0, 15, 15, '*')
    empty_canvas.add_shape(line)
    empty_canvas.render()
    assert empty_canvas.grid[0][0] == '*'
    assert empty_canvas.grid[9][9] == '*'

def test_line_completely_outside(empty_canvas):
    """Проверяем линию полностью за пределами холста."""
    line = Line(100, 100, 105, 105, '*')
    empty_canvas.add_shape(line)
    empty_canvas.render()
    assert all(cell == '.' for row in empty_canvas.grid for cell in row)

