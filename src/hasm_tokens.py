#-*- coding: utf-8 -*-

# ---------------------------------------------------------------------------- #
# hasm_tokens.py
#
# Token specifications for symbols in Hadron Assembly Language. This file is
# meant to be used by the dedicated tokenizer.
# ---------------------------------------------------------------------------- #

# ------------------------------------ #
# File imports
from src.constants import ESCAPE_CODES

# ------------------------------------ #
# Tokens

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

# All tokens
tokens = [
    # File tokens (end of file)
    'EOF'
    
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
    'IDENTIFIER', 'INT_LITERAL', 'HEX_LITERAL', 'OCT_LITERAL', 'BIN_LITERAL',
    'FLOAT_LITERAL', 'STRING_LITERAL', 'CHAR_LITERAL',
]

# Ignore whitespaces, commas and tabulations
t_ignore = ', \t'

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

# Identifiers
t_IDENTIFIER   = r'(?<!\d)[A-Za-z_][A-Za-z0-9_]*'

# Newline
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = 'EOL'
    t.value = None
    return t

# Inline comments (dropped)
def t_INLINE_COMMENT(t):
    r'//.*'

# Block comments (dropped)
def t_BLOCK_COMMENT(t):
    r'/\*(?:.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# Hexadecimal constant
def t_HEX_LITERAL(t):
    r'(?i)0x\w*'
    t.value = t.value[2:].replace('_', '') # remove underscores
    try:
        t.value = int(t.value, 16)
    except ValueError:
        raise SyntaxError(f'invalid hexadecimal literal')
    except Exception:
        raise Exception('Uncaught exception')
    finally:
        pass
    
    return t

# Octal constant
def t_OCT_LITERAL(t):
    r'(?i)0o\w*'
    t.value = t.value[2:].replace('_', '') # remove underscores
    try:
        t.value = int(t.value, 8)
    except ValueError:
        raise SyntaxError(f'invalid octal literal')
    except Exception:
        raise Exception('Uncaught exception')
    finally:
        pass
    
    return t

# Binary constant
def t_BIN_LITERAL(t):
    r'(?i)0b\w*'
    t.value = t.value[2:].replace('_', '') # remove underscores
    try:
        t.value = int(t.value, 2)
    except ValueError:
        raise SyntaxError(f'invalid binary literal')
    except Exception:
        raise Exception('Uncaught exception')
    finally:
        pass
    
    return t

# Float constant
def t_FLOAT_LITERAL(t):
    r'(?i)((?<!\w)\d\w*\.\w*[-\+]?\w*)|((?<!\w)\d\w*e[-\+]?\w+)|((?<!\w)\.\d\w*[-\+]?\w*)'
    # sheesh the size of that regex
    try:
        t.value = float(t.value)
    except ValueError:
        raise SyntaxError(f'invalid float literal')
    except Exception:
        raise Exception('Uncaught exception')
    finally:
        pass
    
    return t

# Integer constant
def t_INT_LITERAL(t):
    r'(?i)(?<!\w)\d\w*'
    try:
        t.value = int(t.value)
    except ValueError:
        raise SyntaxError(f'invalid integer literal')
    except Exception:
        raise Exception('Uncaught exception')
    finally:
        pass
    
    return t

# String constant
def t_STRING_LITERAL(t):
    r'\"(?:(?:\\\")|(?:\\\n)|[^\"\n])*\"'
    t.value = t.value[1:-1]                 # remove enclosing quotes
    # update line count (in case of multi-lines string)
    newlinesCount = t.value.count('\n')
    if newlinesCount:
        # TODO: Warning
        t.lexer.lineno += newlinesCount
    t.value = t.value.replace('\\\n', '')   # remove backslash followed by \n
    t.value = t.value.replace('\\\"', '"')  # remove backslash before quotes
    for esc in ESCAPE_CODES:                # change escape codes to actual char
        t.value = t.value.replace(esc, ESCAPE_CODES[esc])
    return t

# Character constant
def t_CHAR_LITERAL(t):
    r'\'(?:(?:\\.)|[^\\\n])\''
    t.value = t.value[1:-1]
    t.value = t.value.replace('\\\'', '\'') # remove backslash before quote
    for esc in ESCAPE_CODES:                # change escape codes to actual char
        t.value = t.value.replace(esc, ESCAPE_CODES[esc])
    return t

# Uncaught Errors handling
def t_error(t):
    print(f"Uncaught Error: Illegal sequence {t.value}")