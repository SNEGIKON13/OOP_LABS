import json
from shapes import ShapeRegistry


class CanvasFileManager:
    def __init__(self, canvas):
        self.canvas = canvas

    @staticmethod
    def _ensure_json_extension(filename: str) -> str:
        return filename if filename.endswith('.json') else f"{filename}.json"

    def save(self, filename: str) -> None:
        filename = self._ensure_json_extension(filename)
        data = [shape.to_dict() for shape in self.canvas.shapes]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load(self, filename: str) -> None:
        filename = self._ensure_json_extension(filename)
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл '{filename}' не найден.")
        except json.JSONDecodeError:
            raise ValueError(f"Файл '{filename}' содержит некорректный JSON.")

        if not isinstance(data, list):
            raise ValueError("Содержимое файла должно быть списком фигур.")
        # сброс холста
        self.canvas.clear_shapes()
        # заполняем заново
        for item in data:
            shape = ShapeRegistry.create(item)
            self.canvas.add_shape(shape)
