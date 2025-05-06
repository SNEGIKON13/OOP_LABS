import os
import time

from core.canvas import Canvas
from core.canvas_file_manager import CanvasFileManager
from view import ConsoleView
from controller.input_handler import InputHandler
from core.commands import (
    CommandManager,
    AddShapeCommand,
    RemoveShapeCommand,
    MoveShapeCommand,
    SetBackgroundCommand,
    SetCharCommand,
)
from shapes import Circle, Line, Rectangle


class PaintApp:
    def __init__(self):
        # Модель
        self.canvas = Canvas(width=80, height=18)
        self.file_manager = CanvasFileManager(self.canvas)

        # Представление
        self.console_view = ConsoleView(self.canvas)

        # Ввод
        self.input_handler = InputHandler(self.console_view)

        # Команды
        self.command_manager = CommandManager(self.canvas)

        # Диспетчер пунктов меню
        self._actions = {
            1: self._draw_circle,
            2: self._draw_line,
            3: self._draw_rectangle,
            4: self._erase_shape,
            5: self._move_shape,
            6: self._set_background,
            7: self._set_shape_char,
            8: self._save,
            9: self._load,
            10: self._undo,
            11: self._redo,
        }

    def run(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')

            # Рендер и вывод
            self.console_view.display_canvas()
            self.console_view.display_shapes()
            self.console_view.display_messages()
            self.console_view.display_menu()

            # Ввод
            choice = self.input_handler.get_int("Введите выбор: ", 0, 11)
            if choice == 0:
                break

            # Вызов действия
            action = self._actions.get(choice)
            if action:
                action()
            else:
                self.console_view.add_message("Некорректный выбор.")

            time.sleep(0.1)

    def _draw_circle(self):
        try:
            x = self.input_handler.get_int("x (0-79): ", 0, 79)
            y = self.input_handler.get_int("y (0-17): ", 0, 17)
            radius = self.input_handler.get_int("Радиус (1-9): ", 1, 9)
            char = self.input_handler.get_char("Символ (*): ", allow_empty=True) or '*'
            fill_char = self.input_handler.get_char("Заливка (опц.): ", allow_empty=True)
            shape = Circle(x, y, radius, char, fill_char)
            cmd = AddShapeCommand(self.canvas, shape)
            self.command_manager.execute(cmd)
            self.console_view.add_message("Круг добавлен.")
        except ValueError as e:
            self.console_view.add_message(f"Ошибка: {e}")

    def _draw_line(self):
        try:
            x1 = self.input_handler.get_int("x1 (0-79): ", 0, 79)
            y1 = self.input_handler.get_int("y1 (0-17): ", 0, 17)
            x2 = self.input_handler.get_int("x2 (0-79): ", 0, 79)
            y2 = self.input_handler.get_int("y2 (0-17): ", 0, 17)
            char = self.input_handler.get_char("Символ (-): ", allow_empty=True) or '-'
            shape = Line(x1, y1, x2, y2, char)
            cmd = AddShapeCommand(self.canvas, shape)
            self.command_manager.execute(cmd)
            self.console_view.add_message("Линия добавлена.")
        except ValueError as e:
            self.console_view.add_message(f"Ошибка: {e}")

    def _draw_rectangle(self):
        try:
            x1 = self.input_handler.get_int("x1 (0-79): ", 0, 79)
            y1 = self.input_handler.get_int("y1 (0-17): ", 0, 17)
            x2 = self.input_handler.get_int("x2 (0-79): ", 0, 79)
            y2 = self.input_handler.get_int("y2 (0-17): ", 0, 17)
            border_char = self.input_handler.get_char("Граница (*): ", allow_empty=True) or '*'
            fill_char = self.input_handler.get_char("Заливка (опц.): ", allow_empty=True)
            shape = Rectangle(x1, y1, x2, y2, border_char, fill_char)
            cmd = AddShapeCommand(self.canvas, shape)
            self.command_manager.execute(cmd)
            self.console_view.add_message("Прямоугольник добавлен.")
        except ValueError as e:
            self.console_view.add_message(f"Ошибка: {e}")

    def _get_shape_by_id(self, action: str):
        if not self.canvas.shapes:
            self.console_view.add_message(f"Нет фигур для {action}.")
            return None
        sid = self.input_handler.get_int(f"ID фигуры для {action}: ", 1, self.canvas.get_max_shape_id())
        shape = self.canvas.get_shape_by_id(sid)
        if shape is None:
            self.console_view.add_message("Фигура не найдена.")
            return None
        return shape, sid

    def _erase_shape(self):
        res = self._get_shape_by_id("удаления")
        if not res: return
        _, sid = res
        cmd = RemoveShapeCommand(self.canvas, sid)
        self.command_manager.execute(cmd)
        self.console_view.add_message(f"Фигура {sid} удалена.")

    def _move_shape(self):
        res = self._get_shape_by_id("перемещения")
        if not res: return
        shape, sid = res
        dx = self.input_handler.get_int("dx: ", -79, 79)
        dy = self.input_handler.get_int("dy: ", -17, 17)
        cmd = MoveShapeCommand(self.canvas, shape, dx, dy)
        self.command_manager.execute(cmd)
        self.console_view.add_message(f"Фигура {sid} смещена.")

    def _set_background(self):
        res = self._get_shape_by_id("заливки")
        if not res: return
        shape, sid = res
        if not hasattr(shape, 'fill_char'):
            self.console_view.add_message("Нет заливки.")
            return
        fc = self.input_handler.get_char("Новый символ заливки: ", allow_empty=False)
        cmd = SetBackgroundCommand(self.canvas, shape, fc)
        self.command_manager.execute(cmd)
        self.console_view.add_message(f"Заливка {sid} обновлена.")

    def _set_shape_char(self):
        res = self._get_shape_by_id("смены символа")
        if not res: return
        shape, sid = res
        nc = self.input_handler.get_char("Новый символ: ", allow_empty=False)
        cmd = SetCharCommand(self.canvas, shape, nc)
        self.command_manager.execute(cmd)
        self.console_view.add_message(f"Символ {sid} обновлён.")

    def _save(self):
        fn = self.input_handler.get_filename("Имя для сохранения: ")
        self.file_manager.save(fn)
        self.console_view.add_message(f"Сохранено: {fn}.json")

    def _load(self):
        fn = self.input_handler.get_filename("Имя для загрузки: ")
        try:
            self.file_manager.load(fn)
            self.console_view.add_message(f"Загружено: {fn}.json")
        except Exception as e:
            self.console_view.add_message(str(e))

    def _undo(self):
        if self.command_manager.undo():
            self.console_view.add_message("Отмена выполнена.")
        else:
            self.console_view.add_message("Нечего отменять.")

    def _redo(self):
        if self.command_manager.redo():
            self.console_view.add_message("Повтор выполнен.")
        else:
            self.console_view.add_message("Нечего повторять.")
