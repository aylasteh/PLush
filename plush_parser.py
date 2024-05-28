import ast_nodes as Node
#import yacc
#from yacc import yacc

from src.ply import yacc as yacc
#import src.ply.yacc as yacc
#from src.lexer.lex import tokens
from lex import tokens

# CONFIGURATION

##
## Precedence and associativity of operators
##
# If this changes, c_generator.CGenerator.precedence_map needs to change as
# well
precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQ', 'NEQ'),
        ('left', 'GT', 'GE', 'LT', 'LE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'PERCENT')
)

start = "program"

def p_program(p):
    """
    program : function_list
            | val_var_exp_list
            | function_list program
            | val_var_exp_list program
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node.ExpressionList(position=p.lineno(2), expr_list=[p[1]] + p[2].expr_list)

def p_function_list(p):
    """
    function_list : function_decl
                  | function_list function_decl
    """
    if len(p) == 2:
        p[0] = Node.ExpressionList(position=p.lineno(1), expr_list=[p[1]])
    else:
        p[0] = Node.ExpressionList(position=p.lineno(2), expr_list=p[1].expr_list + [p[2]])

def p_val_var_exp_list(p):
    """
    val_var_exp_list : val_exp
                     | var_exp
                     | val_var_exp_list val_var_exp_list
    """
    if len(p) == 2:
        p[0] = Node.ExpressionList(position=p[1].position, expr_list=[p[1]])
    else:
        p[0] = Node.ExpressionList(position=p[1].position, expr_list=p[1].expr_list + [p[2]])

def p_block(p):
    "block : LBRACE block_content RBRACE"
    p[0] = p[2]

def p_block_content(p):
    """
    block_content : statement_list
                  | val_var_exp_list
                  | block_content statement_list
                  | block_content val_var_exp_list
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node.ExpressionList(position=p[1].position, expr_list=p[1].expr_list + [p[2]])

 
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
               | assign_exp SEMICOLON
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


def p_statement_list(p):
    """
    statement_list : statement 
                   | statement_list statement
    """
    if len(p) == 2:
        p[0] = Node.ExpressionList(position=p[1].position, expr_list=[p[1]])
    else:
        p[0] = Node.ExpressionList(position=p[1].position, expr_list=p[1].expr_list + [p[2]])


def p_statement(p):
    """
    statement : op_exp SEMICOLON
              | assign_exp SEMICOLON
              | if_then_exp
              | if_then_else_exp
              | while_exp
              | function_call_exp
    """
    p[0] = p[1]

def p_val_expression(p):
    """
    val_expression : op_exp
                   | array_exp
                   | variable
                   | boolean_exp 
                   | double_exp 
                   | float_exp 
                   | int_exp 
                   | string_exp
                   | function_call
    """
    p[0] = p[1]

def p_paren_exp(p):
    "paren_exp : LPAREN expression RPAREN"
    p[0] = p[2]

def p_function_decl(p):
    """
    function_decl : FUNCTION ID LPAREN val_var_decl_list RPAREN COLON complex_type_spec block
                  | FUNCTION ID LPAREN val_var_decl_list RPAREN COLON complex_type_spec SEMICOLON
                  | FUNCTION ID LPAREN val_var_decl_list RPAREN block
                  | FUNCTION ID LPAREN val_var_decl_list RPAREN SEMICOLON
    """
    if len(p) > 7:
        p[0] = Node.FunctionDec(position=p.lineno(1), name=p[2], params=p[4], return_type=p[7], param_escapes=None, arg_types=None, body=p[8] if p[8] != ";" else None)
    else:
        p[0] = Node.FunctionDec(position=p.lineno(1), name=p[2], params=p[4], return_type=None, param_escapes=None, arg_types=None, body=p[6] if p[6] != ";" else None)

def p_type_spec(p):
    """
    type_spec : BOOLEAN
              | DOUBLE
              | FLOAT
              | INT
              | STRING
              | VOID
    """
    p[0] = p[1]

def p_array_type(p):
    """
    array_type : LBRACK type_spec RBRACK
               | LBRACK array_type RBRACK
    """
    p[0] = Node.ArrayExp(position=p.lineno(1), type=p[2], size=None, dimension = [], init=None)

def p_el_with_comma(p):
    """
    el_with_comma : val_expression
                  | array_init
                  | el_with_comma COMMA val_expression
                  | el_with_comma COMMA array_init
    """
    if len(p) == 2:
        p[0] = Node.ExpressionList(position=p[1].position, expr_list=[p[1]])
    else:
        p[0] = Node.ExpressionList(position=p.lineno(1), expr_list=p[1].expr_list + [p[3]])

def p_array_init(p):
    "array_init : LBRACE el_with_comma RBRACE"
    p[0] = p[2]

def p_complex_type_spec(p):
    """
    complex_type_spec : type_spec
                      | array_type
    """
    p[0] = p[1]

def p_val_exp(p):
    "val_exp : val_decl SEMICOLON"
    p[0] = p[1]

def p_val_decl(p):
    """
    val_decl : VAL variable COLON complex_type_spec ASSIGN val_expression
             | VAL variable COLON complex_type_spec ASSIGN array_init
             | VAL variable COLON complex_type_spec
    """
    if len(p) == 7:
        p[0] = Node.ValVarDeclaration(isval = True, position=p.lineno(1),name=p[2].var,type=p[4],value=p[6])
    else:
        p[0] = Node.ValVarDeclaration(isval = True, position=p.lineno(1),name=p[2].var,type=p[4],value=None)
    
def p_var_decl(p):
    """
    var_decl : VAR variable COLON complex_type_spec ASSIGN val_expression
             | VAR variable COLON complex_type_spec ASSIGN array_init
             | VAR variable COLON complex_type_spec
    """
    if len(p) == 7:
        p[0] = Node.ValVarDeclaration(isval = False, position=p.lineno(1),name=p[2].var,type=p[4],value=p[6])
    else:
        p[0] = Node.ValVarDeclaration(isval = False, position=p.lineno(1),name=p[2].var,type=p[4],value=None)

def p_var_exp(p):
    "var_exp : var_decl SEMICOLON"
    p[0] = p[1]

def p_val_var_decl_list(p):
    """
    val_var_decl_list : val_decl
                      | var_decl
                      | val_var_decl_list COMMA val_decl
                      | val_var_decl_list COMMA var_decl
                      | empty_exp
    """
    if len(p) == 2:
        p[0] = Node.ValVarList(position=p[1].position, args=[p[1]])
    else:
        p[0] = Node.ValVarList(position=p.lineno(3), args=p[1].args + [p[3]])

def p_function_call(p):
    """
    function_call : ID LPAREN el_with_comma RPAREN 
                  | ID LPAREN empty_exp RPAREN
    """
    p[0] = Node.FunctionCall(position=p.lineno(1), name=p[1], args=p[3])

def p_function_call_exp(p):
    "function_call_exp : function_call SEMICOLON"
    p[0] = p[1]

def p_boolean_exp(p):
    "boolean_exp : BOOLEAN_VAL"
    p[0] = Node.BoolExp(position=p.lineno(1), value=True if p[1] == 'true' else False)

def p_double_exp(p):
    "double_exp : DOUBLE_VAL"
    p[0] = Node.FloatExp(position=p.lineno(1), value=p[1])

def p_float_exp(p):
    "float_exp : FLOAT_VAL"
    p[0] = Node.FloatExp(position=p.lineno(1), value=p[1])

def p_int_exp(p):
    "int_exp : INT_VAL"
    p[0] = Node.IntExp(position=p.lineno(1), int=p[1])

def p_string_exp(p):
    "string_exp : STRING_VAL"
    p[0] = Node.StringExp(position=p.lineno(1), string=p[1])

# Non-empty expression sequence.
def p_assign_exp(p):
    """
    assign_exp : variable ASSIGN op_exp
               | array_exp ASSIGN op_exp
    """
    p[0] = Node.AssignExp(position=p.lineno(2), var=p[1], exp=p[3])

def p_if_then_exp(p):
    "if_then_exp : IF op_exp block"
    p[0] = Node.IfExp(position=p.lineno(1), test=p[2], then_do=p[3], else_do=None)

def p_if_then_else_exp(p):
    "if_then_else_exp : IF op_exp block ELSE block"
    p[0] = Node.IfExp(position=p.lineno(1), test=p[2], then_do=p[3], else_do=p[5])

def p_while_exp(p):
    "while_exp : WHILE op_exp block"
    p[0] = Node.WhileExp(position=p.lineno(1), test=p[2], body=p[3])



def p_array_index(p):
    """
    array_index : LBRACK expression RBRACK
                | array_index LBRACK expression RBRACK
    """
    if len(p) == 4:
        p[0] = Node.ExpressionList(position=p.lineno(2), expr_list=[p[2]])
    else:
        p[0] = Node.ExpressionList(position=p.lineno(3), expr_list=p[1].expr_list + [p[3]])

def p_array_exp(p):
    """
    array_exp : ID array_index
              | function_call array_index
    """
    p[0] = Node.ArrayExp(position=p.lineno(1), type=p[1], size=p[2], dimension = [], init=None)

#VARIABLE
def p_variable(p):
    "variable : ID"
    p[0] = Node.VarExp(position=p.lineno(1), var=p[1])

def p_empty_exp(p):
    "empty_exp :"
    p[0] = Node.EmptyExp(position=p.lineno(0))

def p_paren_op_exp(p):
    "paren_op_exp : LPAREN op_exp RPAREN"
    p[0] = p[2]

def p_op_exp(p):
    """
    op_exp : binary_arith_exp
           | binary_compare_exp
           | paren_op_exp
           | unary_not_exp
           | array_exp
           | variable
           | boolean_exp 
           | double_exp 
           | float_exp 
           | int_exp 
           | string_exp
           | function_call
    """
    p[0] = p[1]

def p_binary_arith_exp(p):
    "binary_arith_exp : op_exp PLUS op_exp"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.plus, left=p[1], right=p[3])

def p_binary_arith_exp_minus(p):
    "binary_arith_exp : op_exp MINUS op_exp"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.minus, left=p[1], right=p[3])

def p_binary_arith_exp_times(p):
    "binary_arith_exp : op_exp TIMES op_exp"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.times, left=p[1], right=p[3])

def p_binary_arith_exp_exponend(p):
    "binary_arith_exp : op_exp CARET op_exp"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.exponent, left=p[1], right=p[3])

def p_binary_divide_exp_divide(p):
    "binary_arith_exp : op_exp DIVIDE op_exp"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.divide, left=p[1], right=p[3])

def p_binary_arith_exp_modulo(p):
    "binary_arith_exp : op_exp PERCENT op_exp"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.mod, left=p[1], right=p[3])

def p_binary_compare_exp(p):
    "binary_compare_exp : op_exp EQ op_exp"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.eq, left=p[1], right=p[3])

def p_binary_compare_exp_neq_exp(p):
    "binary_compare_exp : op_exp NEQ op_exp"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.neq, left=p[1], right=p[3])

def p_binary_compare_exp_lt_exp(p):
    "binary_compare_exp : op_exp LT op_exp"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.lt, left=p[1], right=p[3])

def p_binary_compare_exp_le_exp(p):
    "binary_compare_exp : op_exp LE op_exp"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.le, left=p[1], right=p[3])

def p_binary_compare_exp_gt_exp(p):
    "binary_compare_exp : op_exp GT op_exp"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.gt, left=p[1], right=p[3])

def p_binary_compare_exp_ge_exp(p):
    "binary_compare_exp : op_exp GE op_exp"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.ge, left=p[1], right=p[3])

def p_binary_compare_exp_and_exp(p):
    "binary_compare_exp : op_exp AND op_exp"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.andop, left=p[1], right=p[3])

def p_binary_compare_exp_or_exp(p):
    "binary_compare_exp : op_exp OR op_exp"
    p[0] = Node.OpExp(position=p.lineno(2), oper=Node.Oper.orop, left=p[1], right=p[3])

def p_unary_not_exp(p):
    "unary_not_exp : NOT op_exp"
    p[0] = Node.OpExp(position=p.lineno(1), oper=Node.Oper.notop, left=None, right=p[2])

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

parsed_output = None

def plush_parse(input_string):
    try:
        parsed_output = parser.parse(input_string)

    except SyntacticError as e:
        print(f"Syntax error: {e}")
        parsed_output = None
        
    if parsed_output == None:
        print("error parsing")
        exit ()

    return parsed_output
