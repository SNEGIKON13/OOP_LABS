import pytest

from core.canvas import Canvas
from shapes import Rectangle


class TestCanvas:
    def test_add_and_id(self, canvas):
        r1 = Rectangle(0, 0, 1, 1)
        canvas.add_shape(r1)
        assert r1.id == 1
        r2 = Rectangle(1, 1, 2, 2)
        canvas.add_shape(r2)
        assert r2.id == 2
        assert canvas.get_max_shape_id() == 2

    def test_add_out_of_bounds(self, canvas):
        # x2 beyond width
        r = Rectangle(0, 0, canvas.width, 1)
        with pytest.raises(ValueError):
            canvas.add_shape(r)

    def test_remove_get_clear(self, canvas):
        r = Rectangle(0, 0, 1, 1)
        canvas.add_shape(r)
        assert canvas.get_shape_by_id(r.id) is r
        canvas.remove_shape(r.id)
        assert canvas.get_shape_by_id(r.id) is None
        canvas.add_shape(r)
        canvas.clear_shapes()
        assert canvas.shapes == []
        assert canvas.get_max_shape_id() == 0

    def test_render_empty(self):
        c = Canvas(width=4, height=3, bg_char='.')
        data = c.render_data()
        assert len(data) == 3
        assert all(line == '....' for line in data)

    def test_render_fill_2x2(self):
        # rectangle 2×2 has no internal cell → border remains border_char
        c = Canvas(width=6, height=4, bg_char='.', fill_char='x')
        r = Rectangle(1, 1, 4, 2, border_char='*')
        c.add_shape(r)
        data = c.render_data()
        # проверяем любую «внутреннюю» точку – она окажется рамкой
        assert data[2][2] == '*'

    def test_render_fill_larger(self):
        # rectangle 4×4 has true interior → fill_char inside
        c = Canvas(width=8, height=6, bg_char='.', fill_char='x')
        r = Rectangle(1, 1, 5, 4, border_char='*')
        c.add_shape(r)
        data = c.render_data()
        # interior point
        assert data[3][3] == 'x'
