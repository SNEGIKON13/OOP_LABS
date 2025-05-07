import pytest


class DummyView:
    def __init__(self):
        self.messages = []

    def add_message(self, m):
        self.messages.append(m)


def test_get_int_valid_then_invalid(monkeypatch):
    prompts = iter(["foo", "5", "20", "3"])
    monkeypatch.setattr('builtins.input', lambda _: next(prompts))

    view = DummyView()
    from controller.input_handler import InputHandler
    ih = InputHandler(view)

    # first: non-int → message
    val = ih.get_int(">", 1, 10)
    assert val == 5
    assert "Нужно целое число." in view.messages

    view.messages.clear()
    # next: 20 out of bounds
    val = ih.get_int(">", 1, 10)
    assert val == 3
    assert "Должно быть от 1 до 10." in view.messages


def test_get_char(monkeypatch):
    prompts = iter(["ab", "", "z"])
    monkeypatch.setattr('builtins.input', lambda _: next(prompts))

    view = DummyView()
    from controller.input_handler import InputHandler
    ih = InputHandler(view)

    ch = ih.get_char(">", allow_empty=False)
    assert ch == 'z'
    assert "Введите ровно один символ." in view.messages


def test_get_char_allow_empty(monkeypatch):
    prompts = iter(["",])
    monkeypatch.setattr('builtins.input', lambda _: next(prompts))

    view = DummyView()
    from controller.input_handler import InputHandler
    ih = InputHandler(view)

    ch = ih.get_char(">", allow_empty=True)
    assert ch is None


def test_get_filename(monkeypatch):
    prompts = iter(["bad name!", "File123"])
    monkeypatch.setattr('builtins.input', lambda _: next(prompts))

    view = DummyView()
    from controller.input_handler import InputHandler
    ih = InputHandler(view)

    fn = ih.get_filename(">")
    assert fn == "File123"
    assert "Имя: только буквы и цифры." in view.messages
