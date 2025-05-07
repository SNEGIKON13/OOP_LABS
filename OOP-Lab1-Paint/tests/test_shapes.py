import pytest

from shapes import Circle, Rectangle, Line, ShapeRegistry


class TestCircle:
    def test_invalid_radius(self):
        with pytest.raises(ValueError):
            Circle(5, 5, 0)
        with pytest.raises(ValueError):
            Circle(5, 5, -1)

    def test_move(self):
        c = Circle(2, 3, 1)
        c.move(5, -1)
        assert (c.x, c.y) == (7, 2)

    def test_to_from_dict(self):
        c1 = Circle(4, 4, 2, char='*', fill_char='o')
        d = c1.to_dict()
        c2 = Circle.from_dict(d)
        assert c2.x == c1.x and c2.y == c1.y and c2.radius == c1.radius
        assert c2.char == c1.char and c2.fill_char == c1.fill_char

    def test_within_bounds(self):
        # fits
        assert Circle(3, 3, 2).is_within_bounds(10, 10)
        # too close to border
        assert not Circle(1, 1, 2).is_within_bounds(10, 10)

    def test_draw_outline_and_fill(self):
        # small grid
        grid = [['.' for _ in range(7)] for __ in range(7)]
        c = Circle(3, 3, 2, char='*', fill_char='+')
        c.draw(grid)
        # center must be fill
        assert grid[3][3] == '+'
        # one outline point
        assert grid[3 + 2][3] == '*'


class TestRectangle:
    def test_invalid_size(self):
        with pytest.raises(ValueError):
            Rectangle(0, 0, 0, 1)  # width < 1
        with pytest.raises(ValueError):
            Rectangle(0, 0, 1, 0)  # height < 1

    def test_move(self):
        r = Rectangle(1, 1, 3, 3)
        r.move(2, 3)
        assert (r.x1, r.y1, r.x2, r.y2) == (3, 4, 5, 6)

    def test_to_from_dict(self):
        r1 = Rectangle(1, 2, 4, 5, border_char='#', fill_char='.')
        d = r1.to_dict()
        r2 = Rectangle.from_dict(d)
        assert (r1.x1, r1.y1, r1.x2, r1.y2) == (r2.x1, r2.y1, r2.x2, r2.y2)
        assert r1.char == r2.char and r1.fill_char == r2.fill_char

    def test_within_bounds(self):
        assert Rectangle(0, 0, 2, 2).is_within_bounds(5, 5)
        assert not Rectangle(0, 0, 6, 2).is_within_bounds(5, 5)

    def test_draw_outline_and_fill(self):
        grid = [['.' for _ in range(5)] for __ in range(5)]
        # rectangle 3×3 with fill
        r = Rectangle(1, 1, 3, 3, border_char='*', fill_char='x')
        r.draw(grid)
        # corners
        assert grid[1][1] == '*'
        assert grid[3][3] == '*'
        # inside
        assert grid[2][2] == 'x'


class TestLine:
    def test_move(self):
        l = Line(0, 0, 2, 2)
        l.move(3, 4)
        assert (l.x1, l.y1, l.x2, l.y2) == (3, 4, 5, 6)

    def test_to_from_dict(self):
        l1 = Line(1, 1, 4, 5, char='-')
        d = l1.to_dict()
        l2 = Line.from_dict(d)
        assert (l1.x1, l1.y1, l1.x2, l1.y2) == (l2.x1, l2.y1, l2.x2, l2.y2)
        assert l1.char == l2.char

    def test_within_bounds(self):
        assert Line(0, 0, 4, 4).is_within_bounds(5, 5)
        assert not Line(0, 0, 5, 5).is_within_bounds(5, 5)

    def test_draw_horizontal(self):
        grid = [['.' for _ in range(5)] for __ in range(3)]
        l = Line(0, 1, 4, 1, char='-')
        l.draw(grid)
        assert ''.join(grid[1]) == '-----'

    def test_draw_diagonal(self):
        grid = [['.' for _ in range(4)] for __ in range(4)]
        l = Line(0, 0, 3, 3, char='*')
        l.draw(grid)
        for i in range(4):
            assert grid[i][i] == '*'


class TestRegistry:
    def test_create_known(self):
        data = {'type': 'Circle', 'x': 1, 'y': 1, 'radius': 1}
        obj = ShapeRegistry.create(data)
        assert isinstance(obj, Circle)

    def test_create_unknown(self):
        with pytest.raises(ValueError):
            ShapeRegistry.create({'type': 'Unknown'})

    def test_create_invalid_data(self):
        with pytest.raises(ValueError):
            ShapeRegistry.create(['not', 'a', 'dict'])
