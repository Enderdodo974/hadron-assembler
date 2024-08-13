#!/usr/bin/python3
#-*- coding: utf-8 -*-

# ---------------------------------------------------------------------------- #
# argument_parser.py
# 
# This script is used to parse the arguments of the Hadron Assembler.
# It is meant to set up the command line arguments parsing.
# ---------------------------------------------------------------------------- #

# -------------------------------------------------------- #
# Libraries imports
import pathlib
from argparse import ArgumentParser
from logging import getLogger

# -------------------------------------------------------- #
# Files imports
import src.constants as c

# -------------------------------------------------------- #
# Logging set-up
logger = getLogger('assembler')

# -------------------------------------------------------- #
# Functions

# Command line arguments parsing
def setup_CLI_args(arg_parser: ArgumentParser) -> ...:

    # -------------------------------------------------------- #
    # Miscanelleous
    # -------------------------------------------------------- #

    arg_parser.add_argument(
        '-V', '--version',
        help='Show the version number and exit.',
        action='version',
        version='%(prog)s v0.1'
    )
    arg_parser.add_argument(
        '-h', '--help',
        help='Show this help message and exit.',
        action='help'
    )

    # -------------------------------------------------------- #
    # Logging level
    # -------------------------------------------------------- #

    loglevelGroup = arg_parser.add_argument_group(
        'Logging level',
        description='The logging level for the assembler.\
        Each option can be used individually but cannot be combined.'
    ).add_mutually_exclusive_group()
    
    loglevelGroup.add_argument(
        '-d', '--debug',
        help='Print out debug information.',
        action='store_true',
        default=False
    )
    loglevelGroup.add_argument(
        '-v', '--verbose',
        help='Print out additional information during compilation.\
        Can be used multiple times to increase verbosity.',
        action='count',
        default=0,
    )
    loglevelGroup.add_argument(
        '-q', '--quiet',
        help='Suppress all output except for errors.',
        action='store_true',
        default=False
    )
    
    # -------------------------------------------------------- #
    # Input and output files
    # -------------------------------------------------------- #
    
    fileGroup = arg_parser.add_argument_group(
        'Input and output files',
        description='The various input and output files for the assembler.'
    )
    
    fileGroup.add_argument(
        'file',
        help='Input file to assemble. Has to be in a standard text format file.',
        type=pathlib.Path
    )
    fileGroup.add_argument(
        '-o', '--output',
        help='Output file name to write the machine code to.\
        Defaults to `out/a.out`',
        type=pathlib.Path,
        default=pathlib.Path('out/a.out'),
        dest='output_file',
        nargs='?'
    )
    fileGroup.add_argument(
        '-s', '--schematic',
        help='Write the output machine code as a Minecraft schematic file.',
        type=pathlib.Path,
        default=None,
        dest='schem_file',
        nargs='?'
    )

    # -------------------------------------------------------- #
    # Warning and errors
    # -------------------------------------------------------- #
    
    warningGroup = arg_parser.add_argument_group(
        'Warning and errors',
        description='How the assembler should handle various\
        warnings during compilation.'
    )
    
    warningGroup.add_argument(
        '-Wall', '--all-warnings',
        dest='warnings',
        help='Print out all encountered warnings',
        action='append_const',
        const=c.WARNING_ALL
    )
    
    warningGroup.add_argument(
        '-Werr', '--warnings-as-errors',
        dest='warnings',
        help='Treat all encountered warnings as errors',
        action='append_const',
        const=c.WARNING_AS_ERRORS
    )
    
    warningGroup.add_argument(
        '-Wmultiline-strings',
        dest='warnings',
        help='Warn about strings spanning over multiple lines',
        action='append_const',
        const=c.WARNING_MULTILINE_STRING
    )
    
    logger.debug('all CLI arguments added.')
