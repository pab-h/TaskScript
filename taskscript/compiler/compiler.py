import random 
import subprocess

from os import remove
from uuid import uuid4 as uuid
from pathlib import Path
from typing import Union
from tempfile import NamedTemporaryFile

from taskscript.compiler.analysis.parser import Parser
from taskscript.compiler.analysis.ast import *

class Compiler(object):
    def __init__(self) -> None:
        self.parser = Parser()
        self.variables = {}
        self.pdfContent = ""
        self.ctaskContent = ""
        self.templateFilename = f"{ uuid() }.tex"
        self.targetFilename = ""

    def visitProgram(self, node: ProgramNode) -> None:
        self.visit(node.vars)
        self.visit(node.task)
        self.visit(node.checker)

    def visitVars(self, node: VarsNode) -> None:
        self.ctaskContent += "vars:\n"

        for variable in node.variables:
            self.ctaskContent += self.visit(variable)

    def visitVariable(self, node: VariableNode) -> None:
        variableName = node.identifier.value 
        variableValue = self.visit(node.value)
        self.variables.update({
            variableName: variableValue
        })

        return f"   { variableName } := { variableValue }\n"

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
        self.ctaskContent += "task: "

        inputText = self.visit(node.valueNode)
      
        outputText = self.replaceVariables(inputText)
        self.pdfContent = outputText

        valueNode = node.valueNode
        if valueNode.type == ASTTypes.ARGUMENT:
            self.ctaskContent += f"\"{ inputText }\""

    def visitFrom(self, node: FromNode):
        filename = node.argument.value
        self.templateFilename = filename

        self.ctaskContent += f"from \"{ filename }\"\n"

        with open(filename) as file:
            return file.read()
        
    def visitChecker(self, node: CheckerNode):
        checkerFilename = node.argument.value
        self.ctaskContent += f"checker: \"{ checkerFilename }\""

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
        tmpLatexPath = ""

        with NamedTemporaryFile(mode = "w", delete = False) as file:
            file.write(self.pdfContent)

            tmpLatexPath = file.name

        jobname = Path(self.templateFilename).stem

        subprocess.run([
            'pdflatex',
            "-jobname",
            jobname,
            tmpLatexPath,
        ], stdout = subprocess.DEVNULL)

        remove(tmpLatexPath)
        remove(f"{ jobname }.log")
        remove(f"{ jobname }.aux")

        return jobname + ".pdf"


    def createCTask(self) -> str:
        cTaskFilename = Path(self.targetFilename).stem
        cTaskFilename += ".ctask"

        with open(cTaskFilename, "w+") as file:
            file.write(self.ctaskContent)

        return cTaskFilename

    def build(self, code: str) -> None:
        ast = self.parser.parse(code)
        self.visit(ast)

    def compile(self, filename: str) -> list[str]:
        with open(filename) as file:
            self.build(file.read())

        self.targetFilename = filename

        return [
            self.createPdf(),
            self.createCTask()
        ]
        