# coding=utf-8

# flake8: noqa ANN001

# List of token names
tokens = (
    # symbols
    "DOUBLE_VAL",
    "DOUBLE", ## [double]
    "FLOAT_VAL",
    "FLOAT", 
    "INT_VAL",
    "INT", ## [int] [[int]] _allowed
    "STRING_VAL",
    "STRING", #
    "BOOLEAN_VAL",
    "BOOLEAN", # 'true', 'false'
    "ID", #void?
    # ignored symbols the lexer or parser shouldn't mind
    #'NEW_LINE',
    #'TAB',
    #'SPACE',
    'COMMENT',
    # punctuation symbols
    "COMMA",
    "COLON",
    "SEMICOLON",
    "LPAREN", 
    "RPAREN", 
    "LBRACK", 
    "RBRACK", 
    "LBRACE", 
    "RBRACE", 
    #"CARET",
    "PLUS", 
    "MINUS", 
    "TIMES", 
    "DIVIDE", 
    "EQ", 
    "NEQ", 
    "LT", 
    "LE", 
    "GT", 
    "GE", 
    "AND", 
    "OR", 
    "ASSIGN", 
    "PERCENT", 
    #"UNDERSCORE",
    # keywords
    #"ARRAY",
    "IF", 
    #"THEN", 
    "ELSE", 
    "WHILE", 
    "FUNCTION", 
    "VAR",
    "VAL",
)

reservedKeywords = (
    "int",
    "float",
    "double",
    "string",
    "boolean",
    "if",
    "then",
    "else",
    "while",
    "function",
    "var",
    "val"
)

# Regular expression rules with some actions required
# Reads an integer value
def t_DOUBLE_VAL(t):
    r"\d+\.\d*|\.\d+"
    t.value = float(t.value)
    return t

# Reads an integer value
def t_FLOAT_VAL(t):
    r'\d+\.\d*|\.\d+'
    t.value = float(t.value)
    return t

# Reads an integer value
def t_INT(t):
    r"\d+"
    t.value = int(t.value)
    return t


#TODO String not working


# Reads a string
def t_string(t):
    # Reads the first character " and jumps to the string state
    r'\"'
    t.lexer.string_buffer = []
    t.lexer.begin('string')

def t_string_end(t):
    r'\"'
    t.value = ''.join(t.lexer.string_buffer)
    t.type = "STRING_VAL"
    t.lexer.begin('INITIAL')
    return t
'''
def t_string_content(t):
    r'[^\\"]+'
    t.lexer.string_buffer.extend(t.value)

def t_string_escape(t):
    r'\\.'
    # Translate special escape sequences
    escape_sequences = {
        'n': '\n',
        't': '\t',
        '"': '\"',
        '\\': '\\'
    }
    # Append the correct character to the buffer
    t.lexer.string_buffer.append(escape_sequences.get(t.value[1], t.value[1]))'''

'''
def t_string_error(t):
    print(f"Illegal character in the string: {t.value[0]}")
    t.lexer.skip(1)

# Error handling rule for the initial state
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)'''


def t_ID(t):
    r"[a-zA-Z][a-zA-Z_0-9]*"
    if t.value in reservedKeywords:
        t.type = t.value.upper()
    return t

# Ignores comments
def t_comment(t):
    r'\#.*'
    pass  # Ignore the comment

# Regular expression rules for simple tokens
t_COMMA = r"\,"
t_COLON = r"\:"
t_SEMICOLON = r"\;"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACK = r"\["
t_RBRACK = r"\]"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
#t_CARET = r"\^"
t_PLUS = r"\+"
t_MINUS = r"\-"
t_TIMES = r"\*"
t_DIVIDE = r"\/"
t_EQ = r"\="
t_NEQ = r"\!\="
t_LT = r"\<"
t_LE = r"\<\="
t_GT = r"\>"
t_GE = r"\>\="
t_AND = r"\&\&"
t_OR = r"\|\|"
t_ASSIGN = r"\:\="
t_PERCENT = r"\%"
#t_UNDERSCORE = r"\_"


#TODO implement

# A string containing ignored characters (spaces and tabs)
t_ANY_ignore = " \t"

# Error handling rule
def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
#from ply import lex as lex
import sys
from src.ply import lex as lex

lexer = lex.lex()

if __name__ == "__main__":
    '''
    if len(sys.argv) > 1:
        #test einlesen
        test = ','
        f = open(sys.argv[1], "r")
        data = f.read()
        f.close()
    else:
        data = ""
        while True:
            try:
                data += raw_input() + "\n"
            except:
                break'''
    
    data = ''' x
    3 + 4 * 10
    + -20 *2
    '''

    lex.input(data)

    # Tokenize
    while True:
        tok = lex.token()
        if not tok:
            break  # No more input
        print(tok)