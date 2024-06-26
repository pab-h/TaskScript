from enum import Enum
from enum import auto

from typing import Union

class TokenError(Exception):
    pass

class TokenTypes(Enum):
    EOF = auto()
    VARS = auto()
    TASK = auto()
    CHECKER = auto()
    INT = auto()
    FLOAT = auto()
    CALL = auto()
    FROM = auto()
    IDENTIFIER = auto()
    ASSIGN = auto()
    BREAKLINE = auto()
    WHITESPACE = auto()
    COLON = auto()
    OPENBRACKET = auto()
    CLOSEBRACKET = auto()
    NUMBER = auto()
    COMMA = auto()
    ARGUMENT = auto()
    CHOICE = auto()

class Token(object):
    def __init__(self, value: Union[str, int, float], type: TokenTypes) -> None:
        self.value = value
        self.type = type

    def __repr__(self) -> str:
        return f"Token[{ self.value }, { self.type.name }]"
    