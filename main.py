from lexer import Lexer
from parser import Parser
import sys

def main():
    command = "";
    while(command != "exit"):
        command = input(">")
        if(command == "exit"):
            sys.exit(0);
        # lex = Lexer(command);
        # lex.scan_tokens();
        # lex.print_token();

        ast = Parser(command)
        ast.parse()
        ast.print_ast()
        ast.generate()
        ast.dump_tac()
        ast.to_assembly()


if __name__=="__main__":
    main()