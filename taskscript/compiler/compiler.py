import random 
import subprocess

from uuid import uuid4 as uuid

from pathlib import Path

from pdflatex import PDFLaTeX

from typing import Union
from typing import Optional

from taskscript.compiler.analysis.parser import Parser
from taskscript.compiler.analysis.ast import *

class Compiler(object):
    def __init__(self) -> None:
        self.parser = Parser()
        self.variables = {}
        self.pdfContent = ""
        self.templateFile: Optional[str] = None

    def visitProgram(self, node: ProgramNode) -> None:
        self.visit(node.vars)
        self.visit(node.task)
        self.visit(node.checker)

    def visitVars(self, node: VarsNode) -> None:
        for variable in node.variables:
            self.visit(variable)

    def visitVariable(self, node: VariableNode) -> None:
        variableName = node.identifier.value 
        self.variables.update({
            variableName: self.visit(node.value)
        })

    def visitInt(self, node: IntNode) -> int:
        maxValue = int(self.visit(node.max))
        minValue = int(self.visit(node.min))

        return random.randint(
            minValue, 
            maxValue
        )
    
    def visitFloat(self, node: FloatNode) -> float:
        maxValue = self.visit(node.max)
        minValue = self.visit(node.min)

        return random.uniform(
            minValue,
            maxValue
        )
    
    def visitChoice(self, node: ChoiceNode):
        values = []

        for value in node.choices:
            values.append(self.visit(value))

        return random.choice(values)
    
    def visitNumber(self, node: NumberNode) -> float:
        return node.number.value
    
    def visitArgument(self, node: ArgumentNode) -> str:
        return node.argument.value
    
    def visitCall(self, node: CallNode) -> str:
        filename = node.argument.value 

        process = subprocess.Popen(
            args = ["python", filename],
            stdout = subprocess.PIPE
        )

        returned = process.stdout.read() 
        returned = returned.decode("utf-8")

        if returned[-1] == "\n":
            returned = returned[0:-1]

        process.kill()

        return returned

    def visitTask(self, node: TaskNode):
        inputText = self.visit(node.valueNode)
        outputText = self.replaceVariables(inputText)

        self.pdfContent = outputText

    def visitFrom(self, node: FromNode):
        filename = node.argument.value

        self.templateFile = Path(filename).stem

        with open(filename) as file:
            return file.read()
        
    def visitChecker(self, node: CheckerNode):
        pass

    def visit(self, node: AST) -> Union[None, str, int, float]:
        if node.type == ASTTypes.PROGRAM:
            return self.visitProgram(node)

        if node.type == ASTTypes.VARS:
            return self.visitVars(node)

        if node.type == ASTTypes.VARIABLE:
            return self.visitVariable(node)

        if node.type == ASTTypes.INT:
            return self.visitInt(node)

        if node.type == ASTTypes.FLOAT:
            return self.visitFloat(node)

        if node.type == ASTTypes.CHOICE:
            return self.visitChoice(node)

        if node.type == ASTTypes.NUMBER:
            return self.visitNumber(node)

        if node.type == ASTTypes.ARGUMENT:
            return self.visitArgument(node)

        if node.type == ASTTypes.CALL:
            return self.visitCall(node)

        if node.type == ASTTypes.TASK:
            return self.visitTask(node)

        if node.type == ASTTypes.FROM:
            return self.visitFrom(node)
        
        if node.type == ASTTypes.CHECKER:
            return self.visitChecker(node)

    def replaceVariables(self, text: str) -> str:
        for key, value in self.variables.items():
            text = text.replace(
                f"<<{key}>>", 
                str(value)
            )

        return text

    def createPdf(self) -> str:
        pdfContent = bytes(
            self.pdfContent, 
            encoding="utf-8"
        )

        if not self.templateFile:
            self.templateFile = uuid()

        pdfLatex = PDFLaTeX.from_binarystring(
            binstr = pdfContent, 
            jobname = self.templateFile
        )

        pdfLatex.create_pdf(
            keep_pdf_file = True
        )

        return self.templateFile + ".pdf"

    def compile(self, text: str) -> list[str]:
        ast = self.parser.parse(text)
        self.visit(ast)

        return [
            self.createPdf()
        ]
