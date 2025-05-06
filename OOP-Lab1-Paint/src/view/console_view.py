class ConsoleView:
    def __init__(self, canvas):
        self.canvas = canvas
        self.messages = []

    def add_message(self, message: str) -> None:
        self.messages.append(message)
        if len(self.messages) > 5:
            self.messages.pop(0)

    def display_canvas(self) -> None:
        for line in self.canvas.render_data():
            print(line)

    def display_shapes(self) -> None:
        print("\nФигуры:")
        shapes = self.canvas.shapes
        if not shapes:
            print("  (На холсте нет фигур)")
        else:
            for s in shapes:
                print(f"  {s.id}: {s}")

    def display_messages(self) -> None:
        print("\nСообщения:")
        if not self.messages:
            print("  (Нет сообщений)")
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
