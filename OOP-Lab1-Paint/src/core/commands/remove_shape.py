from .base import Command


class RemoveShapeCommand(Command):

    def __init__(self, canvas, shape_id: int):
        self.canvas = canvas
        self.shape_id = shape_id

        self._shape_obj = canvas.get_shape_by_id(shape_id)

    def execute(self) -> None:
        self.canvas.remove_shape(self.shape_id)

    def undo(self) -> None:
        if self._shape_obj is not None:
            self.canvas.add_shape(self._shape_obj)
