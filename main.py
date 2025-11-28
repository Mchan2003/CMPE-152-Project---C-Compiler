from lexer import Lexer
from parser import Parser
import sys

def main():
    while True:
            command = []
            print("Enter code (Ctrl+Z when done):")
            
            try:
                while True:
                    line = input("> ")
                    command.append(line)
            except EOFError:
                pass
            
            code = "\n".join(command)
            
            if not code.strip():  # Exit if empty input
                print("Exiting...")
                break
            
            ast = Parser(code)
            ast.parse()
            print("===== AST =====")
            ast.print_ast()

            ast.generate()
            ast.dump_tac()

            ast.to_assembly()


if __name__=="__main__":
    main()