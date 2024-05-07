import ply.yacc as yacc
from lex import tokens
from ast_nodes import *
from typing import Optional, List

# Define the TypeChecker class
class TypeChecker:
    def __init__(self):
        self.symbol_table = {}  # Symbol table to store variable types

    def check(self, node):
        if isinstance(node, VarDeclaration):
            self.check_variable_declaration(node)
        elif isinstance(node, AssignExp):
            self.check_assignment_expression(node)
        elif isinstance(node, FunctionDec):
            self.check_function_declaration(node)

    def check_variable_declaration(self, node):
        # Check if variable is already declared
        if node.name in self.symbol_table:
            raise TypeCheckingException(f"Variable {node.name} already declared")
        # Add variable to symbol table
        self.symbol_table[node.name] = node.type
        # Check the initial value type
        exp_type = self.infer_expression_type(node.initial_value)
        if node.type != exp_type:
            raise TypeCheckingException(f"Variable {node.name} type mismatch")

    def check_assignment_expression(self, node):
        # Check if variable is declared
        if node.var.name not in self.symbol_table:
            raise TypeCheckingException(f"Variable {node.var.name} is not declared")
        # Check if expression type matches the variable type
        var_type = self.symbol_table[node.var.name]
        exp_type = self.infer_expression_type(node.exp)
        if var_type != exp_type:
            raise TypeCheckingException(f"Assignment type mismatch")

    def check_function_declaration(self, node):
        # Check return type
        if node.return_type:
            self.check_type(node.return_type)
        # Check parameter types
        for param in node.params:
            self.check_type(param.type)

    def infer_expression_type(self, exp):
        # Perform type inference for expressions
        if isinstance(exp, IntExp):
            return "INT"
        elif isinstance(exp, FloatExp):
            return "FLOAT"
        #elif isinstance(exp, DoubleExp):
        #    return "DOUBLE"
        elif isinstance(exp, StringExp):
            return "STRING"
        elif isinstance(exp, BoolExp):
            return "BOOLEAN"
        # Add more cases for other expression types

    def check_type(self, type):
        # Check if a given type is valid
        valid_types = ["BOOLEAN", "DOUBLE", "FLOAT", "INT", "STRING"]
        if type not in valid_types:
            raise TypeCheckingException(f"Invalid type: {type}")

# Create an instance of the TypeChecker
type_checker = TypeChecker()

# Error class for type checking exceptions
class TypeCheckingException(Exception):
    pass

# Parser rules
def p_declaration(p):
    """
    declaration : var_declaration
                | assign_expression
                | function_declaration
    """
    p[0] = p[1]
    type_checker.check(p[0])  # Perform type checking

def p_var_declaration(p):
    """
    var_declaration : VAR ID COLON type_spec ASSIGN expression SEMICOLON
    """
    p[0] = VarDeclaration(name=p[2], type=p[4], initial_value=p[6])

def p_type_spec(p):
    """
    type_spec : BOOLEAN
              | DOUBLE
              | FLOAT
              | INT
              | STRING
    """
    p[0] = p[1]

def p_assign_expression(p):
    """
    assign_expression : ID ASSIGN expression SEMICOLON
    """
    p[0] = AssignExp(var=Variable(name=p[1]), exp=p[3])

def p_expression(p):
    """
    expression : INT
               | FLOAT
               | DOUBLE
               | STRING
               | BOOLEAN
               | ID
    """
    p[0] = p[1]

def p_function_declaration(p):
    """
    function_declaration : FUNCTION ID LPAREN param_list RPAREN COLON type_spec LBRACE declaration_list RBRACE
    """
    p[0] = FunctionDec(name=p[2], params=p[4], return_type=p[7], body=p[9])

def p_param_list(p):
    """
    param_list : param
               | param_list COMMA param
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_param(p):
    """
    param : ID COLON type_spec
    """
    p[0] = Field(name=p[1], type=p[3])

# Build the parser
parser = yacc.yacc()

# Sample input string to test the parser
input_string = """
VAR x: INT := 10;
VAR y: FLOAT := 3.14;
x := 20;  # This should pass
y := 5;   # This should raise a type mismatch error
FUNCTION add(a: INT, b: INT): INT {
    VAR c: INT := a + b;
    RETURN c;
}
"""

# Parsing the input string
try:
    parsed_output = parser.parse(input_string)
    print("Parsing successful!")
    print("Parsed output:")
    print(parsed_output)
except TypeCheckingException as e:
    print(f"Type checking error: {e}")
