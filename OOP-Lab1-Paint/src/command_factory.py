from commands import AddShapeCommand, RemoveShapeCommand, MoveShapeCommand, SetBackgroundCommand, SetCharCommand

class CommandFactory:
    @staticmethod
    def create_add_shape_command(canvas, shape):
        return AddShapeCommand(canvas, shape)

    @staticmethod
    def create_remove_shape_command(canvas, shape_id):
        return RemoveShapeCommand(canvas, shape_id)

    @staticmethod
    def create_move_shape_command(shape, dx, dy):
        return MoveShapeCommand(shape, dx, dy)

    @staticmethod
    def create_set_background_command(shape, new_fill_char):
        return SetBackgroundCommand(shape, new_fill_char)

    @staticmethod
    def create_set_char_command(shape, new_char):
        return SetCharCommand(shape, new_char)