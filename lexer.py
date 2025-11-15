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

class ProdRule(Enum):
    EXPRESSION = auto()
    ARITHMETIC = auto()
    GROUP = auto()
    OPERATOR = auto()
    LITERAL = auto() 
    EOF = auto()

class Token:
    def __init__(self, token_type, prod_rule, lexeme):
        self.token_type = token_type
        self.prod_rule = prod_rule
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
        self.add_token(TokenType.EOF, ProdRule.EOF, "")

    #scan_token
    def scan_token(self, lex):
        match lex :
            case ';' : self.add_token(TokenType.SEMICOLON, ProdRule.OPERATOR, lex)
            case ',' : self.add_token(TokenType.COMMA, ProdRule.OPERATOR, lex)
            case ':' : self.add_token(TokenType.COLON, ProdRule.OPERATOR, lex)
            case '(' : self.add_token(TokenType.LEFTPARAM, ProdRule.OPERATOR, lex)
            case ')' : self.add_token(TokenType.RIGHTPARAM, ProdRule.OPERATOR, lex)
            case '{' : self.add_token(TokenType.LEFTBRACE, ProdRule.OPERATOR, lex)
            case '}' : self.add_token(TokenType.RIGHTBRACE, ProdRule.OPERATOR, lex)
            case '[' : self.add_token(TokenType.LEFTBRKT, ProdRule.OPERATOR, lex)
            case ']' : self.add_token(TokenType.RIGHTBRKT, ProdRule.OPERATOR, lex)
            case '*' : self.add_token(TokenType.STAR, ProdRule.OPERATOR, lex)
            case '^' : self.add_token(TokenType.CARROT, ProdRule.OPERATOR, lex)
            case '?' : self.add_token(TokenType.QUESTION, ProdRule.OPERATOR, lex)
            case '&' : self.add_token(TokenType.AT, ProdRule.OPERATOR, lex)
            case '+' : 
                if(self.current + 1 < len(self.source) and self.source[self.current + 1] == '+'):
                    self.add_token(TokenType.PLUS_PLUS, ProdRule.OPERATOR, "++")
                    self.current += 1
                elif(self.current + 1 < len(self.source) and self.source[self.current + 1] == '='):
                    self.add_token(TokenType.PLUS_EQUAL, ProdRule.OPERATOR, "+=")
                    self.current += 1
                else:
                    self.add_token(TokenType.PLUS, ProdRule.OPERATOR, lex)
            case '-' : 
                if(self.current + 1 < len(self.source) and self.source[self.current + 1] == '-'):
                    self.add_token(TokenType.MINUS_MINUS, ProdRule.OPERATOR, "--")
                    self.current += 1
                else:
                    self.add_token(TokenType.MINUS, ProdRule.OPERATOR, lex)
            case '/' : 
                if(self.current + 1 < len(self.source) and self.source[self.current + 1] == '/'):
                    self.add_token(TokenType.SLASH_SLASH, ProdRule.OPERATOR, "//")
                    self.current += 1
                    while(self.current < len(self.source) and
                        self.source[self.current] != '\n'):        
                        self.current += 1
                else:
                    self.add_token(TokenType.SLASH, ProdRule.OPERATOR, lex)
            case '>' : 
                if(self.current + 1 < len(self.source) and self.source[self.current + 1] == '='):
                    self.add_token(TokenType.GREATER_EQUAL, ProdRule.OPERATOR, ">=")
                    self.current += 1
                elif(self.current + 1 < len(self.source) and self.source[self.current + 1] == '>'):
                    self.add_token(TokenType.SHIFT_RIGHT, ProdRule.OPERATOR, ">>")
                    self.current += 1
                else:
                    self.add_token(TokenType.GREATER, ProdRule.OPERATOR, lex)
            case '<' : 
                if(self.current + 1 < len(self.source) and self.source[self.current + 1] == '='):
                    self.add_token(TokenType.LESSER_EQUAL, ProdRule.OPERATOR, "<=")
                    self.current += 1
                elif(self.current + 1 < len(self.source) and self.source[self.current + 1] == '<'):
                    self.add_token(TokenType.SHIFT_LEFT, ProdRule.OPERATOR, "<<")
                    self.current += 1
                else:
                    self.add_token(TokenType.LESSER, ProdRule.OPERATOR, lex)
            case '=' : 
                if(self.current + 1 < len(self.source) and self.source[self.current + 1] == '='):
                    self.add_token(TokenType.EQUAL_EQUAL, ProdRule.OPERATOR, "==")
                    self.current += 1
                else:
                    self.add_token(TokenType.EQUAL, ProdRule.OPERATOR, lex)
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
                    self.add_token(TokenType.NUMBER, ProdRule.LITERAL, int(''.join(digit)))
                elif(lex.isalpha()):
                    alpha = []
                    alpha.append(lex);
                    while (self.current + 1 < len(self.source) and 
                        self.source[self.current + 1].isalpha()):
                        self.current += 1
                        alpha.append(self.source[self.current])
                    self.add_token(self.handle_keyword(''.join(alpha)), ProdRule.LITERAL, ''.join(alpha))
                else:
                    sys.exit("Invalid Token: {}".format(lex));

    #add_token
    def add_token(self, token_type, prod_rule, lexeme):
        self.tokens.append(Token(token_type, prod_rule, lexeme))
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