from __future__ import annotations
from dataclasses import dataclass
from lexer import Token, TokenType, TokenClass, Lexer
from typing import Union, Optional
import sys

@dataclass
class TreeNode:
    operand1:str
    operator: str
    operand2: str

@dataclass
class LeafNode:
    operand:str

    def __str__(self):
        return f"{self.operand}"

@dataclass
class Operator:
    operator: Token

    def __str__(self):
        return f"{self.operator.lexeme}"

@dataclass
class Literal:
    token: Token

    def __str__(self):
        return f"{self.token.lexeme}"

@dataclass
class Expression:
    left_exp: E 
    op: Operator
    right_exp: E
    
    def __str__(self):
        return self._format(0)
    
    def _format(self, level: int) -> str:
        indent = "\t" * level
        child_indent = "\t" * (level + 1)
        
        if isinstance(self.left_exp, Expression):
            left_str = f"{child_indent}LEFT EXPRESSION:\n{self.left_exp._format(level + 1)}"
        else:
            left_str = f"{child_indent}LEFT EXPRESSION: {self.left_exp}"
        
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
    


@dataclass
class Declaration:
    d_type: Token
    exp: E

    def __str__(self):
        return self._format(0)
    
    def _format(self, level: int) -> str:
        indent = "\t" * level
        child_indent = "\t" * (level + 1)
        
        if isinstance(self.exp, Expression):
            exp_str = f"{child_indent}EXPRESSION:\n{self.exp._format(level + 1)}"
        else:
            exp_str = f"{child_indent}EXPRESSION: {self.exp}"
        
        return (
            f"{indent}DECLARATION:\n"
            f"{indent}[\n"
            f"{child_indent}TYPE: {self.d_type}\n"
            f"{exp_str}\n"
            f"{indent}]"
        )



E = Union[Literal, Expression] 
data_type = {TokenType.INT, TokenType.FLOAT, TokenType.CHAR, TokenType.VOID}

class Parser:
    def __init__(self, line):
        self.root: Optional[E] = None
        self.lex = Lexer(line)
        self.tokens = self.lex.get_tokens()
        self.current = -1
        self.temp_count = 0
        self.tac = []
        
    def parse(self):
        self.lex.scan_tokens()
        self.lex.print_token()
        self.root = self.parse_declare()

        next_token = self.peek()
        if next_token.token_type != TokenType.EOF:
            sys.exit(f"Unexpected token on line {self.lex.get_line()}: {next_token.lexeme}")

    def parse_declare(self) -> Declaration:
        d_type = self.next()

        if d_type.token_class != TokenClass.KEYWORD and d_type.token_type not in data_type:
            sys.exit(f"Invalid data type for declaration on line ({self.lex.get_line()}): {d_type.lexeme}")
        
        exp = self.parse_exp(0.0)
        
        dec = Declaration(d_type, exp)
        return dec
        
    def parse_exp(self, min_bp) -> Expression:
        lhs = self.next()
        
        if lhs.token_type == TokenType.LEFTPARAM:
            lhs = self.parse_exp(0.0)
            right_paren = self.next()
            if right_paren.token_type != TokenType.RIGHTPARAM:
                sys.exit(f"Expected ')' on line {self.lex.get_line()}")
        elif lhs.token_class != TokenClass.LITERAL and lhs.token_class != TokenClass.IDENTIFIER:
            sys.exit(f"Invalid literal on line ({self.lex.get_line()}): {lhs.lexeme}")
        else:
            lhs = Literal(lhs)

        while True: 
            op = self.peek()
            if op.token_type == TokenType.EOF:
                break
            if op.token_type == TokenType.RIGHTPARAM:
                break
            if op.token_class != TokenClass.OPERATOR:
                sys.exit(f"Invalid operator on line ({self.lex.get_line()}): {op.lexeme}")
            left_bp, right_bp = self.binding_power(op)
            if left_bp < min_bp:
                break
            op = self.next()
            op = Operator(op)
            rhs = self.parse_exp(right_bp)
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

    def new_temp(self) -> str:
        tmp = f"t{self.temp_count}"
        self.temp_count += 1
        return tmp

    def gen_tac(self, target: str, arg1: str, op: str, arg2: Optional[str]):
        self.tac.append((target, arg1, op, arg2))

    def eval_ir(self, node: E) -> str:
        if isinstance(node, Expression):
            left_place = self.eval_ir(node.left_exp)
            right_place = self.eval_ir(node.right_exp)
            op = node.op.operator.lexeme
            
            if node.op.operator.token_type == TokenType.EQUAL:
                if not isinstance(node.left_exp, Literal):
                    sys.exit("Left-hand side of assignment must be a variable")
                var_name = node.left_exp.token.lexeme
                self.gen_tac(var_name, right_place, "=", None)
                return var_name
            else:
                tmp = self.new_temp()
                self.gen_tac(tmp, left_place, op, right_place)
                return tmp
        elif isinstance(node, Literal):
            return str(node.token.lexeme)
        elif isinstance(node, Declaration):
            exp = self.eval_ir(node.exp)
            return exp
        else:
            raise RuntimeError("Unknown AST node type")

    def generate(self):
        if self.root is None:
            sys.exit("No AST to generate from")
        result_place = self.eval_ir(self.root)
        return result_place

    def dump_tac(self):
        print("=== Three-Address Code ===")
        for tgt, a1, op, a2 in self.tac:
            if a2 is None:
                print(f"{tgt} = {a1}")
            else:
                print(f"{tgt} = {a1} {op} {a2}")

    def to_assembly(self):
        print("\n=== Pseudo-Assembly ===")
        reg_map: dict[str,str] = {}
        next_reg_num = 1
        
        def reg_for(place: str) -> str:
            nonlocal next_reg_num
            if place not in reg_map:
                reg_map[place] = f"r{next_reg_num}"
                next_reg_num += 1
            return reg_map[place]
        
        def is_immediate(value: str) -> bool:
            """Check if value is a numeric literal"""
            try:
                int(value)
                return True
            except ValueError:
                return False

        for tgt, a1, op, a2 in self.tac:
            if a2 is None:
                if op == "=":
                    rdst = reg_for(tgt)
                    if is_immediate(a1):
                        print(f"mov {rdst}, #{a1}    # {tgt} = {a1}")
                    else:
                        rsrc = reg_for(a1)
                        print(f"mov {rdst}, {rsrc}    # {tgt} = {a1}")
                else:
                    rsrc = reg_for(a1)
                    rdst = reg_for(tgt)
                    print(f"{op} {rdst}, {rsrc}    # {tgt} = {op} {a1}")
            else:
                rdst = reg_for(tgt)
                if is_immediate(a1):
                    r1 = f"#{a1}"
                else:
                    r1 = reg_for(a1)
                    
                if is_immediate(a2):
                    r2 = f"#{a2}"
                else:
                    r2 = reg_for(a2)
                
                op_map = {'+': 'add', '-': 'sub', '*': 'mul', '/': 'div'}
                asm_op = op_map.get(op, op)
                
                print(f"{asm_op} {rdst}, {r1}, {r2}    # {tgt} = {a1} {op} {a2}")