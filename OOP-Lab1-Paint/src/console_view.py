class ConsoleView:
    def __init__(self):
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)
        if len(self.messages) > 5:
            self.messages.pop(0)

    def display_messages(self):
        print("\nСообщения:")
        if not self.messages:
            print("Нет сообщений.")
        else:
            for msg in self.messages:
                print(msg)

    def display_menu(self):
        print("\nМеню:")
        print("1. Нарисовать круг")
        print("2. Нарисовать линию")
        print("3. Нарисовать прямоугольник")
        print("4. Удалить фигуру")
        print("5. Переместить фигуру")
        print("6. Установить заливку")
        print("7. Установить символ фигуры")
        print("8. Сохранить")
        print("9. Загрузить")
        print("10. Отменить")
        print("11. Повторить")
        print("0. Выход")

    def display_shapes(self, shapes):
        print("\nФигуры:")
        if not shapes:
            print("На холсте нет фигур.")
        for s in shapes:
            print(s)

    def display_canvas(self, canvas):
        canvas.print_grid()