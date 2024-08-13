#-*- coding: utf-8 -*-

# ---------------------------------------------------------------------------- #
# hasm_tokens.py
#
# Token specifications for symbols in Hadron Assembly Language. This file is
# meant to be used by the dedicated tokenizer.
# ---------------------------------------------------------------------------- #

# -------------------------------------------------------- #
# Files imports
import src.constants as c
from src.exceptions import ParserError, warn

# -------------------------------------------------------- #
# Tokens

# ---------------- #
# Keywords
keywords = {
    'bits': 'HEADER_BITS',
    'run': 'HEADER_RUN',
    'rom': 'HEADER_RUN_VALUE_ROM',
    'ram': 'HEADER_RUN_VALUE_RAM',
    'minreg': 'HEADER_MINREG',
    'minheap': 'HEADER_MINHEAP',
    'minstack': 'HEADER_MINSTACK',
    'pc': 'SPE_REG_PC',
    'sp': 'SPE_REG_SP',
}

# ---------------- #
# All tokens
tokens = [
    # File tokens (end of file)
    'EOF',
    
    # Comments
    'INLINE_COMMENT', 'BLOCK_COMMENT',
    
    # Delimiters end-of-line . ; : ~ % $ @ # ( ) [ ] { }
    'EOL', 'PERIOD', 'SEMI', 'COLON', 'TILDE', 'PLUS',
    'MINUS', 'PERCENT', 'DOLLAR', 'AT', 'HASHTAG',
    # 'LPAREN',   'RPAREN',
    'LBRACKET', 'RBRACKET',
    # 'LBRACE',   'RBRACE',
    
    # Operators <= == >=
    'LE', 'EQ', 'GE',
    
    # Literals (identifier, integer, hex, octal, binary, float, string, char)
    'IDENTIFIER', 'INST_IDENTIFIER', 'INT_LITERAL', 'HEX_LITERAL', 'OCT_LITERAL',
    'BIN_LITERAL', 'FLOAT_LITERAL', 'STRING_LITERAL', 'CHAR_LITERAL',
] + list(keywords.values())

# Ignore whitespaces, commas and tabulations
t_ignore = ', \t'

# ---------------- #
# Simple tokens
t_PERIOD       = r'\.'
t_SEMI         = r';'
t_COLON        = r':'
t_TILDE        = r'~'
t_PLUS         = r'\+'
t_MINUS        = r'-'
t_PERCENT      = r'\%'
t_DOLLAR       = r'\$'
t_AT           = r'\@'
t_HASHTAG      = r'\#'
t_LBRACKET     = r'\['
t_RBRACKET     = r'\]'
t_LE           = r'<='
t_EQ           = r'=='
t_GE           = r'>='

# ---------------- #
# Identifiers
def t_IDENTIFIER(t):
    r'(?<!\d)[A-Za-z_][A-Za-z0-9_]*'
    
    # Keywords look-up
    tokenType = keywords.get(t.value, 'IDENTIFIER')
    
    # Instruction Identifier look-up
    if tokenType == 'IDENTIFIER':
        if t.value.lower() in c.ALL_INSTRUCTIONS:
            tokenType = 'INST_IDENTIFIER'
    
    t.type = tokenType
    return t

# ---------------- #
# Newline
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = 'EOL'
    t.value = None
    return t

# ---------------- #
# Inline comments (dropped)
def t_INLINE_COMMENT(t):
    r'//.*'

# ---------------- #
# Block comments (dropped)
def t_BLOCK_COMMENT(t):
    r'/\*(?:.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# ---------------- #
# Hexadecimal constant
def t_HEX_LITERAL(t):
    r'(?i)0x\w*'
    value = t.value[2:].replace('_', '') # remove underscores
    try:
        t.value = int(value, 16)
    except ValueError:
        raise ParserError('Invalid hexadecimal literal', c.ERROR_INVALID_LITERAL)

    return t

# ---------------- #
# Octal constant
def t_OCT_LITERAL(t):
    r'(?i)0o\w*'
    value = t.value[2:].replace('_', '') # remove underscores
    try:
        t.value = int(value, 8)
    except ValueError:
        raise ParserError('Invalid octal literal', c.ERROR_INVALID_LITERAL)

    return t

# ---------------- #
# Binary constant
def t_BIN_LITERAL(t):
    r'(?i)0b\w*'
    value = t.value[2:].replace('_', '') # remove underscores
    try:
        t.value = int(value, 2)
    except ValueError:
        raise ParserError('Invalid binary literal', c.ERROR_INVALID_LITERAL)

    return t

# ---------------- #
# Float constant
def t_FLOAT_LITERAL(t):
    r'(?i)((?<!\w)\d\w*\.\w*[-\+]?\w*)|((?<!\w)\d\w*e[-\+]?\w+)|((?<!\w)\.\d\w*[-\+]?\w*)'
    value = t.value.replace('_', '') # remove underscores
    try:
        t.value = float(value)
    except ValueError:
        raise ParserError('Invalid float literal', c.ERROR_INVALID_LITERAL)

    return t

# ---------------- #
# Integer constant
def t_INT_LITERAL(t):
    r'(?i)(?<!\w)\d\w*'
    try:
        t.value = int(t.value)
    except ValueError:
        raise ParserError('Invalid integer literal', c.ERROR_INVALID_LITERAL)

    return t

# ---------------- #
# String constant
def t_STRING_LITERAL(t):
    r'\"(?:(?:\\\")|(?:\\\n)|[^\"\n])*\"'
    t.value = t.value[1:-1]                 # remove enclosing quotes
    # update line count (in case of multi-lines string)
    newlinesCount = t.value.count('\n')
    if newlinesCount:
        warn(
            logger=None,
            message='String spanning over multiple lines',
            warnID=c.WARNING_MULTILINE_STRING,
            module='assembler.parser'
        )
        t.lexer.lineno += newlinesCount
    
    t.value = t.value.replace('\\\n', '')   # remove backslash followed by \n
    t.value = t.value.replace('\\\"', '"')  # remove backslash before quotes
    for esc in c.ESCAPE_CODES:                # change escape codes to actual char
        t.value = t.value.replace(esc, c.ESCAPE_CODES[esc])
    return t

# ---------------- #
# Character constant
def t_CHAR_LITERAL(t):
    r'\'(?:(?:\\.)|[^\\\n])\''
    t.value = t.value[1:-1]
    t.value = t.value.replace('\\\'', '\'') # remove backslash before quote
    for esc in c.ESCAPE_CODES:                # change escape codes to actual char
        t.value = t.value.replace(esc, c.ESCAPE_CODES[esc])
    return t

# ---------------- #
# Errors handling
def t_error(t):
    # TODO: handle them
    raise ParserError('Illegal token')