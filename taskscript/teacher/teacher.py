import subprocess

from taskscript.compiler.analysis.parser import Parser
from taskscript.compiler.analysis.ast import *

from typing import Union

class Teacher(object):
    def __init__(self) -> None:
        self.ctask = ""
        self.parser = Parser()
        self.variables = {}
        self.response = ""
        self.correctResponse = ""

    def visitProgram(self, node: ProgramNode) -> None:
        self.visit(node.vars)
        self.visit(node.checker)

    def visitVars(self, node: VarsNode) -> None:
        for variable in node.variables:
            self.visit(variable)

    def visitVariable(self, node: VariableNode) -> None:
        variableName = node.identifier.value 
        variableValue = self.visit(node.value)

        self.variables.update({
            variableName: variableValue
        })
    
    def visitNumber(self, node: NumberNode) -> float:
        return node.number.value
    
    def visitArgument(self, node: ArgumentNode) -> str:
        return node.argument.value

    def visitChecker(self, node: CheckerNode):
        checkerFilename = node.argument.value

        variables = [str(v) for v in self.variables.values()]
        variables = "|".join(variables)

        process = subprocess.Popen(
            args = ["python", checkerFilename, variables],
            stdout = subprocess.PIPE
        )

        returned = process.stdout.read() 
        returned = returned.decode("utf-8")
        returned = returned.replace("\n", "")

        process.kill()

        self.correctResponse = returned

    def visit(self, node: AST) -> Union[None, str, int, float]:
        if node.type == ASTTypes.PROGRAM:
            return self.visitProgram(node)

        if node.type == ASTTypes.VARS:
            return self.visitVars(node)

        if node.type == ASTTypes.VARIABLE:
            return self.visitVariable(node)

        if node.type == ASTTypes.NUMBER:
            return self.visitNumber(node)

        if node.type == ASTTypes.ARGUMENT:
            return self.visitArgument(node)

        if node.type == ASTTypes.CALL:
            return self.visitCall(node)

        if node.type == ASTTypes.CHECKER:
            return self.visitChecker(node)

    def build(self) -> None:
        ast = self.parser.parse(self.ctask)
        self.visit(ast)

    def correct(self, response: str, ctask: str) -> bool:
        with open(ctask) as file:
            self.ctask = file.read()

        self.response = response
        self.build()

        return self.response == self.correctResponse
