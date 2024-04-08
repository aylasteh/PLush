# coding=utf-8

# flake8: noqa ANN001

# List of token names
tokens = (
    # symbols
    "DOUBLE", ## [double]
    "FLOAT", 
    "INT", ## [int] [[int]] _allowed
    "STRING", #
    "BOOLEAN", # 'true', 'false'
    "ID", #void?
    # ignored symbols the lexer or parser shouldn't mind
    #'NEW_LINE',
    #'TAB',
    #'SPACE',
    #'COMMENT',
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
    "CARET",
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
    "UNDERSCORE",
    # keywords
    #"ARRAY",
    "IF", 
    "THEN", 
    "ELSE", 
    "WHILE", 
    "FUNCTION", 
    "VAR",
    "VAL",
)

reservedKeywords = (
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
def t_DOUBLE(t):
    r"\d+"
    t.value = float(t.value)
    return t

# Reads an integer value
def t_FLOAT(t):
    r"\d+"
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
    r"\""
    t.lexer.string_start = t.lexer.lexpos
    t.lexer.begin("string")


def t_string_word(t):
    r"[^\\\"\n]+"


def t_string_notWord(t):
    r"((\\n)|(\\t)|(\\\^c)|(\\[0-9][0-9][0-9])|(\\\")|(\\\\))+"

# If the lexer reads the beginning of a multiline string, enter special state
def t_string_specialCase(t):
    r"\\"
    t.lexer.special_start = t.lexer.lexpos
    t.lexer.begin("escapeString")


def t_escapeString_finish(t):
    r"\\"
    t.lexer.begin("string")


def t_string_STRING(t):
    # Reads the second character " and returns the STRING token
    r"\""
    t.value = t.lexer.lexdata[t.lexer.string_start - 1 : t.lexer.lexpos]
    t.type = "STRING"
    t.lexer.begin("INITIAL")
    return t

def t_ID(t):
    r"[a-zA-Z][a-zA-Z_0-9]*"
    if t.value in reservedKeywords:
        t.type = t.value.upper()
    return t

# Ignores comments
# Note: it only recognize comments if there is a whitespace at the end of the comment
# i.e: /*any_text */
def t_comment(t):
    r"\#"
    t.lexer.code_start = t.lexer.lexpos
    t.lexer.level = 1
    t.lexer.begin("comment")


def t_comment_begin(t):
    r"\#"
    t.lexer.level += 1
    pass


def t_comment_COMMENT(t):
    r"\S+"
    pass


def t_comment_end(t):
    r"\ "
    t.lexer.level -= 1

    if t.lexer.level == 0:
        t.lexer.begin("INITIAL")

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
t_CARET = r"\^"
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
t_UNDERSCORE = r"\_"


#TODO implement

# A string containing ignored characters (spaces and tabs)
t_ANY_ignore = " \t"

# Error handling rule
def t_ANY_error(t):
    print("Illegal character '%s' in line '%s'" % (t.value[0], t.lineno))


# Build the lexer
#from ply import lex as lex
import sys
from ply import lex as lex

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

    lex.input("1")

    # Tokenize
    while True:
        tok = lex.token()
        if not tok:
            break  # No more input
        print(tok)