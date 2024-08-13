#-*- coding: utf-8 -*-

# ---------------------------------------------------------------------------- #
# util.py
#
# File containing various utility functions and classes used by the
# Hadron Assembler.
# ---------------------------------------------------------------------------- #

# -------------------------------------------------------- #
# Library imports
from sys import stderr
import logging
from argparse import ArgumentParser, ArgumentError
from typing import NoReturn

# -------------------------------------------------------- #
# Files imports
import src.constants as c

# -------------------------------------------------------- #
# Classes

# ------------------------------------ #
# Colored formatter class used for stdout logging
# Source: https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
class ColoredFormatter(logging.Formatter):

    GREY = "\x1b[38;20m"
    BOLD_BLUE = "\x1b[1;36;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"
    # Logging format : [TIME] - FILE:LINE: LEVEL: MESSAGE
    _format = "[%(asctime)s] - %(filename)s:%(lineno)d: {COL}%(levelname)s" \
        + RESET + ": %(message)s"

    FORMATS = {
        logging.DEBUG:      GREY,
        logging.INFO:       BOLD_BLUE,
        logging.WARNING:    YELLOW,
        logging.ERROR:      RED,
        logging.CRITICAL:   BOLD_RED,
    }

    def format(self, record) -> str:

        # Lower the level name and replace critical with fatal
        if record.levelno == logging.CRITICAL:
            record.levelname = 'FATAL'
        record.levelname = record.levelname.lower()

        # If source file name and line are available, use them
        source_name = record.__dict__.get('source_name', None)
        log_fmt = self._format
        if source_name is not None:
            log_fmt = self._format.replace('%(filename)s', '%(source_name)s')
            log_fmt = log_fmt.replace('%(lineno)d', '%(source_line)d')

        # Colorize the level name
        color = self.FORMATS.get(record.levelno)
        log_fmt = log_fmt.replace("{COL}", color)

        # Format the message
        # TODO: avoid instancing a new Formatter for this
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# ------------------------------------ #
# Full formatter for log files
class FullFormatter(logging.Formatter):

    _format = '[{asctime}][{levelname:^8}]({filename}:{lineno}) {source_name}:{source_line}: {message}'

    def format(self, record: logging.LogRecord) -> str:

        # Remove the source file name and line number if not available
        source_name = record.__dict__.get('source_name', None)
        log_fmt = self._format
        if source_name is None:
            log_fmt = self._format.replace('{source_name}:{source_line}: ', '')

        # Format the message
        # TODO: avoid instancing a new Formatter for this
        formatter = logging.Formatter(log_fmt, style='{')
        return formatter.format(record)

# ------------------------------------ #
# Custom Argument Parser used to handle CLI argument errors properly
class CustomArgumentParser(ArgumentParser):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
    def error(self, message: str) -> NoReturn:
        self.print_usage(stderr)
        raise ArgumentError(None, message) # TODO: additional info

# ------------------------------------ #
# Warning Filter
# Used to drop all warnings not specified as arguments during
# CLI arguments parsing (with the -W... flags)
class WarningFilter(logging.Filter):
    
    def filter(self, record: logging.LogRecord) -> bool:
        
        # Skip everything other than warnings
        if not record.levelno == logging.WARNING:
            return True
        
        # Get the warning ID
        warnID = record.__dict__.get('warnID', 0)
        
        # Get the global list of warnings
        warnings = logging.getLogger('assembler').warnings
        
        # If it should be treated as an error (-Werr)
        if c.WARNING_AS_ERRORS in warnings:
            record.levelno = logging.ERROR
            record.levelname = 'ERROR'
        
        # # If the -Wall flag is on
        if c.WARNING_ALL in warnings:
            return True
        
        # If the warning ID is in the global list
        if warnID in warnings:
            return True
        
        # # Otherwise, drop it
        return False

# -------------------------------------------------------- #
# Functions

# get_line(source: str, pos: int)
# get the entire line in which pos is,
# pos is the character position in the source
# returns the line string and the position of pos in the line
def get_line(source: str, pos: int) -> tuple[str, int]:
    
    assert 0 <= pos < len(source) #TODO: proper handling
    
    lineStart = source.rfind('\n', 0, pos) + 1
    lineEnd   = source.find('\n', pos)
    pos = pos - lineStart
    
    if lineEnd == -1:
        return (source[lineStart:], pos)
    
    return (source[lineStart:lineEnd], pos)