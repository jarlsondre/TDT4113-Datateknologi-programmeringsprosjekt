from enum import Enum, auto

class State(Enum):
    START = auto()
    INPUT_PASSWORD = auto()
    CHECK_PASSWORD = auto()
    INPUT_NEW_PASSWORD = auto()
    VALIDATE_NEW_PASSWORD = auto()
    MENY = auto()
    END = auto()

    