import pytest
from shapes.circle import Circle
from canvas import Canvas
from paint_app import PaintApp, AddShapeCommand, MoveShapeCommand, RemoveShapeCommand

@pytest.fixture
def paint_app():
    """Фикстура для создания PaintApp с холстом 10x10."""
    app = PaintApp()
    app.canvas = Canvas(10, 10)
    return app

def test_paint_app_draw_shape(paint_app):
    """Проверяем добавление фигуры."""
    circle = Circle(5, 5, 2, '*')
    paint_app.execute_command(AddShapeCommand(paint_app.canvas, circle))
    assert len(paint_app.canvas.shapes) == 1
    paint_app.canvas.render()
    assert paint_app.canvas.grid[5][7] == '*'  # Проверяем точку на границе (правая)

def test_paint_app_move_shape(paint_app):
    """Проверяем перемещение фигуры."""
    circle = Circle(5, 5, 2, '*')
    paint_app.execute_command(AddShapeCommand(paint_app.canvas, circle))
    paint_app.execute_command(MoveShapeCommand(circle, 2, 2))
    assert circle.x == 7
    assert circle.y == 7

def test_paint_app_remove_shape(paint_app):
    """Проверяем удаление фигуры."""
    circle = Circle(5, 5, 2, '*')
    paint_app.execute_command(AddShapeCommand(paint_app.canvas, circle))
    paint_app.execute_command(RemoveShapeCommand(paint_app.canvas, circle.id))
    assert len(paint_app.canvas.shapes) == 0

def test_paint_app_undo_redo(paint_app):
    """Проверяем undo и redo."""
    circle = Circle(5, 5, 2, '*')
    paint_app.execute_command(AddShapeCommand(paint_app.canvas, circle))
    paint_app.undo()
    assert len(paint_app.canvas.shapes) == 0
    paint_app.redo()
    assert len(paint_app.canvas.shapes) == 1

def test_paint_app_save_load(paint_app, tmp_path):
    """Проверяем сохранение и загрузку."""
    circle = Circle(5, 5, 2, '*')
    paint_app.execute_command(AddShapeCommand(paint_app.canvas, circle))
    file_path = tmp_path / "test.json"
    paint_app.canvas.save(str(file_path))
    paint_app.canvas.load(str(file_path))
    assert len(paint_app.canvas.shapes) == 1