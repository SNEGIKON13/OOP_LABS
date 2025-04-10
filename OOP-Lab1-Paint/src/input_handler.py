class InputHandler:
    def __init__(self, console_view):
        self.console_view = console_view

    def get_int(self, prompt, min_val, max_val):
        while True:
            try:
                value = int(input(prompt))
                if min_val <= value <= max_val:
                    return value
                else:
                    self.console_view.add_message(f"Ошибка: Значение должно быть от {min_val} до {max_val}.")
            except ValueError:
                self.console_view.add_message("Ошибка: Введите целое число.")

    def get_char(self, prompt, allow_empty=False):
        while True:
            value = input(prompt).strip()
            if not value and allow_empty:
                return None
            if value and len(value) == 1:
                return value
            self.console_view.add_message("Ошибка: Введите один символ или оставьте пустым, если разрешено.")

    def get_filename(self, prompt):
        while True:
            filename = input(prompt).strip()
            if filename and filename.isalnum():
                return filename
            self.console_view.add_message("Ошибка: Имя файла должно быть непустым и содержать только буквы и цифры.")