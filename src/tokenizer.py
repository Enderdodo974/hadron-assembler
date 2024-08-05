#-*- coding: utf-8 -*-

# ---------------------------------------------------------------------------- #
# tokenizer.py
# 
# This file contains the tokenizer for the Hadron Assembler. It is used by
# instancing the HASMTokenizer and reading a source file.
# ---------------------------------------------------------------------------- #

# ------------------------------------ #
# Libraries imports
from ply import lex

# ------------------------------------ #
# Files imports
import src.hasm_tokens as hasm_tokens

# ------------------------------------ #
# Classes
class HASMTokenizer:
    
    def __init__(self) -> None:
        pass

if __name__ == '__main__':
    
    lexer = lex.lex(module=hasm_tokens)
    
    data = '''
    .;:~+-%$@#[]<= == >=
    ,,,,,           
    identifier
    0x123
    0X1_2_3
    
    0o123
    0O1_2_3
    0b1_111
    0B0000_1111  // this is a comment
    /*
    multiline comment
    
    
    */
    123
    1_2_3
    1.1123
    1e6
    1e-6
    .123
    1_1.e+4
    "hi i'm a string"
    "and another \\
    string"
    'a'
    '\\n'
    '\\t'
    '''

    lex.input(data)
    
    while True:
        token = lexer.token()
        if not token:
            break
        print(token)