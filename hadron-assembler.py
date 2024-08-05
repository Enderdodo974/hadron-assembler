#!/usr/bin/python3
#-*- coding: utf-8 -*-

# ---------------------------------------------------------------------------- #
# hadron-assembler.py
# 
# 
# 
# 
# ---------------------------------------------------------------------------- #

# ------------------------------------ #
# Libraries imports
import os
import sys
import pathlib
import argparse
import logging

# ------------------------------------ #
# Files imports
from src.logger import setup_logging
from src.tokenizer import HASMTokenizer
from src.argument_parser import setup_CLI_args

# ------------------------------------ #
# Functions

# Assemble function
def assemble() -> ...:
    pass

# ------------------------------------ #
# Program entry point
if __name__ == '__main__':
    
    # Logging configuration
    loggingConfigFile = pathlib.Path('config/default/logger.json')
    logger = setup_logging(loggingConfigFile)
    logger.debug(f'Logging set-up complete.')
    
    # Command Line arguments configuration
    argParser = argparse.ArgumentParser(
        prog='Hadron Assembler',
        description='Assemble Hadron Assembly Language source file(s)\
        into machine code and/or Minecraft schematics.',
        epilog='For more information, see the documentation at \
        https://github.com/Enderdodo974/hadron-assembler',
        add_help=False,
        exit_on_error=False
    )

    # Setup the CLI arguments
    setup_CLI_args(argParser)
    
    # Catch errors on parsed arguments
    try:
        arguments = argParser.parse_args()
    except argparse.ArgumentError as e:
        logger.critical(e)
        exit(-1)
    
    # Logging level
    if arguments.quiet:
        logger.setLevel(logging.ERROR)
    if arguments.verbose == 1:
        logger.setLevel(logging.INFO)
    elif arguments.verbose >= 1:
        logger.setLevel(logging.DEBUG)
    if arguments.debug:
        logger.setLevel(logging.DEBUG)
    
    logger.debug('Parsed CLI arguments:')
    logger.debug(arguments)