# commands/manager.py
from .base import Command

class CommandManager:
    def __init__(self, canvas):
        self.canvas = canvas
        self._undo = []
        self._redo = []

    def execute(self, cmd: Command) -> None:
        """Выполнить команду и записать её в стек undo."""
        cmd.execute()
        self._undo.append(cmd)
        self._redo.clear()

    def undo(self) -> bool:
        """
        Отменить последнюю выполненную команду.
        Возвращает True, если была отмена, False — если стек пуст.
        """
        if not self._undo:
            return False
        cmd = self._undo.pop()
        cmd.undo()
        self._redo.append(cmd)
        return True

    def redo(self) -> bool:
        """
        Повторить последнюю отменённую команду.
        Возвращает True, если была повтор, False — если стек пуст.
        """
        if not self._redo:
            return False
        cmd = self._redo.pop()
        cmd.execute()
        self._undo.append(cmd)
        return True
