import json
from shapes.shape_factory import ShapeFactory

class CanvasFileManager:
    def __init__(self, canvas):
        self.canvas = canvas

    @staticmethod
    def _ensure_json_extension(filename):
        if not filename.endswith('.json'):
            filename += '.json'
        return filename

    def save(self, filename):
        filename = self._ensure_json_extension(filename)
        with open(filename, 'w') as f:
            json.dump([shape.to_dict() for shape in self.canvas.shapes], f, indent=2)

    def load(self, filename):
        filename = self._ensure_json_extension(filename)
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("Содержимое файла должно быть списком фигур.")
                if not data:
                    self.canvas._shapes = []
                    self.canvas._next_id = 1
                    return
                self.canvas._shapes = []
                self.canvas._next_id = 1
                for shape_data in data:
                    shape = ShapeFactory.from_dict(shape_data)
                    self.canvas.add_shape(shape)
        except FileNotFoundError:
            raise FileNotFoundError(f"Ошибка: Файл '{filename}' не найден.")
        except json.JSONDecodeError:
            raise ValueError(f"Ошибка: Файл '{filename}' содержит некорректный JSON.")
        except Exception as e:
            raise Exception(f"Ошибка: Не удалось загрузить файл '{filename}'. Причина: {str(e)}")