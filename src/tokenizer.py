#-*- coding: utf-8 -*-

# ---------------------------------------------------------------------------- #
# tokenizer.py
# 
# This file contains the tokenizer for the Hadron Assembler. It is used by
# instancing the HASMTokenizer and reading a source file.
# ---------------------------------------------------------------------------- #

# -------------------------------------------------------- #
# Libraries imports
import pathlib
from ply import lex
from logging import getLogger

# -------------------------------------------------------- #
# Files imports
import src.hasm_tokens as hasm_tokens
import src.constants as c
from src.exceptions import ParserError, error

# -------------------------------------------------------- #
# Classes
class HASMTokenizer:
    
    def __init__(self, debug: bool = False) -> None:
        
        self.debug = debug
        self.logger = getLogger('assembler.parser')
        self.logger.extra = {
            'warnID': None,
            'errID': None,
            'source': None,
            'source_name': None,
            'source_line': None,
            'source_pos': None
        }
        self.lexer = lex.lex(
            module=hasm_tokens,
            debug=debug,
            debuglog=self.logger
        )

    def tokenize(self, file: pathlib.Path) -> list[lex.LexToken]:

        try:
            with open(file) as f:
                source = f.read()
        except FileNotFoundError:
            error(
                logger=self.logger, 
                message=f"Error trying to open file '{file.absolute()}'.", 
                errID=c.ERROR_FILE_NOT_FOUND
            )
        except OSError:
            error(
                logger=self.logger,
                message=f"Error opening file '{file.absolute()}'.",
                errID=c.ERROR_OPENING_FILE
            )

        # Input source to the lexer
        self.lexer.input(source)

        # Setup logger extra info
        self.logger.extra['source_name'] = file.name
        self.logger.extra['source'] = source

        # Tokenize the source code
        tokens = []
        while True:
            try:
                token = self.lexer.token()
            except ParserError as err:
                self.logger.extra['errID']       = err.errID
                self.logger.extra['source_line'] = self.lexer.lineno
                self.logger.extra['source_pos']  = self.lexer.lexpos
                error(self.logger, err.message, err.errID)

            # Update logger extra infos
            self.logger.extra['source_line'] = self.lexer.lineno
            self.logger.extra['source_pos']  = self.lexer.lexpos

            # EOF reached
            if not token: break

            # Debug the tokens
            if self.debug: self.logger.debug(token)

            tokens.append(token)

        self.logger.info(f"tokenized source file '{file.absolute()}'")
        self.logger.info(f'total: {len(tokens)} tokens.')

        return tokens