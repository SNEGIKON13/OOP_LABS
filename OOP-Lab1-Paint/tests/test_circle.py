import pytest
from shapes.circle import Circle
from canvas import Canvas

@pytest.fixture
def empty_canvas():
    """Фикстура для создания пустого холста 10x10."""
    return Canvas(10, 10)

def test_circle_constructor():
    """Проверяем, что конструктор правильно устанавливает свойства."""
    circle = Circle(5, 5, 3, '*', fill_char='#')
    assert circle.x == 5
    assert circle.y == 5
    assert circle.radius == 3
    assert circle.char == '*'
    assert circle.fill_char == '#'

def test_circle_draw(empty_canvas):
    """Проверяем, что круг правильно отрисовывается на холсте (только граница)."""
    circle = Circle(5, 5, 2, '*')
    empty_canvas.add_shape(circle)
    empty_canvas.render()
    # Проверяем точки на границе
    assert empty_canvas.grid[5][7] == '*'  # Правая точка
    assert empty_canvas.grid[5][3] == '*'  # Левая точка
    assert empty_canvas.grid[7][5] == '*'  # Нижняя точка
    assert empty_canvas.grid[3][5] == '*'  # Верхняя точка
    assert empty_canvas.grid[5][5] == '.'  # Центр должен быть пустым

def test_circle_move():
    """Проверяем, что круг правильно перемещается."""
    circle = Circle(0, 0, 3, '*')
    circle.move(2, 3)
    assert circle.x == 2
    assert circle.y == 3

def test_circle_remove(empty_canvas):
    """Проверяем, что круг удаляется с холста."""
    circle = Circle(5, 5, 2, '*')
    empty_canvas.add_shape(circle)
    empty_canvas.render()
    assert empty_canvas.grid[5][7] == '*'  # Проверяем точку на границе (правая)
    empty_canvas.remove_shape(circle.id)
    empty_canvas.render()
    assert empty_canvas.grid[5][7] == '.'  # После удаления точка должна быть пустой

def test_circle_to_dict():
    """Проверяем, что метод to_dict возвращает правильный словарь."""
    circle = Circle(0, 0, 3, '*', fill_char='#')
    assert circle.to_dict() == {
        'type': 'Circle',
        'x': 0,
        'y': 0,
        'radius': 3,
        'char': '*',
        'fill_char': '#'
    }

def test_circle_str():
    """Проверяем строковое представление круга."""
    circle = Circle(0, 0, 3, '*', fill_char='#')
    assert str(circle) == "Circle at (0,0) with radius=3 and char='*' and fill='#'"

def test_circle_radius_zero():
    """Проверяем, что создание круга с радиусом 0 вызывает ошибку."""
    with pytest.raises(ValueError):
        Circle(5, 5, 0, '*')

def test_circle_negative_radius():
    """Проверяем, что отрицательный радиус вызывает ошибку."""
    with pytest.raises(ValueError):
        Circle(5, 5, -3, '*')

def test_circle_partially_outside(empty_canvas):
    """Проверяем круг, частично выходящий за пределы холста."""
    circle = Circle(-2, -2, 5, '*')
    empty_canvas.add_shape(circle)
    empty_canvas.render()
    assert empty_canvas.grid[2][1] == '*'  # Точка на границе внутри холста

def test_circle_completely_outside(empty_canvas):
    """Проверяем, что круг полностью за пределами холста не рисуется."""
    circle = Circle(100, 100, 5, '*')
    empty_canvas.add_shape(circle)
    empty_canvas.render()
    assert all(cell == '.' for row in empty_canvas.grid for cell in row)

def test_circle_on_edge(empty_canvas):
    """Проверяем круг на краю холста."""
    circle = Circle(9, 9, 2, '*')
    empty_canvas.add_shape(circle)
    empty_canvas.render()
    assert empty_canvas.grid[9][7] == '*'  # Точка на левой границе