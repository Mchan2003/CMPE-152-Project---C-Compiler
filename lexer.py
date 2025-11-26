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
    MAIN = auto()
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
    #delimiter
    SEMICOLON = auto()
    COMMA = auto()
    COLON = auto()
    LEFTPARAM = auto()
    RIGHTPARAM = auto()
    LEFTBRACE = auto()
    RIGHTBRACE = auto()
    LEFTBRKT = auto()
    RIGHTBRKT = auto()

class TokenClass(Enum):
    DELIMITER = auto()
    IDENTIFIER = auto()
    KEYWORD = auto()
    OPERATOR = auto()
    LITERAL = auto() 
    EOF = auto()

class Token:
    def __init__(self, token_type, token_class, lexeme):
        self.token_type = token_type
        self.token_class = token_class
        self.lexeme = lexeme
    
    def __str__(self):
        return f"Token({self.token_type}, '{self.lexeme}')"

class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.current = 0
        self.line = 1

    #scan_token
    def scan_tokens(self):
        while self.current < len(self.source):
            self.scan_token(self.source[self.current])
        self.add_token(TokenType.EOF, TokenClass.EOF, "")

    #scan_token
    def scan_token(self, lex):
        match lex :
            case ';' : self.add_token(TokenType.SEMICOLON, TokenClass.DELIMITER, lex)
            case ',' : self.add_token(TokenType.COMMA, TokenClass.DELIMITER, lex)
            case ':' : self.add_token(TokenType.COLON, TokenClass.DELIMITER, lex)
            case '(' : self.add_token(TokenType.LEFTPARAM, TokenClass.DELIMITER, lex)
            case ')' : self.add_token(TokenType.RIGHTPARAM, TokenClass.DELIMITER, lex)
            case '{' : self.add_token(TokenType.LEFTBRACE, TokenClass.DELIMITER, lex)
            case '}' : self.add_token(TokenType.RIGHTBRACE, TokenClass.DELIMITER, lex)
            case '[' : self.add_token(TokenType.LEFTBRKT, TokenClass.DELIMITER, lex)
            case ']' : self.add_token(TokenType.RIGHTBRKT, TokenClass.DELIMITER, lex)
            case '*' : self.add_token(TokenType.STAR, TokenClass.OPERATOR, lex)
            case '^' : self.add_token(TokenType.CARROT, TokenClass.OPERATOR, lex)
            case '?' : self.add_token(TokenType.QUESTION, TokenClass.OPERATOR, lex)
            case '&' : self.add_token(TokenType.AT, TokenClass.OPERATOR, lex)
            case '+' : 
                if(self.current + 1 < len(self.source) and self.source[self.current + 1] == '+'):
                    self.add_token(TokenType.PLUS_PLUS, TokenClass.OPERATOR, "++")
                    self.current += 1
                elif(self.current + 1 < len(self.source) and self.source[self.current + 1] == '='):
                    self.add_token(TokenType.PLUS_EQUAL, TokenClass.OPERATOR, "+=")
                    self.current += 1
                else:
                    self.add_token(TokenType.PLUS, TokenClass.OPERATOR, lex)
            case '-' : 
                if(self.current + 1 < len(self.source) and self.source[self.current + 1] == '-'):
                    self.add_token(TokenType.MINUS_MINUS, TokenClass.OPERATOR, "--")
                    self.current += 1
                else:
                    self.add_token(TokenType.MINUS, TokenClass.OPERATOR, lex)
            case '/' : 
                if(self.current + 1 < len(self.source) and self.source[self.current + 1] == '/'):
                    self.add_token(TokenType.SLASH_SLASH, TokenClass.OPERATOR, "//")
                    self.current += 1
                    while(self.current < len(self.source) and
                        self.source[self.current] != '\n'):        
                        self.current += 1
                else:
                    self.add_token(TokenType.SLASH, TokenClass.OPERATOR, lex)
            case '>' : 
                if(self.current + 1 < len(self.source) and self.source[self.current + 1] == '='):
                    self.add_token(TokenType.GREATER_EQUAL, TokenClass.OPERATOR, ">=")
                    self.current += 1
                elif(self.current + 1 < len(self.source) and self.source[self.current + 1] == '>'):
                    self.add_token(TokenType.SHIFT_RIGHT, TokenClass.OPERATOR, ">>")
                    self.current += 1
                else:
                    self.add_token(TokenType.GREATER, TokenClass.OPERATOR, lex)
            case '<' : 
                if(self.current + 1 < len(self.source) and self.source[self.current + 1] == '='):
                    self.add_token(TokenType.LESSER_EQUAL, TokenClass.OPERATOR, "<=")
                    self.current += 1
                elif(self.current + 1 < len(self.source) and self.source[self.current + 1] == '<'):
                    self.add_token(TokenType.SHIFT_LEFT, TokenClass.OPERATOR, "<<")
                    self.current += 1
                else:
                    self.add_token(TokenType.LESSER, TokenClass.OPERATOR, lex)
            case '=' : 
                if(self.current + 1 < len(self.source) and self.source[self.current + 1] == '='):
                    self.add_token(TokenType.EQUAL_EQUAL, TokenClass.OPERATOR, "==")
                    self.current += 1
                else:
                    self.add_token(TokenType.EQUAL, TokenClass.OPERATOR, lex)
            case ' ' : 
                self.current += 1
            case '\n' : 
                self.current += 1
                self.line += 1
            case _ :
                if(lex.isdigit()):
                    digit = []
                    digit.append(lex);
                    while (self.current + 1 < len(self.source) and 
                        self.source[self.current + 1].isdigit()):
                        self.current += 1
                        digit.append(self.source[self.current])
                    self.add_token(TokenType.NUMBER, TokenClass.LITERAL, int(''.join(digit)))
                elif(lex.isalpha()):
                    alpha = []
                    alpha.append(lex);
                    while (self.current + 1 < len(self.source) and 
                        self.source[self.current + 1].isalpha()):
                        self.current += 1
                        alpha.append(self.source[self.current])
                    alpha_keyword = self.handle_keyword(''.join(alpha))
                    alpha_class = TokenClass.IDENTIFIER if (alpha_keyword == TokenType.IDENTIFIER) else TokenClass.KEYWORD
                    self.add_token(alpha_keyword, alpha_class , ''.join(alpha))
                else:
                    sys.exit("Invalid Token: {}".format(lex));

    #add_token
    def add_token(self, token_type, token_class, lexeme):
        self.tokens.append(Token(token_type, token_class, lexeme))
        self.current += 1;

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
            case "main" : return TokenType.MAIN
            case _ : return TokenType.IDENTIFIER

    #print token
    def print_token(self):
        for token in self.tokens:
            print(token)

    #get tokens
    def get_tokens(self):
        return self.tokens
    
    #get line
    def get_line(self):
        return self.line