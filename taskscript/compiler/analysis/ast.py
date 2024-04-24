from enum import Enum
from enum import auto

from taskscript.compiler.analysis.token import Token

class ASTTypes(Enum):
    ABSTRACT = auto()
    PROGRAM = auto()
    VARS = auto()
    VARIABLE = auto()
    VALUE = auto()
    TASK = auto()
    CHECKER = auto()
    ARGUMENT = auto()
    FROM = auto()
    INT = auto()
    FLOAT = auto()
    CHOICE = auto()
    NUMBER = auto()
    CALL = auto()

class AST(object):
    def __init__(self, type = ASTTypes.ABSTRACT) -> None:
        self.type = type

class ValueNode(AST):
    def __init__(self, type = ASTTypes.VALUE) -> None:
        super().__init__(type)

class CallNode(ValueNode):
    def __init__(self, argument: Token) -> None:
        super().__init__(ASTTypes.CALL)

        self.argument = argument

class NumberNode(ValueNode):
    def __init__(self, number: Token) -> None:
        super().__init__(ASTTypes.NUMBER)

        self.number = number

class ChoiceNode(ValueNode):
    def __init__(self) -> None:
        super().__init__(ASTTypes.CHOICE)

        self.choices: list[ValueNode] = []

class FloatNode(ValueNode):
    def __init__(self, min: NumberNode, max: NumberNode) -> None:
        super().__init__(ASTTypes.FLOAT)

        self.min = min
        self.max = max

class IntNode(ValueNode):
    def __init__(self, min: NumberNode, max: NumberNode) -> None:
        super().__init__(ASTTypes.INT)

        self.min = min
        self.max = max

class ArgumentNode(ValueNode):
    def __init__(self, argument: Token) -> None:
        super().__init__(ASTTypes.ARGUMENT)

        self.argument = argument

class FromNode(ValueNode):
    def __init__(self, argument: Token) -> None:
        super().__init__(ASTTypes.FROM)

        self.argument = argument

class CheckerNode(AST):
    def __init__(self, argument: ArgumentNode) -> None:
        super().__init__(ASTTypes.CHECKER)

        self.argument = argument

class TaskNode(AST):
    def __init__(self, valueNode: ArgumentNode | FromNode) -> None:
        super().__init__(ASTTypes.TASK)

        self.valueNode = valueNode

class VariableNode(AST):
    def __init__(self, identifier: Token) -> None:
        super().__init__(ASTTypes.VARIABLE)

        self.identifier = identifier
        self.value: ValueNode = None

class VarsNode(AST):
    def __init__(self) -> None:
        super().__init__(ASTTypes.VARS)

        self.variables: list[VariableNode] = []

class ProgramNode(AST):
    def __init__(self) -> None:
        super().__init__()

        self.type = ASTTypes.PROGRAM
        self.vars: VarsNode = None 
        self.task: TaskNode = None 
        self.checker: CheckerNode = None 
        