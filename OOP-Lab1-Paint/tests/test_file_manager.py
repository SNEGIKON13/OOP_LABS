import json
import pytest
from core.canvas_file_manager import CanvasFileManager
from shapes import Circle


class TestFileManager:
    def test_ensure_extension(self):
        mgr = CanvasFileManager(None)
        assert mgr._ensure_json_extension("a") == "a.json"
        assert mgr._ensure_json_extension("b.json") == "b.json"

    def test_save_and_load(self, tmp_path, canvas, file_manager):
        # создаём файл без расширения
        fn = tmp_path / "testfile"
        # добавим одну фигуру
        c = Circle(2, 2, 1)
        canvas.add_shape(c)
        file_manager.save(str(fn))
        # проверьте, что файл создался
        path = fn.with_suffix(".json")
        assert path.exists()
        # очистим холст и загрузим
        canvas.clear_shapes()
        file_manager.load(str(fn))
        # после загрузки фигура восстановилась
        shapes = canvas.shapes
        assert len(shapes) == 1
        assert shapes[0].x == 2 and shapes[0].y == 2 and shapes[0].radius == 1

    def test_load_not_found(self, tmp_path, file_manager):
        with pytest.raises(FileNotFoundError):
            file_manager.load(str(tmp_path / "no_such_file"))

    def test_load_invalid_json(self, tmp_path, file_manager):
        f = tmp_path / "bad.json"
        f.write_text("{ not valid json ")
        with pytest.raises(ValueError):
            file_manager.load(str(f))

    def test_load_non_list(self, tmp_path, file_manager):
        f = tmp_path / "obj.json"
        f.write_text(json.dumps({"type": "Circle"}))
        with pytest.raises(ValueError):
            file_manager.load(str(f))

    def test_load_unknown_type(self, tmp_path, file_manager):
        f = tmp_path / "unknown.json"
        f.write_text(json.dumps([{"type": "Nope"}]))
        with pytest.raises(ValueError):
            file_manager.load(str(f))
