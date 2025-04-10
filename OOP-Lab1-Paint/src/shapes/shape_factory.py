class ShapeFactory:
    _shape_classes = {}

    @classmethod
    def register_shape(cls, shape_type, shape_class):
        cls._shape_classes[shape_type] = shape_class

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Данные должны быть словарем")
        if 'type' not in data:
            raise ValueError("Данные должны содержать ключ 'type'")
        shape_type = data['type']
        if shape_type not in cls._shape_classes:
            raise ValueError(f"Неизвестный тип фигуры: {shape_type}")
        return cls._shape_classes[shape_type].from_dict(data)