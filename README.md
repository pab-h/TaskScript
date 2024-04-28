# TaskScript

Uma maneira fácil de criar tarefas para casa 

# How install

Para usar corretamente, é necessário utilizar o [poetry](https://python-poetry.org/)

1. Clone o repositório:
`git clone https://github.com/pab-h/TaskScript.git`
1. Na pasta do projeto, 
`poetry run start`

# The sintaxe

```js
program: vars task checker
vars: 'vars' ':' '\n' declaration (declaration)* 
declaration: identifier assign value '\n'
identifier: "qualquer sequência de letras"
assign: ":="
value: number | argument | int | float | choice | call 
number: "número de ponto flutuante"
argument: \" identifier \"
int: 'int' '[' number ',' number ']'
float: 'float' '[' number ',' number ']'
choice: 'choice' '[' value (',' value)* ']'
call: 'call' argument
task: 'task' ':' (argument | 'from' argument) '\n'
checker: 'checker' ':' argument
```

# The .task files

Os arquivos do TaskScript são os .task. Esse arquivo em que você fará as principais configurações sobre seu modelo. Veja alguns exemplos: 

```go
vars:
    a := int[100, 200]
    b := int[300, 400]
task: from "homework.tex"
checker: "calculator.py"
```

```go
vars:
    aluno := choice["Pablo", "John", "Marchel"]
    banana := int[300, 400]
task: from "homework.tex"
checker: "banana.py"
```

```go
vars:
    aluno := call "alunos.py"
    banana := int[300, 400]
task: from "homework.tex"
checker: "banana.py"
```

# Freatures

* `int[a, b]`: retorna um inteiro entre `a` e `b`
* `float[a, b]`: retona um ponto flutuante entre `a` e `b`
* `choice[.., .., ..]`: retorna um elemento dentre as escolhas
* `call "arquivo.py"`: executa e retorna a saída do arquivo "arquivo.py"
* `from "arquivo.text"`: retorna o conteúdo do arquivo "arquivo.text" 

# How compile and correct a task

Para compilar, basta executar
```bash
compile <tarefa>.task

```

Para corrigir uma tarefa, basta executar
```bash 
correct <tarefa>.ctask <resposta dada>
```

O comando `compile` compila o arquivo **.task**  retonando o arquivo do campos `task` compilado em **.pdf**. Além disso, retorna um arquivo `.ctask` usado para correção da tarefa.

O camando `correct` corrige a tarefa compilada. Para isso é necessário passar o arquivo `.ctask` e a resposta dada retornando *True* ou *False*

Exemplo: 

```bash
compile calculo.task
correct calculo.ctask -123
```

# Disclaimer

Esse projeto é somente uma prova de conceito. Certamente, não está em sua melhor forma. Caso queira, sinta-se a vontade para expandir a ideia.