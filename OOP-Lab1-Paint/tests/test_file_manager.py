from core.canvas_file_manager import CanvasFileManager
from core.canvas import Canvas
from shapes.circle import Circle

def test_save_load(tmp_path):
    canvas = Canvas(width=80, height=18)
    manager = CanvasFileManager(canvas)
    shape = Circle(40, 9, 3, '*')
    canvas.add_shape(shape)
    filename = tmp_path / "test.json"
    manager.save(str(filename))
    assert filename.exists()