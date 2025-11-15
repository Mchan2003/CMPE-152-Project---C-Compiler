from __future__ import annotations
from dataclasses import dataclass
from lexer import Token, TokenType, ProdRule, Lexer
from typing import Union, Optional
import sys

@dataclass
class Operator:
    operator: Token

    def __str__(self):
        return f"{self.operator}"

@dataclass
class Literal:
    literal: Token

    def __str__(self):
        return f"{self.literal}"
    

@dataclass
class Expression:
    left_exp: S 
    op: Operator
    right_exp: S
    
    def __str__(self):
        return self._format(0)
    
    def _format(self, level: int) -> str:
        indent = "\t" * level
        child_indent = "\t" * (level + 1)
        
        # Format left expression
        if isinstance(self.left_exp, Expression):
            left_str = f"{child_indent}LEFT EXPRESSION:\n{self.left_exp._format(level + 1)}"
        else:
            left_str = f"{child_indent}LEFT EXPRESSION: {self.left_exp}"
        
        # Format right expression
        if isinstance(self.right_exp, Expression):
            right_str = f"{child_indent}RIGHT EXPRESSION:\n{self.right_exp._format(level + 1)}"
        else:
            right_str = f"{child_indent}RIGHT EXPRESSION: {self.right_exp}"
        
        return (
            f"{indent}[\n"
            f"{left_str}\n"
            f"{child_indent}OPERATOR: {self.op}\n"
            f"{right_str}\n"
            f"{indent}]"
        )

S = Union[Literal, Expression] 

class Parser:
    def __init__(self, line):
        self.root: Optional[S] = None
        self.lex = Lexer(line);
        self.tokens = self.lex.get_tokens()
        self.current = -1;
    
    def parse(self):
        self.lex.scan_tokens()
        # self.lex.print_token()
        self.root = self.parse_exp(0.0)

        next_token = self.peek()
        if next_token.token_type != TokenType.EOF:
            sys.exit(f"Unexpected token on line {self.lex.get_line()}: {next_token.lexeme}")
        
    def parse_exp(self, min_bp):
        lhs = self.next();
        # print(f"lhs: {lhs} | current = {self.current}")
        if lhs.token_type == TokenType.LEFTPARAM:
            self.parse_exp(0.0)
            assert(self.next() == TokenType.RIGHTPARAM);
        if lhs.prod_rule != ProdRule.LITERAL:
            sys.exit(f"Invalid literal on line ({self.lex.get_line()}): {lhs.lexeme}")

        while True: 
            op = self.peek()
            if op.token_type == TokenType.EOF:
                break;
            if op.token_type == TokenType.RIGHTPARAM:
                break;
            if op.prod_rule != ProdRule.OPERATOR:
                sys.exit(f"Invalid operator on line ({self.lex.get_line()}): {lhs.lexeme}")
            left_bp, right_bp = self.binding_power(op);
            if left_bp < min_bp:
                break;
            op = self.next()
            # print(f"op: {op} | current = {self.current}")
            rhs = self.parse_exp(right_bp)
            # print(f"rhs: {rhs} | current = {self.current}")
            lhs = Expression(lhs, op, rhs)
        return lhs  
      
    def binding_power(self, token):
        match token.token_type:
            case TokenType.EQUAL:
                return (1.0, 1.1)
            case TokenType.PLUS | TokenType.MINUS:
                return (2.0, 2.1)
            case TokenType.STAR | TokenType.SLASH:
                return (3.0, 3.1)
            case _:
                sys.exit(f"Invalid token on line ({self.lex.get_line()}): {token.lexeme}")

    def next(self):
        self.current += 1
        if self.current >= len(self.tokens):
            sys.exit(f"Parser reach beyond the end of tokens on line: {self.lex.get_line()} at {self.tokens[self.current-1].lexeme}")
        return self.tokens[self.current]
    
    def peek(self):
        if self.current + 1 < len(self.tokens):
            return self.tokens[self.current + 1]
        return self.tokens[-1]
    
    def print_ast(self):
        print(self.root)
