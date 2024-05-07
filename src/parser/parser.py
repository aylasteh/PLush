'''import ast_nodes as Node
import src.ply.yacc as yacc
from src.lexer.lex import tokens

# CONFIGURATION

start = "expression"

# EXPRESSION
def p_expression(p):
    """
    expression : paren_exp 
               | function_decl
               | function_call
               | var_exp 
               | val_exp
               | boolean_exp 
               | double_exp 
               | float_exp 
               | int_exp 
               | string_exp 
               | assign_exp 
               | if_then_exp 
               | if_then_else_exp 
               | while_exp 
               | array_exp 
               | empty_exp
               | op_exp
               | id_exp
               | comment
               | terminator
    """
    if len(p) == 2:  # Check if only comment is parsed
        p[0] = p[1]
    else:
        p[0] = p[1]

def p_paren_exp(p):
    "paren_exp : LPAREN expression RPAREN"
    p[0] = p[2]

def p_function_decl(p):
    """
    function_decl : FUNCTION ID LPAREN args_list RPAREN COLON type_spec LBRACE block RBRACE
                  | FUNCTION ID LPAREN args_list RPAREN COLON type_spec SEMICOLON
    """
    p[0] = Node.FunctionDec(position=p.lineno(1), name=p[2], args=p[4], return_type=p[7], block=p[9] if len(p) > 8 else None)

def p_args_list(p):
    """
    args_list : expression
              | args_list COMMA expression
    """
    if len(p) == 2:
        p[0] = Node.ArgsList(args=[p[1]])
    else:
        p[0] = Node.ArgsList(args=[p[1]] + p[3].args)

def p_function_call_exp(p):
    "function_call_exp : ID LPAREN args_list RPAREN"
    p[0] = Node.FunctionCall(position=p.lineno(1), name=p[1], args=p[3])

def p_var_exp(p):
    "var_exp : VAR variable ASSIGN expression"
    p[0] = Node.VarExp(position=p.slice[1].value.position, var=p[1])

def p_val_exp(p):
    "val_exp : VAL variable ASSIGN expression"
    p[0] = Node.VarExp(position=p.slice[1].value.position, var=p[1])

def p_boolean_exp(p):
    "boolean_exp : BOOLEAN"
    p[0] = Node.BoolExp(position=p.lineno(1), value=True if p[1] == 'true' else False)

def p_double_exp(p):
    "double_exp : DOUBLE"
    p[0] = Node.IntExp(position=p.lineno(1), int=p[1])

def p_float_exp(p):
    "float_exp : FLOAT"
    p[0] = Node.FloatExp(position=p.lineno(1), int=p[1])

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
    p[0] = Node.IfExp(position=p.lineno(1), test=p[2], then_do=p[4], else_do=p[7])

def p_while_exp(p):
    "while_exp : WHILE expression LBRACE expression RBRACE"
    p[0] = Node.WhileExp(position=p.lineno(1), test=p[2], body=p[4])

def p_array_exp(p):
    "array_exp : ID LBRACK expression RBRACK"
    p[0] = Node.ArrayExp(position=p.lineno(1), type=p[1], size=p[3], init=p[6])

#VARIABLE
def p_variable(p):
    "variable : ID"
    p[0] = Node.SimpleVar(position=p.lineno(1), sym=p[1])

def p_empty_exp(p):
    "empty_exp :"
    p[0] = Node.EmptyExp(position=p.lineno(0))

def p_op_exp(p):
    """op_exp : binary_plus_exp
           | binary_minus_exp
           | binary_times_exp
           | binary_divide_exp
           | binary_eq_exp
           | binary_neq_exp
           | binary_lt_exp
           | binary_le_exp
           | binary_gt_exp
           | binary_ge_exp
           | binary_and_exp
           | binary_or_exp
           | binary_mod_exp"""
    p[0] = p[1]

def p_binary_plus_exp(p):
    "binary_plus_exp : expression PLUS expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.plus, left=p[1], right=p[3])


def p_binary_minus_exp(p):
    "binary_minus_exp : expression MINUS expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.minus, left=p[1], right=p[3])


def p_binary_times_exp(p):
    "binary_times_exp : expression TIMES expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.times, left=p[1], right=p[3])


def p_binary_divide_exp(p):
    "binary_divide_exp : expression DIVIDE expression"
    p[0] = Node.OpExp(
        position=p.lineno(2), oper=Node.Oper.divide, left=p[1], right=p[3]
    )


def p_binary_eq_exp(p):
    "binary_eq_exp : expression EQ expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.eq, left=p[1], right=p[3])


def p_binary_neq_exp(p):
    "binary_neq_exp : expression NEQ expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.neq, left=p[1], right=p[3])


def p_binary_lt_exp(p):
    "binary_lt_exp : expression LT expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.lt, left=p[1], right=p[3])


def p_binary_le_exp(p):
    "binary_le_exp : expression LE expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.le, left=p[1], right=p[3])


def p_binary_gt_exp(p):
    "binary_gt_exp : expression GT expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.gt, left=p[1], right=p[3])


def p_binary_ge_exp(p):
    "binary_ge_exp : expression GE expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.ge, left=p[1], right=p[3])


def p_binary_and_exp(p):
    "binary_and_exp : expression AND expression"
    #p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.and, left=p[1], right=p[3])
    p[0] = Node.IfExp(
        position=p.lineno(2),
        test=p[1],
        then_do=p[3],
        else_do=Node.IntExp(position=p.lineno(2), int=0),
    )


def p_binary_or_exp(p):
    "binary_or_exp : expression OR expression"
    #p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.or, left=p[1], right=p[3])
    p[0] = Node.IfExp(
        position=p.lineno(2),
        test=p[1],
        then_do=Node.IntExp(position=p.lineno(2), int=1),
        else_do=p[3],
    )

def p_binary_mod_exp(p):
    "binary_mod_exp : expression MOD expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.mod, left=p[1], right=p[3])


def p_id_exp(p):
    "id_exp : ID"
    p[0]=p[1]

# COMMENT
def p_comment(p):
    """
    comment : COMMENT_CONTENT
    """
    pass  # Ignore comments

def p_terminator(p):
    """
    terminator : SEMICOLON
    """
    pass  # Ignore semicolons

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


# Sample input string to test the parser
input_string = "if (x < 10) { y = x + 1;} else {y = x - 1;}"
input_string = "if x = 10 { y = x + 1}"
#input_string = "if x { y }"
input_string = "var x := int 1"
#input_string = "int "
#input_string = "23"
#input_string = "int = 23"
#input_string = "var "

# Parsing the input string
try:
    parsed_output = parser.parse(input_string)
    print("Parsing successful!")
    print("Parsed output:")
    print(parsed_output)
except SyntacticError as e:
    print(f"Syntax error: {e}")
'''

import ast_nodes as Node
from ply.yacc import yacc
#import src.ply.yacc as yacc
#from src.lexer.lex import tokens
from lexer.lex import tokens

# CONFIGURATION

start = "expression"

# EXPRESSION
def p_expression(p):
    """
    expression : paren_exp 
               | function_decl
               | function_call_exp
               | var_exp 
               | val_exp
               | boolean_exp 
               | double_exp 
               | float_exp 
               | int_exp 
               | string_exp 
               | assign_exp 
               | if_then_exp 
               | if_then_else_exp 
               | while_exp 
               | array_exp 
               | empty_exp
               | op_exp
               | id_exp
               | comment
               | terminator
    """
    if len(p) == 2:  # Check if only comment is parsed
        p[0] = p[1]
    else:
        p[0] = p[1]

def p_paren_exp(p):
    "paren_exp : LPAREN expression RPAREN"
    p[0] = p[2]

def p_function_decl(p):
    """
    function_decl : FUNCTION ID LPAREN args_list RPAREN COLON type_spec LBRACE expression RBRACE
                  | FUNCTION ID LPAREN args_list RPAREN COLON type_spec SEMICOLON
    """
    p[0] = Node.FunctionDec(position=p.lineno(1), name=p[2], args=p[4], return_type=p[7], block=p[9] if len(p) > 8 else None)

def p_type_spec(p):
    """
    type_spec: BOOLEAN
             | DOUBLE
             | FLOAT
             | INT
             | STRING
    """

def p_args_list(p):
    """
    args_list : expression
              | args_list COMMA expression
    """
    if len(p) == 2:
        p[0] = Node.ArgsList(args=[p[1]])
    else:
        p[0] = Node.ArgsList(args=[p[1]] + p[3].args)

def p_function_call_exp(p):
    "function_call_exp : ID LPAREN args_list RPAREN"
    p[0] = Node.FunctionCall(position=p.lineno(1), name=p[1], args=p[3])

def p_var_exp(p):
    "var_exp : VAR variable ASSIGN expression"
    p[0] = Node.VarExp(position=p.slice[1].value.position, var=p[1])

def p_val_exp(p):
    "val_exp : VAL variable ASSIGN expression"
    p[0] = Node.VarExp(position=p.slice[1].value.position, var=p[1])

def p_boolean_exp(p):
    "boolean_exp : BOOLEAN"
    p[0] = Node.BoolExp(position=p.lineno(1), value=True if p[1] == 'true' else False)

def p_double_exp(p):
    "double_exp : DOUBLE"
    p[0] = Node.IntExp(position=p.lineno(1), int=p[1])

def p_float_exp(p):
    "float_exp : FLOAT"
    p[0] = Node.FloatExp(position=p.lineno(1), int=p[1])

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
    p[0] = Node.IfExp(position=p.lineno(1), test=p[2], then_do=p[4], else_do=p[7])

def p_while_exp(p):
    "while_exp : WHILE expression LBRACE expression RBRACE"
    p[0] = Node.WhileExp(position=p.lineno(1), test=p[2], body=p[4])

def p_array_exp(p):
    "array_exp : ID LBRACK expression RBRACK"
    p[0] = Node.ArrayExp(position=p.lineno(1), type=p[1], size=p[3], init=p[6])

#VARIABLE
def p_variable(p):
    "variable : ID"
    p[0] = Node.SimpleVar(position=p.lineno(1), sym=p[1])

def p_empty_exp(p):
    "empty_exp :"
    p[0] = Node.EmptyExp(position=p.lineno(0))

def p_op_exp(p):
    """op_exp : binary_plus_exp
           | binary_minus_exp
           | binary_times_exp
           | binary_divide_exp
           | binary_eq_exp
           | binary_neq_exp
           | binary_lt_exp
           | binary_le_exp
           | binary_gt_exp
           | binary_ge_exp
           | binary_and_exp
           | binary_or_exp
           | binary_mod_exp"""
    p[0] = p[1]

def p_binary_plus_exp(p):
    "binary_plus_exp : expression PLUS expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.plus, left=p[1], right=p[3])


def p_binary_minus_exp(p):
    "binary_minus_exp : expression MINUS expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.minus, left=p[1], right=p[3])


def p_binary_times_exp(p):
    "binary_times_exp : expression TIMES expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.times, left=p[1], right=p[3])


def p_binary_divide_exp(p):
    "binary_divide_exp : expression DIVIDE expression"
    p[0] = Node.OpExp(
        position=p.lineno(2), oper=Node.Oper.divide, left=p[1], right=p[3]
    )


def p_binary_eq_exp(p):
    "binary_eq_exp : expression EQ expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.eq, left=p[1], right=p[3])


def p_binary_neq_exp(p):
    "binary_neq_exp : expression NEQ expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.neq, left=p[1], right=p[3])


def p_binary_lt_exp(p):
    "binary_lt_exp : expression LT expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.lt, left=p[1], right=p[3])


def p_binary_le_exp(p):
    "binary_le_exp : expression LE expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.le, left=p[1], right=p[3])


def p_binary_gt_exp(p):
    "binary_gt_exp : expression GT expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.gt, left=p[1], right=p[3])


def p_binary_ge_exp(p):
    "binary_ge_exp : expression GE expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.ge, left=p[1], right=p[3])


def p_binary_and_exp(p):
    "binary_and_exp : expression AND expression"
    #p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.and, left=p[1], right=p[3])
    p[0] = Node.IfExp(
        position=p.lineno(2),
        test=p[1],
        then_do=p[3],
        else_do=Node.IntExp(position=p.lineno(2), int=0),
    )


def p_binary_or_exp(p):
    "binary_or_exp : expression OR expression"
    #p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.or, left=p[1], right=p[3])
    p[0] = Node.IfExp(
        position=p.lineno(2),
        test=p[1],
        then_do=Node.IntExp(position=p.lineno(2), int=1),
        else_do=p[3],
    )

def p_binary_mod_exp(p):
    "binary_mod_exp : expression PERCENT expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.mod, left=p[1], right=p[3])


def p_id_exp(p):
    "id_exp : ID"
    p[0]=p[1]

# COMMENT
def p_comment(p):
    """
    comment : COMMENT
    """
    pass  # Ignore comments

def p_terminator(p):
    """
    terminator : SEMICOLON
    """
    pass  # Ignore semicolons

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


# Sample input string to test the parser
input_string = "if (x < 10) { y = x + 1;} else {y = x - 1;}"
input_string = "if x = 10 { y = x + 1}"
#input_string = "if x { y }"
input_string = "var x := int 1"
#input_string = "int "
#input_string = "23"
#input_string = "int = 23"
#input_string = "var "

# Parsing the input string
try:
    parsed_output = parser.parse(input_string)
    print("Parsing successful!")
    print("Parsed output:")
    print(parsed_output)
except SyntacticError as e:
    print(f"Syntax error: {e}")


'''import ast_nodes as Node
import src.ply.yacc as yacc
from src.lexer.lex import tokens

# CONFIGURATION

start = "expression"

# EXPRESSION
def p_expression(p):
    """
    expression : paren_exp 
               | var_exp 
               | val_exp
               | boolean_exp 
               | double_exp 
               | float_exp 
               | int_exp 
               | string_exp 
               | assign_exp 
               | if_then_exp 
               | if_then_else_exp 
               | while_exp 
               | array_exp 
               | empty_exp
               | op_exp
               | id_exp
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
    "variable : ASSIGN ID"
    p[0] = Node.SimpleVar(position=p.lineno(1), sym=p[1])

def p_empty_exp(p):
    "empty_exp :"
    p[0] = Node.EmptyExp(position=p.lineno(0))

def p_op_exp(p):
    """op_exp : binary_plus_exp
           | binary_minus_exp
           | binary_times_exp
           | binary_divide_exp
           | binary_eq_exp
           | binary_neq_exp
           | binary_lt_exp
           | binary_le_exp
           | binary_gt_exp
           | binary_ge_exp
           | binary_and_exp
           | binary_or_exp"""
    p[0] = p[1]

def p_binary_plus_exp(p):
    "binary_plus_exp : expression PLUS expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.plus, left=p[1], right=p[3])


def p_binary_minus_exp(p):
    "binary_minus_exp : expression MINUS expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.minus, left=p[1], right=p[3])


def p_binary_times_exp(p):
    "binary_times_exp : expression TIMES expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.times, left=p[1], right=p[3])


def p_binary_divide_exp(p):
    "binary_divide_exp : expression DIVIDE expression"
    p[0] = Node.OpExp(
        position=p.lineno(2), oper=Node.Oper.divide, left=p[1], right=p[3]
    )


def p_binary_eq_exp(p):
    "binary_eq_exp : expression EQ expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.eq, left=p[1], right=p[3])


def p_binary_neq_exp(p):
    "binary_neq_exp : expression NEQ expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.neq, left=p[1], right=p[3])


def p_binary_lt_exp(p):
    "binary_lt_exp : expression LT expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.lt, left=p[1], right=p[3])


def p_binary_le_exp(p):
    "binary_le_exp : expression LE expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.le, left=p[1], right=p[3])


def p_binary_gt_exp(p):
    "binary_gt_exp : expression GT expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.gt, left=p[1], right=p[3])


def p_binary_ge_exp(p):
    "binary_ge_exp : expression GE expression"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.ge, left=p[1], right=p[3])


def p_binary_and_exp(p):
    "binary_and_exp : expression AND expression"
    p[0] = Node.IfExp(
        position=p.lineno(2),
        test=p[1],
        then_do=p[3],
        else_do=Node.IntExp(position=p.lineno(2), int=0),
    )


def p_binary_or_exp(p):
    "binary_or_exp : expression OR expression"
    p[0] = Node.IfExp(
        position=p.lineno(2),
        test=p[1],
        then_do=Node.IntExp(position=p.lineno(2), int=1),
        else_do=p[3],
    )

def p_id_exp(p):
    "id_exp : ID"
    p[0]=p[1]

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


# Sample input string to test the parser
input_string = "if (x < 10) { y = x + 1;} else {y = x - 1;}"
input_string = "if x = 10 { y = x + 1}"
input_string = "if x { y }"
input_string = "var x := int 1"
#input_string = "int "
#input_string = "23"
input_string = "int = 23"
#input_string = "var "

# Parsing the input string
try:
    parsed_output = parser.parse(input_string)
    print("Parsing successful!")
    print("Parsed output:")
    print(parsed_output)
except SyntacticError as e:
    print(f"Syntax error: {e}")'''