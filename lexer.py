from enum import Enum, auto
import sys

class TokenType(Enum):
    #keywords
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    BREAK = auto()
    CONTINUE = auto()
    INT = auto()
    FLOAT = auto()
    RETURN = auto()
    CHAR = auto()
    VOID = auto()
    #identifiers
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    EOF = auto()
    #operators
    PLUS = auto()
    PLUS_PLUS = auto()
    PLUS_EQUAL = auto()
    MINUS = auto()
    MINUS_MINUS = auto()
    SLASH = auto()
    SLASH_SLASH = auto()
    STAR = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESSER = auto()
    LESSER_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    SHIFT_LEFT = auto()
    SHIFT_RIGHT = auto()
    CARROT = auto()
    QUESTION = auto()
    AT = auto()
    #seperators
    SEMICOLON = auto()
    COMMA = auto()
    COLON = auto()
    LEFTPARAM = auto()
    RIGHTPARAM = auto()
    LEFTBRACE = auto()
    RIGHTBRACE = auto()
    LEFTBRKT = auto()
    RIGHTBRKT = auto()

class Token:
    def __init__(self, token_type, lexeme):
        self.token_type = token_type
        self.lexeme = lexeme
    
    def __str__(self):
        return f"Token({self.token_type}, '{self.lexeme}')"

class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.current = 0

    #scan_token
    def scan_tokens(self):
        while self.current < len(self.source):
            self.scan_token(self.source[self.current])
        self.add_token(TokenType.EOF, "")

    #scan_token
    def scan_token(self, lex):
        match lex :
            case ';' : self.handle_operator(TokenType.SEMICOLON, lex)
            case ',' : self.handle_operator(TokenType.COMMA, lex)
            case ':' : self.handle_operator(TokenType.COLON, lex)
            case '(' : self.handle_operator(TokenType.LEFTPARAM, lex)
            case ')' : self.handle_operator(TokenType.RIGHTPARAM, lex)
            case '{' : self.handle_operator(TokenType.LEFTBRACE, lex)
            case '}' : self.handle_operator(TokenType.RIGHTBRACE, lex)
            case '[' : self.handle_operator(TokenType.LEFTBRKT, lex)
            case ']' : self.handle_operator(TokenType.RIGHTBRKT, lex)
            case '*' : self.handle_operator(TokenType.STAR, lex)
            case '^' : self.handle_operator(TokenType.CARROT, lex)
            case '?' : self.handle_operator(TokenType.QUESTION, lex)
            case '&' : self.handle_operator(TokenType.AT, lex)
            case '+' : 
                if(self.current + 1 < len(self.source) and self.source[self.current + 1] == '+'):
                    self.handle_operator(TokenType.PLUS_PLUS, "++")
                    self.current += 1
                elif(self.current + 1 < len(self.source) and self.source[self.current + 1] == '='):
                    self.handle_operator(TokenType.PLUS_EQUAL, "+=")
                    self.current += 1
                else:
                    self.handle_operator(TokenType.PLUS, lex)
            case '-' : 
                if(self.current + 1 < len(self.source) and self.source[self.current + 1] == '-'):
                    self.handle_operator(TokenType.MINUS_MINUS, "--")
                    self.current += 1
                else:
                    self.handle_operator(TokenType.MINUS, lex)
            case '/' : 
                if(self.current + 1 < len(self.source) and self.source[self.current + 1] == '/'):
                    self.handle_operator(TokenType.SLASH_SLASH, "//")
                    self.current += 1
                    while(self.current < len(self.source) and
                        self.source[self.current] != '\n'):        
                        self.current += 1
                else:
                    self.handle_operator(TokenType.SLASH, lex)
            case '>' : 
                if(self.current + 1 < len(self.source) and self.source[self.current + 1] == '='):
                    self.handle_operator(TokenType.GREATER_EQUAL, ">=")
                    self.current += 1
                elif(self.current + 1 < len(self.source) and self.source[self.current + 1] == '>'):
                    self.handle_operator(TokenType.SHIFT_RIGHT, ">>")
                    self.current += 1
                else:
                    self.handle_operator(TokenType.GREATER, lex)
            case '<' : 
                if(self.current + 1 < len(self.source) and self.source[self.current + 1] == '='):
                    self.handle_operator(TokenType.LESSER_EQUAL, "<=")
                    self.current += 1
                elif(self.current + 1 < len(self.source) and self.source[self.current + 1] == '<'):
                    self.handle_operator(TokenType.SHIFT_LEFT, "<<")
                    self.current += 1
                else:
                    self.handle_operator(TokenType.LESSER, lex)
            case '=' : 
                if(self.current + 1 < len(self.source) and self.source[self.current + 1] == '='):
                    self.handle_operator(TokenType.EQUAL_EQUAL, "==")
                    self.current += 1
                else:
                    self.handle_operator(TokenType.EQUAL, lex)
            case ' ' : 
                self.current += 1
            case _ :
                if(lex.isdigit()):
                    digit = []
                    digit.append(lex);
                    while (self.current + 1 < len(self.source) and 
                        self.source[self.current + 1].isdigit()):
                        self.current += 1
                        digit.append(self.source[self.current])
                    self.handle_operator(TokenType.NUMBER, int(''.join(digit)))
                elif(lex.isalpha()):
                    alpha = []
                    alpha.append(lex);
                    while (self.current + 1 < len(self.source) and 
                        self.source[self.current + 1].isalpha()):
                        self.current += 1
                        alpha.append(self.source[self.current])
                    self.handle_operator(self.handle_keyword(''.join(alpha)), ''.join(alpha))
                else:
                    sys.exit("Invalid Token: {}".format(lex));

    #add_token
    def add_token(self, token_type, lexeme):
        self.tokens.append(Token(token_type, lexeme))
        self.current += 1;

    #handle operator
    def handle_operator(self, token_type, lexeme):
        self.add_token(token_type, lexeme)

    #handle identifier
    def handle_keyword(self, lex):
        match lex :
            case "if" : return TokenType.IF
            case "else" : return TokenType.ELSE
            case "while" : return TokenType.WHILE
            case "break" : return TokenType.BREAK
            case "continue" : return TokenType.CONTINUE
            case "int" : return TokenType.INT
            case "float" : return TokenType.FLOAT
            case "return" : return TokenType.RETURN
            case "char" : return TokenType.CHAR
            case "void" : return TokenType.VOID
            case _ : return TokenType.IDENTIFIER

    #print token
    def print_token(self):
        for token in self.tokens:
            print(token)