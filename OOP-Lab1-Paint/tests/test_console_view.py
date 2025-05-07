import sys
from io import StringIO

import pytest
from view.console_view import ConsoleView


class DummyCanvas:
    def __init__(self):
        self.width = 4
        self.height = 3
        self.bg_char = '.'
        self.fill_char = 'x'
        self._shapes = []

    @property
    def shapes(self):
        return list(self._shapes)

    def render_data(self):
        return [''.join(self.bg_char for _ in range(self.width))
                for __ in range(self.height)]

    def get_max_shape_id(self):
        return 0

    def clear_shapes(self):
        self._shapes.clear()


@pytest.fixture
def view():
    return ConsoleView(DummyCanvas())


def test_add_message_limit(view):
    for i in range(10):
        view.add_message(str(i))
    assert len(view.messages) == 5
    assert view.messages == ['5', '6', '7', '8', '9']


def test_display_shapes_empty(capfd, view):
    view.display_shapes()
    out = capfd.readouterr().out
    assert "На холсте нет фигур." in out

def test_display_messages_empty(capfd, view):
    view.display_messages()
    out = capfd.readouterr().out
    assert "Нет сообщений." in out

def test_display_canvas_and_menu(capfd, view):
    view.display_canvas()
    view.display_menu()
    out = capfd.readouterr().out
    # header row with X‑axis labels
    assert "   0" in out and str(view.canvas.width-1) in out
    # one row of field
    assert "0 " + view.canvas.bg_char*view.canvas.width in out
    # menu items
    assert "1. Нарисовать круг" in out
    assert "0. Выход" in out
