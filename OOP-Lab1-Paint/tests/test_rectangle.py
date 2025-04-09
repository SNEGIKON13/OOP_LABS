import pytest
from shapes.rectangle import Rectangle
from canvas import Canvas

@pytest.fixture
def empty_canvas():
    """Фикстура для создания пустого холста 10x10."""
    return Canvas(10, 10)

def test_rectangle_constructor():
    """Проверяем, что конструктор правильно устанавливает свойства."""
    rect = Rectangle(0, 0, 10, 5, '*', fill_char='#')
    assert rect.x1 == 0
    assert rect.y1 == 0
    assert rect.x2 == 10
    assert rect.y2 == 5
    assert rect.char == '*'
    assert rect.fill_char == '#'

def test_rectangle_draw(empty_canvas):
    """Проверяем, что прямоугольник правильно отрисовывается на холсте."""
    rect = Rectangle(2, 2, 4, 4, '*', fill_char='#')
    empty_canvas.add_shape(rect)
    empty_canvas.render()
    assert empty_canvas.grid[2][2] == '*'  # Граница
    assert empty_canvas.grid[3][3] == '#'  # Заливка

def test_rectangle_move():
    """Проверяем, что прямоугольник правильно перемещается."""
    rect = Rectangle(0, 0, 10, 5, '*')
    rect.move(5, 5)
    assert rect.x1 == 5
    assert rect.y1 == 5
    assert rect.x2 == 15
    assert rect.y2 == 10

def test_rectangle_remove(empty_canvas):
    """Проверяем, что прямоугольник удаляется с холста."""
    rect = Rectangle(2, 2, 4, 4, '*')
    empty_canvas.add_shape(rect)
    empty_canvas.render()
    assert empty_canvas.grid[2][2] == '*'
    empty_canvas.remove_shape(rect.id)
    empty_canvas.render()
    assert empty_canvas.grid[2][2] == '.'

def test_rectangle_to_dict():
    """Проверяем, что метод to_dict возвращает правильный словарь."""
    rect = Rectangle(0, 0, 10, 5, '*', fill_char='#')
    assert rect.to_dict() == {
        'type': 'Rectangle',
        'x1': 0,
        'y1': 0,
        'x2': 10,
        'y2': 5,
        'border_char': '*',
        'fill_char': '#'
    }

def test_rectangle_width_zero():
    """Проверяем, что создание прямоугольника с шириной 0 вызывает ошибку."""
    with pytest.raises(ValueError):
        Rectangle(0, 0, 0, 5, '*')

def test_rectangle_partially_outside(empty_canvas):
    """Проверяем прямоугольник, частично выходящий за пределы холста."""
    rect = Rectangle(-2, -2, 5, 5, '*')
    empty_canvas.add_shape(rect)
    empty_canvas.render()
    assert empty_canvas.grid[5][0] == '*'  # Точка на верхней границе внутри холста

def test_rectangle_completely_outside(empty_canvas):
    """Проверяем прямоугольник полностью за пределами холста."""
    rect = Rectangle(100, 100, 105, 105, '*')
    empty_canvas.add_shape(rect)
    empty_canvas.render()
    assert all(cell == '.' for row in empty_canvas.grid for cell in row)