class InputHandler:
    def __init__(self, view):
        self.view = view

    def get_int(self, prompt: str, lo: int, hi: int) -> int:
        while True:
            try:
                val = int(input(prompt))
                if lo <= val <= hi:
                    return val
                self.view.add_message(f"Должно быть от {lo} до {hi}.")
            except ValueError:
                self.view.add_message("Нужно целое число.")

    def get_char(self, prompt: str, allow_empty: bool = False) -> str | None:
        while True:
            txt = input(prompt).strip()
            if txt == "" and allow_empty:
                return None
            if len(txt) == 1:
                return txt
            self.view.add_message("Введите ровно один символ.")

    def get_filename(self, prompt: str) -> str:
        while True:
            fn = input(prompt).strip()
            if fn.isalnum():
                return fn
            self.view.add_message("Имя: только буквы и цифры.")
