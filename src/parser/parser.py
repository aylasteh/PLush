import ast_nodes as Node
import ply.yacc as yacc
#from lexer.lex import tokens

# CONFIGURATION

start = "expression"

# EXPRESSION
def p_expression(p):
    """
    expression : paren_exp #
               | var_exp #
               | val_exp #
               | boolean_exp #
               | double_exp #
               | char_exp
               | float_exp #
               | int_exp #
               | string_exp #
               | assign_exp #
               | if_then_exp #
               | if_then_else_exp #
               | while_exp #
               | array_exp #
               | empty_exp
    """
    p[0] = p[1]

def p_paren_exp(p):
    "paren_exp : LPAREN expression RPAREN"
    p[0] = p[2]

def p_var_exp(p):
    "var_exp : variable"
    p[0] = Node.VarExp(position=p.slice[1].value.position, var=p[1])

def p_val_exp(p):
    "val_exp : variable"
    p[0] = Node.VarExp(position=p.slice[1].value.position, var=p[1])

def p_boolean_exp(p):
    "boolean_exp : BOOLEAN"
    p[0] = Node.IntExp(position=p.lineno(1), int=p[1])

def p_double_exp(p):
    "double_exp : DOUBLE"
    p[0] = Node.IntExp(position=p.lineno(1), int=p[1])

def p_float_exp(p):
    "float_exp : FLOAT"
    p[0] = Node.IntExp(position=p.lineno(1), int=p[1])

def p_int_exp(p):
    "int_exp : INT"
    p[0] = Node.IntExp(position=p.lineno(1), int=p[1])

def p_string_exp(p):
    "string_exp : STRING"
    p[0] = Node.StringExp(position=p.lineno(1), string=p[1])

# Non-empty expression sequence.
def p_assign_exp(p):
    "assign_exp : variable ASSIGN expression"
    p[0] = Node.AssignExp(position=p.lineno(2), var=p[1], exp=p[3])

def p_if_then_exp(p):
    "if_then_exp : IF expression LBRACE expression RBRACE"
    p[0] = Node.IfExp(position=p.lineno(1), test=p[2], then_do=p[4], else_do=None)

def p_if_then_else_exp(p):
    "if_then_else_exp : IF expression LBRACE expression RBRACE ELSE LBRACE expression RBRACE"
    p[0] = Node.IfExp(position=p.lineno(1), test=p[2], then_do=p[4], else_do=p[8])

def p_while_exp(p):
    "while_exp : WHILE expression LBRACE expression RBRACE"
    p[0] = Node.WhileExp(position=p.lineno(1), test=p[2], body=p[4])

def p_array_exp(p):
    "array_exp : ID LBRACK expression RBRACK"
    p[0] = Node.ArrayExp(position=p.lineno(1), type=p[1], size=p[3], init=p[6])

#VARIABLE
def p_variable(p):
    "simple_var ASSIGN ID"
    p[0] = Node.SimpleVar(position=p.lineno(1), sym=p[1])

def p_empty_exp(p):
    "empty_exp :"
    p[0] = Node.EmptyExp(position=p.lineno(0))

#TODO implement

# ERROR
class SyntacticError(Exception):
    def __init__(self, value: str, position: int):
        self.value = value
        self.position = position

    def __str__(self):
        return f"Syntax error in input! Unexpected value {self.value} in line {self.position}"


def p_error(p):
    raise SyntacticError(p.value, p.lexer.lineno)

# Build the parser
parser = yacc.yacc()