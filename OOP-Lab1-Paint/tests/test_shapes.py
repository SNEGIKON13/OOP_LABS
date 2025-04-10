import pytest
from shapes.circle import Circle
from shapes.line import Line
from shapes.rectangle import Rectangle

def test_circle_creation():
    circle = Circle(40, 9, 3, '*', '#')
    assert circle.x == 40
    assert circle.radius == 3

def test_line_creation():
    line = Line(0, 0, 79, 17, '-')
    assert line.x1 == 0
    assert line.x2 == 79

def test_rectangle_creation():
    rect = Rectangle(1, 1, 4, 4, '*', '#')
    assert rect.x1 == 1
    assert rect.x2 == 4 