from taskscript.compiler.compiler import Compiler
from taskscript.teacher.teacher import Teacher

def main() -> None:
    compiler = Compiler()    
    teacher = Teacher()    

    i = 0

    print("TaskScript IDLE\n")

    while True:
        try: 
            text = input(f"In[{ i }] > ")
            
            if text == "exit":
                raise EOFError()

            commands = text.split(" ")

            action = commands[0]
            file = commands[1]
            response = ""


            output = ""


            if len(commands) == 3:
                response = commands[2]

            if action == "compile":
                output = compiler.compile(file)

            if action == "correct":
                output = teacher.correct(response, file)
            
            print(f"Out[{ i }] > { output }\n")
            i += 1

        except EOFError:
            print("\nBye, bye!\n")
            break

if __name__ == "__main__":
    main()
