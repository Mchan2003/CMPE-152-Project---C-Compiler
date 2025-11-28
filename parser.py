from __future__ import annotations
from dataclasses import dataclass
from lexer import Token, TokenType, TokenClass, Lexer
from typing import Union, Optional
import sys

# @dataclass
# class TreeNode:
#     operand1:str
#     operator: str
#     operand2: str

# @dataclass
# class LeafNode:
#     operand:str

#     def __str__(self):
#         return f"{self.operand}"

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
class Identifier:
    ident: Token

    def __str__(self):
        return f"{self.ident}"

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
    ident: Identifier

    def __str__(self):
        return self._format(0)
    
    def _format(self, level: int) -> str:
        indent = "\t" * level
        child_indent = "\t" * (level + 1)
        
        return (
            f"{indent}DECLARATION:\n"
            f"{indent}[\n"
            f"{child_indent}TYPE: {self.d_type}\n"
            f"{child_indent}IDENTIFIER: {self.ident}\n"
            f"{indent}]"
        )

@dataclass
class Assignment:
    ident: Identifier
    init: E

    def __str__(self):
        return self._format(0)
    
    def _format(self, level: int) -> str:
        indent = "\t" * level
        child_indent = "\t" * (level + 1)
        
        if isinstance(self.init, Expression):
            init_str = f"\n{child_indent}EXPRESSION:\n{self.init._format(level + 1)}"
        else:
            init_str = f"\n{child_indent}EXPRESSION: {self.init}"
        
        return (
            f"{indent}ASSIGNMENT:\n"
            f"{indent}[\n"
            f"{child_indent}IDENTIFIER: {self.ident}\n"
            f"{init_str}\n"
            f"{indent}]"
        )

@dataclass
class Variable:
    declaration: Declaration
    init: Optional[E] = None

    def __str__(self):
        return self._format(0)
    
    def _format(self, level: int) -> str:
        indent = "\t" * level
        child_indent = "\t" * (level + 1)

        dec_str = self.declaration._format(level + 1)
        
        if self.init is not None:
            if isinstance(self.init, Expression):
                init_str = f"\n{child_indent}EXPRESSION:\n{self.init._format(level + 1)}"
            else:
                init_str = f"\n{child_indent}EXPRESSION: {self.init}"
        else:
            init_str = "" 
        
        return (
            f"{indent}VARIABLE:\n"
            f"{indent}[\n"
            f"{dec_str}"
            f"{init_str}\n"
            f"{indent}]"
        )

@dataclass
class Function:
    declaration: Declaration
    parameters: list[Declaration]
    statement_block: StatementBlock

    def __str__(self):
        return self._format(0)
    
    def _format(self, level: int) -> str:
        indent = "\t" * level
        child_indent = "\t" * (level + 1)
        
        func_decl_str = self.declaration._format(level + 1)
        
        if self.parameters:
            params_list = []
            for param in self.parameters:
                params_list.append(param._format(level + 2))
            params_str = f"{child_indent}PARAMETERS:\n{child_indent}[\n" + ",\n".join(params_list) + f"\n{child_indent}]"
        else:
            params_str = f"{child_indent}PARAMETERS: []"
        
        block_str = self.statement_block._format(level + 1)
        
        return (
            f"{indent}FUNCTION:\n"
            f"{indent}[\n"
            f"{func_decl_str}\n"
            f"{params_str}\n"
            f"{block_str}\n"
            f"{indent}]"
        )
    
@dataclass
class Statement:
    statement: Union[Variable, Assignment]

    def __str__(self):
        return self._format(0)
    
    def _format(self, level: int) -> str:
        indent = "\t" * level
        
        return (
            f"{indent}STATEMENT:\n"
            f"{indent}[\n"
            f"{self.statement._format(level + 1)}\n"
            f"{indent}]"
        )

@dataclass
class StatementBlock:
    statement: list[Statement]

    def __str__(self):
        return self._format(0)
    
    def _format(self, level: int) -> str:
        indent = "\t" * level
        
        items_str = "\n".join(stmt._format(level + 1) for stmt in self.statement)
        
        return (
            f"{indent}STATEMENT_BLOCK:\n"
            f"{indent}[\n"
            f"{items_str}\n"
            f"{indent}]"
        )

@dataclass
class Program: 
    programs: list[Union[Function, Statement]]

    def __str__(self):
        return self._format(0)
    
    def _format(self, level: int) -> str:
        indent = "\t" * level
        
        if not self.programs:
            return f"{indent}PROGRAM: []"
        
        items_str = "\n".join(item._format(level + 1) for item in self.programs)
        
        return (
            f"{indent}PROGRAM:\n"
            f"{indent}[\n"
            f"{items_str}\n"
            f"{indent}]"
        )

E = Union[Literal, Expression] 
S = Union[Declaration, Expression]
data_type = {TokenType.INT, TokenType.FLOAT, TokenType.CHAR, TokenType.VOID}
condition_operator = {TokenType.EQUAL_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL,
                      TokenType.LESSER, TokenType.LESSER_EQUAL}

class Parser:
    def __init__(self, line):
        self.root: Optional[StatementBlock] = None
        self.lex = Lexer(line)
        self.tokens = self.lex.get_tokens()
        self.current = -1
        self.temp_count = 0
        self.tac = []
        
    def parse(self):
        self.lex.scan_tokens()
        print("===== TOKENS =====")
        self.lex.print_token()
        self.root = self.parse_program()

        next_token = self.peek()
        if next_token.token_type != TokenType.EOF and next_token.token_type != TokenType.SEMICOLON:
            sys.exit(f"Unexpected token on line {next_token.line}: {next_token.lexeme}")

    def parse_program(self) -> Program:
        program = []
        while 1:
            next_token = self.peek()
            if next_token.token_type == TokenType.EOF:
                break

            next_dec = self.peek_dec()
            print(f"debug: {next_dec}")
            if next_dec.token_type == TokenType.LEFTPARAM:
                func = self.parse_function()
                program.append(func)
            elif next_dec.token_type == TokenType.EQUAL or next_dec.token_type == TokenType.SEMICOLON:
                var = self.parse_statement()                
                program.append(var)
            else:
                sys.exit(f"Not a function nor variable declaration on line {next_token.line}: {next_token.lexeme}")
        return Program(program)

    def parse_statement(self) -> Statement:
        start = self.peek()
        if start.token_class == TokenClass.IDENTIFIER:
            statement = self.parse_assignment()
        elif start.token_class == TokenClass.KEYWORD and start.token_type in data_type:
            statement = self.parse_variable()

        semicolon = self.peek();
        if semicolon.token_type != TokenType.SEMICOLON:
            sys.exit(f"Statement need to end with a ; on line {semicolon.line}: Got {semicolon.lexeme}")
        semicolon = self.next();
    
        return Statement(statement)
    
    def parse_statement_block(self) -> StatementBlock:
        delim = self.peek();
        if delim.token_type != TokenType.LEFTBRACE:
            sys.exit(f"Statement block need to start  with {{ on line {delim.line}: Got {delim.lexeme}")
        delim = self.next();
    
        statements = [];
        while 1:
            statement = self.peek();
            if statement.token_type == TokenType.RIGHTBRACE:
                end = self.next();
                break
            
            if statement.token_type == TokenType.EOF:
                sys.exit(f"Statement block need to end with }} on line {statement.line}: Got {statement.lexeme}")

            statement = self.parse_statement()
            statements.append(statement)    

        return StatementBlock(statements)

    def parse_function(self) -> Function:
        dec = self.parse_declare()
        delim = self.peek()
        if delim.token_type != TokenType.LEFTPARAM:
            sys.exit(f"Function parameter need to start with ( on line {delim.line}: Got {delim.lexeme}")
        delim = self.next()

        param = []
        first_param = self.peek()
        if first_param.token_type != TokenType.RIGHTPARAM:
            param.append(self.parse_declare())

            while self.peek().token_type == TokenType.COMMA:
                self.next()  
                param.append(self.parse_declare())

        if self.peek().token_type != TokenType.RIGHTPARAM:
            sys.exit(f"Function parameter need to end with ) on line {self.peek().line}")
        self.next()  

        block = self.parse_statement_block()

        return Function(dec, param, block)
    
    def parse_assignment(self) -> Assignment:
        ident = self.next()
        if ident.token_type != TokenType.IDENTIFIER:
            sys.exit(f"Token not an identifier for assignment on line ({ident.line}): {ident.lexeme}")

        op = self.peek()
        if op.token_type != TokenType.EQUAL:
            sys.exit(f"Token not an = for assignment on line ({op.line}): {op.lexeme}")
        op = self.next()
        init = self.parse_exp(0.0)

        return Assignment(ident, init)
    
    def parse_variable(self) -> Variable:
        dec = self.parse_declare()
        op = self.peek()
        if op.token_type == TokenType.EQUAL:
            op = self.next()
            init = self.parse_exp(0.0)
            return Variable(dec, init)
        else:
            return Variable(dec, None)
    
    def parse_declare(self) -> Declaration:
        d_type = self.next()

        if d_type.token_class != TokenClass.KEYWORD and d_type.token_type not in data_type:
            sys.exit(f"Invalid data type for declaration on line ({d_type.line}): {d_type.lexeme}")
        
        ident = self.peek()
        if ident.token_type != TokenType.IDENTIFIER and ident.token_type != TokenType.MAIN:
            sys.exit(f"Token not an identifier for declaration on line ({d_type.line}): {d_type.lexeme}")
        ident = self.next()

        return Declaration(d_type, ident);  

    def parse_exp(self, min_bp) -> Expression:
        lhs = self.next()
        
        if lhs.token_type == TokenType.LEFTPARAM:
            lhs = self.parse_exp(0.0)
            right_paren = self.next()
            if right_paren.token_type != TokenType.RIGHTPARAM:
                sys.exit(f"Expected ')' on line {right_paren.line}")
        elif lhs.token_class != TokenClass.LITERAL and lhs.token_class != TokenClass.IDENTIFIER:
            sys.exit(f"Invalid literal on line ({lhs.line}): {lhs.lexeme}")
        else:
            lhs = Literal(lhs)

        while True: 
            op = self.peek()
            if op.token_type == TokenType.EOF:
                break
            if op.token_type == TokenType.SEMICOLON:
                break
            if op.token_type == TokenType.RIGHTPARAM:
                break
            if op.token_class != TokenClass.OPERATOR:
                sys.exit(f"Invalid operator on line ({op.line}): {op.lexeme}")
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
            case TokenType.EQUAL_EQUAL:
                return (8.0, 8.1)
            case TokenType.LESSER | TokenType.LESSER_EQUAL | TokenType.GREATER | TokenType.GREATER_EQUAL:
                return (9.0, 9.1)
            case TokenType.PLUS | TokenType.MINUS:
                return (11.0, 11.1)
            case TokenType.STAR | TokenType.SLASH:
                return (12.0, 12.1)
            case _:
                sys.exit(f"Invalid token on line ({token.line}): {token.lexeme}")

    def next(self):
        self.current += 1
        if self.current >= len(self.tokens):
            sys.exit(f"Parser reach beyond the end of tokens on line: {self.tokens[self.current-1].line} at {self.tokens[self.current-1].lexeme}")
        return self.tokens[self.current]
    
    def peek(self):
        if self.current + 1 < len(self.tokens):
            return self.tokens[self.current + 1]
        return self.tokens[-1]
    
    def peek_dec(self):
        if self.current + 3 < len(self.tokens):
            return self.tokens[self.current + 3]
        return self.tokens[-1]
    
    def print_ast(self):
        print(self.root)

    def new_temp(self) -> str:
        tmp = f"t{self.temp_count}"
        self.temp_count += 1
        return tmp

    def gen_tac(self, target: str, arg1: str, op: str, arg2: Optional[str]):
        self.tac.append((target, arg1, op, arg2))

    def eval_ir(self, node) -> str:
        if isinstance(node, Program):
            for program in node.programs:
                self.eval_ir(program)
            return ""
        
        elif isinstance(node, Function):
            function_name = node.declaration.ident.lexeme

            self.gen_tac("LABEL",function_name, "", None)

            for param in node.parameters:
                param_name = param.ident.lexeme
                self.gen_tac("PARAMETER", param_name, "", None)

            self.eval_ir(node.statement_block)

            self.gen_tac("END", function_name, "", None)
            return function_name
        
        elif isinstance(node, StatementBlock):
            for stmt in node.statement:
                self.eval_ir(stmt)

        elif isinstance(node, Statement):
            self.eval_ir(node.statement)

        elif isinstance(node, Assignment):
            var_name = node.ident.lexeme
            init = self.eval_ir(node.init)
            self.gen_tac(var_name, init, "=", None)
            return var_name
        
        elif isinstance(node, Variable):
            var_name = node.declaration.ident.lexeme
            if node.init is not None:
                init = self.eval_ir(node.init)
                self.gen_tac(var_name, init, "=", None)
            else:
                self.gen_tac("DECLARE", var_name, "", None)
            return var_name
        
        elif isinstance(node, Expression):
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
            return str(node.literal.lexeme)
        
        elif isinstance(node, Identifier):
            return str(node.ident.lexeme)
        
        else:
            raise RuntimeError("Unknown AST node type")

    def generate(self):
        if self.root is None:
            sys.exit("No AST to generate from")
        self.eval_ir(self.root)
        return self.tac

    def dump_tac(self):
        print("=== Three-Address Code ===")
        for tgt, a1, op, a2 in self.tac:
            if tgt in ("LABEL", "END", "PARAMETER", "DECLARE"):
                print(f"{tgt} {a1}")
            elif a2 is None:
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
            match tgt:
                case "LABEL":
                    print(f"\n{a1}: ")
                    print(f"    push rbp")
                    print(f"    mov rbp, rsp")
                    continue
                case "END":
                    print(f"    mov rsp, rbp")
                    print(f"    pop rbp")
                    print(f"    ret")
                    continue
                case "PARAMETER":
                    # rdst = reg_for(a1)
                    # print(f"    # Parameter: {a1} -> {rdst}")
                    continue
                    
                case "DECLARE":
                    # rdst = reg_for(a1)
                    # print(f"    # Declare: {a1} -> {rdst}")
                    continue

            if a2 is None:
                if op == "=":
                    rdst = reg_for(tgt)
                    if is_immediate(a1):
                        print(f"    mov {rdst}, #{a1}")
                    else:
                        rsrc = reg_for(a1)
                        print(f"    mov {rdst}, {rsrc}")
                else:
                    rsrc = reg_for(a1)
                    rdst = reg_for(tgt)
                    print(f"    {op} {rdst}, {rsrc}")
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
                
                print(f"    {asm_op} {rdst}, {r1}, {r2}")