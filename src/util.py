#-*- coding: utf-8 -*-

# ---------------------------------------------------------------------------- #
# util.py
#
# File containing various utility functions and classes used by the
# Hadron Assembler.
# ---------------------------------------------------------------------------- #

# ------------------------------------ #
# Library imports
import logging
from argparse import ArgumentParser, ArgumentError
from typing import NoReturn

# ------------------------------------ #
# Classes

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

# Custom Argument Parser used to handle argument errors
class CustomArgumentParser(ArgumentParser):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
    
    def error(self, message: str) -> NoReturn:
        raise ArgumentError(None, message)