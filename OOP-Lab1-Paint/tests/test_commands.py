import pytest

from shapes import Circle, Rectangle
from core.commands.add_shape import AddShapeCommand
from core.commands.remove_shape import RemoveShapeCommand
from core.commands.move_shape import MoveShapeCommand
from core.commands.set_background import SetBackgroundCommand
from core.commands.set_char import SetCharCommand


@pytest.fixture(autouse=True)
def ensure_set_background_on_shapes(monkeypatch):
    # если у фигур нет метода set_background, добавим его
    def _set_background(self, ch):
        self.fill_char = ch
    monkeypatch.setattr(Rectangle, 'set_background', _set_background, raising=False)
    monkeypatch.setattr(Circle, 'set_background', _set_background, raising=False)


class TestCommands:
    def test_add_undo(self, canvas, command_manager):
        c = Circle(2, 2, 1)
        cmd = AddShapeCommand(canvas, c)
        command_manager.execute(cmd)
        assert c in canvas.shapes
        command_manager.undo()
        assert c not in canvas.shapes

    def test_remove_undo(self, canvas, command_manager):
        c = Circle(2, 2, 1)
        canvas.add_shape(c)
        cmd = RemoveShapeCommand(canvas, c.id)
        command_manager.execute(cmd)
        assert c not in canvas.shapes
        command_manager.undo()
        # проверяем, что объект вернулся
        assert c in canvas.shapes

    def test_move_undo(self, canvas, command_manager):
        c = Circle(2, 2, 1)
        canvas.add_shape(c)
        cmd = MoveShapeCommand(canvas, c, 3, 4)
        command_manager.execute(cmd)
        assert (c.x, c.y) == (5, 6)
        command_manager.undo()
        assert (c.x, c.y) == (2, 2)

    def test_set_background_and_undo(self, canvas, command_manager):
        r = Rectangle(1, 1, 3, 3, fill_char='o')
        canvas.add_shape(r)
        cmd = SetBackgroundCommand(canvas, r, 'x')
        command_manager.execute(cmd)
        assert r.fill_char == 'x'
        command_manager.undo()
        assert r.fill_char == 'o'

    def test_set_char_and_undo(self, canvas, command_manager):
        r = Rectangle(1, 1, 3, 3, border_char='*')
        canvas.add_shape(r)
        cmd = SetCharCommand(canvas, r, '+')
        command_manager.execute(cmd)
        assert r.char == '+'
        command_manager.undo()
        assert r.char == '*'

    def test_manager_redo(self, canvas, command_manager):
        c = Circle(2, 2, 1)
        cmd = AddShapeCommand(canvas, c)
        command_manager.execute(cmd)
        command_manager.undo()
        assert c not in canvas.shapes
        command_manager.redo()
        assert c in canvas.shapes
