from taskscript.compiler.analysis.token import *
from taskscript.compiler.analysis.lexer import Lexer

class ParserError(Exception):
    pass

class Parser(object):
    def __init__(self) -> None:
        self.lexer = Lexer()
        self.index = 0
        self.tokens: list[Token] = []

    def currentToken(self) -> Token:
        return self.tokens[self.index]

    def eat(self, tokenType: TokenTypes) -> None:
        if self.currentToken().type == tokenType:
            print(tokenType)
            self.index += 1
            return

        raise ParserError(f"token of type { tokenType.name }  is expected")

    def number(self):
        if self.currentToken().type == TokenTypes.MINUS:
            self.eat(TokenTypes.MINUS)
        self.eat(TokenTypes.NUMBER)

    def int(self):
        self.eat(TokenTypes.INT)
        self.eat(TokenTypes.OPENBRACKET)
        self.number()
        self.eat(TokenTypes.COMMA)
        self.number()
        self.eat(TokenTypes.CLOSEBRACKET)

    def float(self):
        self.eat(TokenTypes.FLOAT)
        self.eat(TokenTypes.OPENBRACKET)
        self.number()
        self.eat(TokenTypes.COMMA)
        self.number()
        self.eat(TokenTypes.CLOSEBRACKET)

    def choice(self):
        self.eat(TokenTypes.CHOICE)
        self.eat(TokenTypes.OPENBRACKET)
        
        self.value()
        
        while self.currentToken().type == TokenTypes.COMMA:
            self.eat(TokenTypes.COMMA)
            self.value()

        self.eat(TokenTypes.CLOSEBRACKET)

    def call(self):
        self.eat(TokenTypes.CALL)
        self.eat(TokenTypes.ARGUMENT)

    def value(self):
        if self.currentToken().type == TokenTypes.MINUS:
            return self.number()
        
        if self.currentToken().type == TokenTypes.NUMBER:
            return self.number()

        if self.currentToken().type == TokenTypes.ARGUMENT:
            return self.eat(TokenTypes.ARGUMENT)

        if self.currentToken().type == TokenTypes.INT:
            return self.int()
        
        if self.currentToken().type == TokenTypes.FLOAT:
            return self.float()
        
        if self.currentToken().type == TokenTypes.CHOICE:
            return self.choice()
        
        if self.currentToken().type == TokenTypes.CALL:
            return self.call()

    def declaration(self):
        self.eat(TokenTypes.IDENTIFIER)
        self.eat(TokenTypes.ASSIGN)
        self.value()
        self.eat(TokenTypes.BREAKLINE)

    def vars(self):
        self.eat(TokenTypes.VARS)
        self.eat(TokenTypes.COLON)
        self.eat(TokenTypes.BREAKLINE)

        self.declaration()

        while self.currentToken().type == TokenTypes.IDENTIFIER:
            self.declaration()

    def task(self):
        self.eat(TokenTypes.TASK)
        self.eat(TokenTypes.COLON)

        if self.currentToken().type == TokenTypes.FROM:
            self.eat(TokenTypes.FROM)

        self.eat(TokenTypes.ARGUMENT)
        self.eat(TokenTypes.BREAKLINE)

    def checker(self):
        self.eat(TokenTypes.CHECKER)
        self.eat(TokenTypes.COLON)
        self.eat(TokenTypes.ARGUMENT)

    def program(self):
        self.vars()
        self.task()
        self.checker()

    def parse(self, text: str):
        self.index = 0
        self.tokens = self.lexer.tokenize(text)

        return self.program()
