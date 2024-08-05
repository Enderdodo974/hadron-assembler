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
from json import load

# ------------------------------------ #
# Files imports
from src.tokenizer import HASMTokenizer
from src.argument_parser import setup_CLI_args
from src.util import CustomArgumentParser

# ------------------------------------ #
# Functions

def setup_logging(config_file: pathlib.Path) -> logging.Logger:
    
    with open(config_file) as f:
        config = load(f)
    
    logging.config.dictConfig(config)
    logger = logging.getLogger('assembler')
    
    return logger
# Assemble function
def assemble() -> ...:
    pass

# ------------------------------------ #
# Program entry point
if __name__ == '__main__':
    
    # Logging configuration
    loggingConfigFile = pathlib.Path('config/default/logger.json')
    logger = setup_logging(loggingConfigFile)
    # Get the handlers by name; that way it is easier to access them
    handlers = {handler.name: handler for handler in logger.handlers}
    # Until CLI arguments are parsed, set the level on stdout to warning only
    handlers['stdout'].setLevel(logging.WARNING)
    logger.debug('Logging set-up completed.')
    
    # Command Line arguments configuration
    argParser = CustomArgumentParser(
        prog='hadron-assembler.py',
        description='Assemble HASM (Hadron Assembly Language) source file(s)\
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
        handlers['stdout'].setLevel(logging.ERROR)
    if arguments.verbose == 1:
        handlers['stdout'].setLevel(logging.INFO)
    if arguments.verbose > 1 or arguments.debug:
        handlers['stdout'].setLevel(logging.DEBUG)
    
    logger.debug('Parsed CLI arguments:')
    logger.debug(f'Debug: {arguments.debug}')
    logger.debug(f'Verbose level: {arguments.verbose}')
    logger.debug(f'Quiet: {arguments.quiet}')
    logger.debug(f'Input file(s): {arguments.file}')
    logger.debug(f'Output file: {arguments.output_file}')
    logger.debug(f'Schematic file: {arguments.schem_file}')

    # TODO: instanciate the tokenizer
