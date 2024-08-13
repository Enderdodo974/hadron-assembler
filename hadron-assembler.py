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
import pathlib
import argparse
import logging
import logging.config
from json import load

# ------------------------------------ #
# Files imports
from src.tokenizer import HASMTokenizer
from src.argument_parser import setup_CLI_args
from src.util import CustomArgumentParser
from src.exceptions import _exit

# ------------------------------------ #
# Functions

def setup_logging(config_file: pathlib.Path) -> logging.Logger:
    
    with open(config_file) as f:
        config = load(f)
    
    logging.config.dictConfig(config)
    return logging.getLogger('assembler')

# Assemble function
def assemble(file: pathlib.Path, args: argparse.Namespace) -> ...:
    
    # ================================================== #
    # 1. Tokenize the source code
    
    tokenizer = HASMTokenizer(args.debug)
    tokens = tokenizer.tokenize(file)
    

# ------------------------------------ #
# Program entry point
if __name__ == '__main__':
    
    # Logging configuration
    loggingConfigFile = pathlib.Path('config/default/logger.json')
    logger = setup_logging(loggingConfigFile)
    # Get the handlers by name; that way it is easier to access them
    handlers = {handler.name: handler for handler in logger.handlers}
    # Until CLI arguments are parsed, set the level on stdout to warnings only
    handlers['stdout'].setLevel(logging.WARNING)
    logger.debug('logging set-up completed.')
    
    # Command Line arguments configuration
    argParser = CustomArgumentParser(
        prog='hadron-assembler.py',
        description='Assemble HASM (Hadron Assembly Language) source files\
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
        _exit(-1)
    
    # Logging level
    if arguments.quiet:
        handlers['stdout'].setLevel(logging.ERROR)
    if arguments.verbose == 1:
        handlers['stdout'].setLevel(logging.INFO)
    if arguments.verbose > 1 or arguments.debug:
        handlers['stdout'].setLevel(logging.DEBUG)
    
    # Warning flags for the logger
    if arguments.warnings is None:
        logger.warnings = []
    else:
        logger.warnings = arguments.warnings
    
    # Delete handlers dictionary
    del handlers
    
    logger.info('parsed CLI arguments:')
    logger.info(f'debug: {arguments.debug}')
    logger.info(f'verbose level: {arguments.verbose}')
    logger.info(f'quiet: {arguments.quiet}')
    logger.info(f'input file(s): {arguments.file}')
    logger.info(f'output file: {arguments.output_file}')
    logger.info(f'schematic file: {arguments.schem_file}')

    logger.info("completed set-up.")
    logger.info(f"starting compilation for file {arguments.file.absolute()}")

    # Assemble the source file
    assemble(arguments.file, arguments)

    # End compilation
    _exit(0)