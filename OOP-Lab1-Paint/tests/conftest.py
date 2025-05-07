import pytest

from core.canvas import Canvas
from core.commands.manager import CommandManager
from core.canvas_file_manager import CanvasFileManager
from view.console_view import ConsoleView
from controller.input_handler import InputHandler


@pytest.fixture
def canvas():
    return Canvas(width=80, height=18)


@pytest.fixture
def command_manager(canvas):
    return CommandManager(canvas)


@pytest.fixture
def file_manager(canvas):
    return CanvasFileManager(canvas)


@pytest.fixture
def console_view(canvas):
    return ConsoleView(canvas)


@pytest.fixture
def input_handler(console_view):
    return InputHandler(console_view)
