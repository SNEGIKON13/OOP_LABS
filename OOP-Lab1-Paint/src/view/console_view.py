# view/console_view.py

class ConsoleView:
    def __init__(self, canvas):
        self.canvas = canvas
        self.messages = []

    def add_message(self, message: str) -> None:
        self.messages.append(message)
        if len(self.messages) > 5:
            self.messages.pop(0)

    def display_canvas(self) -> None:
        grid = self.canvas.render_data()   # список строк длины width

        width  = self.canvas.width
        height = self.canvas.height

        # 1) Верхняя ось X (0–width-1) через каждые 10 и последний индекс
        prefix = "   "  # отступ под номера строк
        header = [' ']*width
        # цифры 0,10,20,...,70
        for x in range(0, width, 10):
            s = str(x)
            for idx, ch in enumerate(s):
                if x + idx < width:
                    header[x + idx] = ch
        # добавляем конец шкалы: '79' для width=80
        end_label = str(width - 1)
        start = width - len(end_label)
        for idx, ch in enumerate(end_label):
            header[start + idx] = ch

        print(prefix + ''.join(header))

        # 2) Само поле: каждая строка с номером Y
        for y, line in enumerate(grid):
            print(f"{y:2d} {line}")

        # 3) Размер холста
        print(f"\nРазмер холста: {width}x{height}")

    def display_shapes(self) -> None:
        print("\nФигуры:")
        shapes = self.canvas.shapes
        if not shapes:
            print("  На холсте нет фигур.")
        else:
            for s in shapes:
                print(f"  {s.id}: {s}")

    def display_messages(self) -> None:
        print("\nСообщения:")
        if not self.messages:
            print("  Нет сообщений.")
        else:
            for msg in self.messages:
                print(" ", msg)

    @staticmethod
    def display_menu() -> None:
        print("\nМеню:")
        print(" 1. Нарисовать круг")
        print(" 2. Нарисовать линию")
        print(" 3. Нарисовать прямоугольник")
        print(" 4. Удалить фигуру")
        print(" 5. Переместить фигуру")
        print(" 6. Установить заливку")
        print(" 7. Установить символ фигуры")
        print(" 8. Сохранить")
        print(" 9. Загрузить")
        print("10. Отменить")
        print("11. Повторить")
        print(" 0. Выход")
