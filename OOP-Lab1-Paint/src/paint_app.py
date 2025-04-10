import os
import time
from input_handler import InputHandler
from console_view import ConsoleView
from command_manager import CommandManager
from shapes.shape_factory import ShapeFactory
from command_factory import CommandFactory
from canvas import Canvas
from canvas_file_manager import CanvasFileManager
from shapes.circle import Circle
from shapes.line import Line
from shapes.rectangle import Rectangle

class PaintApp:
    def __init__(self):
        self.canvas = Canvas(width=80, height=18)
        self.file_manager = CanvasFileManager(self.canvas)
        self.console_view = ConsoleView()
        self.input_handler = InputHandler(self.console_view)
        self.command_manager = CommandManager()
        ShapeFactory.register_shape('Circle', Circle)
        ShapeFactory.register_shape('Line', Line)
        ShapeFactory.register_shape('Rectangle', Rectangle)

    def run(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.canvas.render()
            self.console_view.display_canvas(self.canvas)
            self.console_view.display_shapes(self.canvas.list_shapes())
            self.console_view.display_messages()
            self.console_view.display_menu()
            choice = self.input_handler.get_int("Введите выбор: ", 0, 11)
            if choice == 0:
                break
            elif choice == 1:
                self._draw_circle()
            elif choice == 2:
                self._draw_line()
            elif choice == 3:
                self._draw_rectangle()
            elif choice == 4:
                self._erase_shape()
            elif choice == 5:
                self._move_shape()
            elif choice == 6:
                self._set_background()
            elif choice == 7:
                self._set_shape_char()
            elif choice == 8:
                self._save()
            elif choice == 9:
                self._load()
            elif choice == 10:
                self._undo()
            elif choice == 11:
                self._redo()
            time.sleep(1)

    def _draw_circle(self):
        try:
            x = self.input_handler.get_int("Введите x (0-79): ", 0, 79)
            y = self.input_handler.get_int("Введите y (0-17): ", 0, 17)
            radius = self.input_handler.get_int("Введите радиус (1-9): ", 1, 9)
            char = self.input_handler.get_char("Введите символ (по умолчанию '*'): ", allow_empty=True) or '*'
            fill_char = self.input_handler.get_char("Введите символ заливки (опционально): ", allow_empty=True)
            shape = Circle(x, y, radius, char, fill_char)
            command = CommandFactory.create_add_shape_command(self.canvas, shape)
            self.command_manager.execute(command)
            self.console_view.add_message("Круг успешно добавлен.")
        except ValueError as e:
            self.console_view.add_message(f"Ошибка: {str(e)}")

    def _draw_line(self):
        try:
            x1 = self.input_handler.get_int("Введите x1 (0-79): ", 0, 79)
            y1 = self.input_handler.get_int("Введите y1 (0-17): ", 0, 17)
            x2 = self.input_handler.get_int("Введите x2 (0-79): ", 0, 79)
            y2 = self.input_handler.get_int("Введите y2 (0-17): ", 0, 17)
            char = self.input_handler.get_char("Введите символ (по умолчанию '-'): ", allow_empty=True) or '-'
            shape = Line(x1, y1, x2, y2, char)
            command = CommandFactory.create_add_shape_command(self.canvas, shape)
            self.command_manager.execute(command)
            self.console_view.add_message("Линия успешно добавлена.")
        except ValueError as e:
            self.console_view.add_message(f"Ошибка: {str(e)}")

    def _draw_rectangle(self):
        try:
            x1 = self.input_handler.get_int("Введите x1 (0-79): ", 0, 79)
            y1 = self.input_handler.get_int("Введите y1 (0-17): ", 0, 17)
            x2 = self.input_handler.get_int("Введите x2 (0-79): ", 0, 79)
            y2 = self.input_handler.get_int("Введите y2 (0-17): ", 0, 17)
            border_char = self.input_handler.get_char("Введите символ границы (по умолчанию '*'): ", allow_empty=True) or '*'
            fill_char = self.input_handler.get_char("Введите символ заливки (опционально): ", allow_empty=True)
            shape = Rectangle(x1, y1, x2, y2, border_char, fill_char)
            command = CommandFactory.create_add_shape_command(self.canvas, shape)
            self.command_manager.execute(command)
            self.console_view.add_message("Прямоугольник успешно добавлен.")
        except ValueError as e:
            self.console_view.add_message(f"Ошибка: {str(e)}")

    def _erase_shape(self):
        if not self.canvas.list_shapes():
            self.console_view.add_message("Ошибка: Нет фигур для удаления.")
            return
        shape_id = self.input_handler.get_int("Введите ID фигуры для удаления: ", 1, self.canvas._next_id - 1)
        if self.canvas.get_shape_by_id(shape_id) is None:
            self.console_view.add_message("Ошибка: Фигура с таким ID не найдена.")
            return
        command = CommandFactory.create_remove_shape_command(self.canvas, shape_id)
        self.command_manager.execute(command)
        self.console_view.add_message(f"Фигура с ID {shape_id} успешно удалена.")

    def _move_shape(self):
        if not self.canvas.list_shapes():
            self.console_view.add_message("Ошибка: Нет фигур для перемещения.")
            return
        shape_id = self.input_handler.get_int("Введите ID фигуры для перемещения: ", 1, self.canvas._next_id - 1)
        shape = self.canvas.get_shape_by_id(shape_id)
        if shape is None:
            self.console_view.add_message("Ошибка: Фигура с таким ID не найдена.")
            return
        dx = self.input_handler.get_int("Введите dx: ", -79, 79)
        dy = self.input_handler.get_int("Введите dy: ", -17, 17)
        command = CommandFactory.create_move_shape_command(self.canvas, shape, dx, dy)
        self.command_manager.execute(command)
        self.console_view.add_message(f"Фигура с ID {shape_id} успешно перемещена на dx={dx}, dy={dy}.")

    def _set_background(self):
        if not self.canvas.list_shapes():
            self.console_view.add_message("Ошибка: Нет фигур для установки заливки.")
            return
        shape_id = self.input_handler.get_int("Введите ID фигуры для установки заливки: ", 1, self.canvas._next_id - 1)
        shape = self.canvas.get_shape_by_id(shape_id)
        if shape is None:
            self.console_view.add_message("Ошибка: Фигура с таким ID не найдена.")
            return
        if not hasattr(shape, 'set_background'):
            self.console_view.add_message("Ошибка: Только круги и прямоугольники поддерживают заливку.")
            return
        fill_char = self.input_handler.get_char("Введите символ заливки: ", allow_empty=False)
        command = CommandFactory.create_set_background_command(self.canvas, shape, fill_char)
        self.command_manager.execute(command)
        self.console_view.add_message(f"Заливка для фигуры с ID {shape_id} установлена на '{fill_char}'.")

    def _set_shape_char(self):
        if not self.canvas.list_shapes():
            self.console_view.add_message("Ошибка: Нет фигур для установки символа.")
            return
        shape_id = self.input_handler.get_int("Введите ID фигуры для установки символа: ", 1, self.canvas._next_id - 1)
        shape = self.canvas.get_shape_by_id(shape_id)
        if shape is None:
            self.console_view.add_message("Ошибка: Фигура с таким ID не найдена.")
            return
        new_char = self.input_handler.get_char("Введите новый символ: ", allow_empty=False)
        command = CommandFactory.create_set_char_command(self.canvas, shape, new_char)
        self.command_manager.execute(command)
        self.console_view.add_message(f"Символ для фигуры с ID {shape_id} установлен на '{new_char}'.")

    def _save(self):
        filename = self.input_handler.get_filename("Введите имя файла для сохранения: ")
        self.file_manager.save(filename)
        self.console_view.add_message(f"Холст успешно сохранен в {filename}.json.")

    def _load(self):
        filename = self.input_handler.get_filename("Введите имя файла для загрузки: ")
        try:
            self.file_manager.load(filename)
            self.canvas.render()
            self.console_view.add_message(f"Холст успешно загружен из {filename}.json.")
        except (FileNotFoundError, ValueError) as e:
            self.console_view.add_message(str(e))

    def _undo(self):
        if self.command_manager.undo():
            self.console_view.add_message("Отмена выполнена успешно.")
        else:
            self.console_view.add_message("Нечего отменять.")

    def _redo(self):
        if self.command_manager.redo():
            self.console_view.add_message("Повтор выполнен успешно.")
        else:
            self.console_view.add_message("Нечего повторять.")

if __name__ == "__main__":
    app = PaintApp()
    app.run()