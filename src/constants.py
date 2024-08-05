# -*- encoding: utf-8 -*-

# ---------------------------------------------------------------------------- #
# constants.py
#
# Various constants for the Hadron Assembler. This file is meant to be used
# by the tokenizer, parser and assembler.
# ---------------------------------------------------------------------------- #

ESCAPE_CODES = {
    r'\n': '\n',
    r'\a': '\a',
    r'\b': '\b',
    r'\v': '\v',
    r'\f': '\f',
    r'\0': '\0',
    r'\t': '\t',
    r'\r': '\r',
}