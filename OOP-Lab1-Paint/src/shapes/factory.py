from shapes.shape import Shape
from shapes.circle import Circle
from shapes.line import Line
from shapes.rectangle import Rectangle

def create_shape(data):
    if data['type'] == 'Circle':
        return Circle.from_dict(data)
    elif data['type'] == 'Line':
        return Line.from_dict(data)
    elif data['type'] == 'Rectangle':
        return Rectangle.from_dict(data)
    else:
        raise ValueError(f"Unknown shape type: {data['type']}")