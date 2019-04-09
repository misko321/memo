import time
from enum import Enum, auto


class Mode(Enum):
    QUIZ = auto()
    EDIT = auto()
    EXPLAIN = auto()


class InvalidEntryException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ModeSwitchException(Exception):
    def __init__(self, mode: Mode, *args: object) -> None:
        super().__init__(*args)
        self.mode = mode


class Entry:
    def __init__(self, definition: str, explanation: str, mode: Mode) -> None:
        self.definition = definition
        self.explanation = explanation
        self.mode = mode
        self.last_review_timestamp = time.time()

    @property
    def explanation(self):
        return self.__explanation

    @explanation.setter
    def explanation(self, explanation):
        self.__explanation = explanation
