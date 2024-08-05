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
        color = self.FORMATS.get(record.levelno)
        log_fmt = self._format.replace("{COL}", color)
        formatter = logging.Formatter(log_fmt)
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
        
        # # Skip everything other than warnings
        # if not record.levelno == logging.WARNING:
        #     return True
        
        # # Get the warning ID
        # warning = record.__dict__.get('warn', 0)
        
        # # Get the global list of warnings
        # warnings = [2, 4, 9] # TODO find a way to access the global list
        
        # # If it should be treated as an error
        # if warn_as_err:
        #     record.levelno = logging.ERROR
        #     record.levelname = 'ERROR'
        
        # # If the -Wall flag is on
        # if 1 in warnings:
        #     return True
        
        # # If the warning ID is in the global list
        # if warning in warnings:
        #     return True
        
        # # Otherwise, drop it
        # return False
        
        return True
