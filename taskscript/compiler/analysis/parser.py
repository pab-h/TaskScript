from taskscript.compiler.analysis.token import *
from taskscript.compiler.analysis.ast import *

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
            self.index += 1
            return

        raise ParserError(f"token of type { tokenType.name }  is expected")

    def number(self) -> NumberNode:
        numberNode = NumberNode(self.currentToken())
        self.eat(TokenTypes.NUMBER)

        return numberNode

    def int(self) -> IntNode:
        self.eat(TokenTypes.INT)
        self.eat(TokenTypes.OPENBRACKET)

        minNumber = self.number()

        self.eat(TokenTypes.COMMA)

        maxNumber = self.number()

        self.eat(TokenTypes.CLOSEBRACKET)

        return IntNode(
            min = minNumber,
            max = maxNumber
        )

    def float(self) -> FloatNode:
        self.eat(TokenTypes.FLOAT)
        self.eat(TokenTypes.OPENBRACKET)

        minNumber = self.number()

        self.eat(TokenTypes.COMMA)

        maxNumber = self.number()

        self.eat(TokenTypes.CLOSEBRACKET)

        return FloatNode(
            min = minNumber,
            max = maxNumber
        )

    def choice(self) -> ChoiceNode:
        choiceNode = ChoiceNode()

        self.eat(TokenTypes.CHOICE)
        self.eat(TokenTypes.OPENBRACKET)
        
        value = self.value()
        choiceNode.choices.append(value)

        while self.currentToken().type == TokenTypes.COMMA:
            self.eat(TokenTypes.COMMA)
            value = self.value()
            choiceNode.choices.append(value)

        self.eat(TokenTypes.CLOSEBRACKET)

        return choiceNode

    def call(self) -> CallNode:
        self.eat(TokenTypes.CALL)

        argument = self.currentToken()

        self.eat(TokenTypes.ARGUMENT)

        return CallNode(argument)

    def value(self) -> ValueNode:
        if self.currentToken().type == TokenTypes.NUMBER:
            return self.number()

        if self.currentToken().type == TokenTypes.ARGUMENT:
            argument = ArgumentNode(self.currentToken())
            self.eat(TokenTypes.ARGUMENT)

            return argument

        if self.currentToken().type == TokenTypes.INT:
            return self.int()
        
        if self.currentToken().type == TokenTypes.FLOAT:
            return self.float()
        
        if self.currentToken().type == TokenTypes.CHOICE:
            return self.choice()
        
        if self.currentToken().type == TokenTypes.CALL:
            return self.call()

    def declaration(self) -> VariableNode:
        identifier = self.currentToken()
        variable = VariableNode(identifier)
        
        self.eat(TokenTypes.IDENTIFIER)
        self.eat(TokenTypes.ASSIGN)

        variable.value = self.value()

        self.eat(TokenTypes.BREAKLINE)

        return variable

    def vars(self) -> VarsNode:
        vars = VarsNode()

        self.eat(TokenTypes.VARS)
        self.eat(TokenTypes.COLON)
        self.eat(TokenTypes.BREAKLINE)

        declaration = self.declaration() 
        vars.variables.append(declaration)

        while self.currentToken().type == TokenTypes.IDENTIFIER:
            declaration = self.declaration()
            vars.variables.append(declaration)

        return vars

    def task(self) -> TaskNode:
        self.eat(TokenTypes.TASK)
        self.eat(TokenTypes.COLON)

        if self.currentToken().type == TokenTypes.FROM:
            self.eat(TokenTypes.FROM)
    
            argument = self.currentToken()
            self.eat(TokenTypes.ARGUMENT)

            fromNode = FromNode(argument) 
            self.eat(TokenTypes.BREAKLINE)

            return TaskNode(fromNode)

        argument = self.currentToken()
        self.eat(TokenTypes.ARGUMENT)

        argumentNode = ArgumentNode(argument)

        self.eat(TokenTypes.BREAKLINE)

        return TaskNode(argumentNode)

    def checker(self) -> CheckerNode:
        self.eat(TokenTypes.CHECKER)
        self.eat(TokenTypes.COLON)
        argument = self.currentToken()
        self.eat(TokenTypes.ARGUMENT)

        return CheckerNode(argument)

    def program(self) -> ProgramNode:
        program = ProgramNode()

        program.vars = self.vars()
        program.task = self.task()
        program.checker = self.checker()

        return program

    def parse(self, text: str) -> AST:
        self.index = 0
        self.tokens = self.lexer.tokenize(text)
        
        return self.program()
