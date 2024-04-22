from taskscript.compiler.analysis.token import *

from typing import Optional

class Lexer(object):
    def __init__(self) -> None:
        self.index = 0
        self.text = ""
        self.textLen = 0

        self.keywords: dict[str, Token] = {
            "vars": Token(
                value = TokenTypes.VARS.name,
                type = TokenTypes.VARS
            ),
            "int": Token(
                value = TokenTypes.INT.name,
                type = TokenTypes.INT
            ),
            "float": Token(
                value = TokenTypes.ASSIGN.name,
                type = TokenTypes.ASSIGN
            ),
            "call": Token(
                value = TokenTypes.CALL.name,
                type = TokenTypes.CALL
            ),
            "task": Token(
                value = TokenTypes.TASK.name,
                type = TokenTypes.TASK
            ),
            "from": Token(
                value = TokenTypes.FROM.name,
                type = TokenTypes.FROM
            ),
            "checker": Token(
                value = TokenTypes.CHECKER.name,
                type = TokenTypes.CHECKER
            ),
            "choice": Token(
                value = TokenTypes.CHOICE.name,
                type = TokenTypes.CHOICE
            )
        }

    def hasNext(self) -> bool:
        return self.index < self.textLen

    def currentChar(self) -> str:
        return self.text[self.index]

    def peekChar(self) -> Optional[str]:
        if self.index + 1 >= self.textLen:
            return None
        return self.text[self.index  + 1]

    def assign(self) -> Token:
        assign = self.currentChar()
        self.index += 1

        assign += self.currentChar()
        self.index += 1

        return Token(
            value = assign,
            type = TokenTypes.ASSIGN
        )

    def identifier(self) -> Token:
        identifier = ""

        while self.hasNext() and self.currentChar().isalpha():
            identifier = identifier + self.currentChar()
            self.index += 1

        token = Token(
            value = identifier,
            type = TokenTypes.IDENTIFIER
        )

        return self.keywords.get(identifier, token)

    def number(self) -> Token:
        number = ""

        while self.hasNext() and self.currentChar().isdigit():
            number += self.currentChar()
            self.index += 1

            if self.hasNext() and self.currentChar() == ".":
                number += self.currentChar()
                self.index += 1

        return Token(
            value = float(number),
            type = TokenTypes.NUMBER
        )

    def argument(self) -> Token:
        argument = ""
        self.index += 1

        while self.hasNext() and self.currentChar() != "\"":
            argument += self.currentChar()
            self.index += 1

        return Token(
            value = argument,
            type = TokenTypes.ARGUMENT
        )

    def nextToken(self) -> Token:
        if self.currentChar() == "\"":
            return self.argument()

        if self.currentChar() == ",":
            token = Token(
                value = self.currentChar(),
                type = TokenTypes.COMMA
            )

            self.index += 1

            return token

        if self.currentChar().isdigit():
            return self.number()

        if self.currentChar() == "-":
            token = Token(
                value = self.currentChar(),
                type = TokenTypes.MINUS
            )

            self.index += 1

            return token

        if self.currentChar() == "[":
            token = Token(
                value = self.currentChar(),
                type = TokenTypes.OPENBRACKET
            )

            self.index += 1

            return token
        
        if self.currentChar() == "]":
            token = Token(
                value = self.currentChar(),
                type = TokenTypes.CLOSEBRACKET
            )

            self.index += 1

            return token

        if self.currentChar() == " ":
            token = Token(
                value = self.currentChar(),
                type = TokenTypes.WHITESPACE
            )

            self.index += 1

            return token
            
        if self.currentChar() == "\n":
            token = Token(
                value = r"\n",
                type = TokenTypes.BREAKLINE
            )

            self.index += 1

            return token

        if self.currentChar() == ":":
            if self.peekChar() and self.peekChar() == "=":
                return self.assign()
            
            token = Token(
                value = self.currentChar(),
                type = TokenTypes.COLON
            )

            self.index += 1

            return token

        if self.currentChar().isalpha():
            return self.identifier()

        raise TokenError(f"unrecognized token [{ self.index }]({ self.currentChar() })")

    def tokenize(self, text: str) -> list[Token]:
        self.index = 0
        self.text = text
        self.textLen = len(text)

        tokens = []

        while self.hasNext():
            token = self.nextToken()

            if token.type != TokenTypes.WHITESPACE:
                tokens.append(token)

        eof = Token(
            value = None,
            type = TokenTypes.EOF
        )

        tokens.append(eof)

        return tokens
    