from lexer import Lexer
from parser import Parser
import sys

def main():
    command = "";
    while(command != "exit"):
        command = input(">")
        if(command == "exit"):
            sys.exit(0);
        lex = Lexer(command);
        lex.scan_tokens();
        lex.print_token();

        parse = Parser(lex.tokens)
        parse.syntax_analysis()
        parse.sematic_analysis()
        parse.code_generation()

if __name__=="__main__":
    main()