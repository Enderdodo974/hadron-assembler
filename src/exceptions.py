#-*- coding: utf-8 -*-

# ---------------------------------------------------------------------------- #
# exceptions.py
# 
# This file lists all exceptions generated during assembling and compiling.
# ---------------------------------------------------------------------------- #

# -------------------------------------------------------- #
# Libraries imports
from logging import getLogger, Logger
from typing import NoReturn

# -------------------------------------------------------- #
# Files imports
from src.util import get_line

# -------------------------------------------------------- #
# Classes

# Base exception for Assembly Errors
class AssemblyError(Exception):
    
    def __init__(self, message: str, errID: int = 0) -> None:
        self.message = message
        self.errID = errID

# Parser Error
class ParserError(AssemblyError):
    
    def __init__(self, message: str, errID: int = 0) -> None:
        super().__init__(message, errID)

# Preprocessor Error
class PreprocessorError(AssemblyError):
    
    def __init__(self, message: str, errID: int = 0) -> None:
        super().__init__(message, errID)

# -------------------------------------------------------- #
# Functions

# Exit function, just logs a message before exiting
def _exit(exitCode: int = 0) -> NoReturn:
    getLogger('assembler').info('compilation terminated.')
    exit(exitCode)

# Warn function: used as a replacement of the logger.warning() method
def warn(
        logger: Logger | None,
        message: str,
        warnID: int = 0,
        module: str = 'assembler'
    ) -> None:
    
    # Get the logger
    if logger is None:
        logger = getLogger(module)

    # Get the extra informations passed to the logger
    try:
        extra = logger.extra
    except AttributeError:
        extra = {}
    finally:
        extra.update({'warnID': warnID})
    
    # If line informations are available, log the current line
    if source := extra.get('source', None):
        line, col = get_line(source, extra.get('source_pos'))
        logger.warning(line, extra=extra)
        logger.warning(' '*col + '^', extra=extra)
    
    # Log the message
    logger.warning(message, extra=extra)

# Error function: used as a replacement of the logger.error() method
def error(
        logger: Logger | None,
        message: str,
        errID: int = 0,
        module: str = 'assembler'
    ) -> NoReturn:

    # Get the logger
    if logger is None:
        logger = getLogger(module)
    
    # Get the extra informations passed to the logger
    try:
        extra = logger.extra
    except AttributeError:
        extra = {}
    finally:
        extra.update({'errID': errID})
    
    # If line informations are available, log the current line
    if source := extra.get('source', None):
        line, col = get_line(source, extra.get('source_pos'))
        logger.error(line, extra=extra)
        logger.error(' '*col + '^', extra=extra)
    
    # Log the message and exit
    logger.error(message, extra=extra)
    _exit(errID)