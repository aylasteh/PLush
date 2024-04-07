# coding=utf-8

# flake8: noqa ANN001

# List of token names
tokens = (
    "COMMA",
    "VAR"
)

reservedKeywords = (
    "var"
)

# Regular expression rules for simple tokens
t_COMMA = r","



#TODO implement



# Build the lexer
from ply import lex as lex
import sys

lexer = lex.lex()

if __name__ == "__main__":

    if len(sys.argv) > 1:
        f = open(sys.argv[1], "r")
        data = f.read()
        f.close()
    else:
        data = ""
        '''while True:
            try:
                data += raw_input() + "\n"
            except:
                break'''

    lex.input(data)

    # Tokenize
    while True:
        tok = lex.token()
        if not tok:
            break  # No more input
        print(tok)