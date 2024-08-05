#-*- coding: utf-8 -*-

# ---------------------------------------------------------------------------- #
# logger.py
#
# Logger for the Hadron Assembler. It is used to produce logs and debug messages
# both in the console and in various log files.
# ---------------------------------------------------------------------------- #

# ------------------------------------ #
# Library imports
import logging
import json
import logging.config
import pathlib

# ------------------------------------ #
# Functions

def setup_logging(config_file: pathlib.Path) -> logging.Logger:
    
    with open(config_file) as f:
        config = json.load(f)
    
    logging.config.dictConfig(config)
    logger = logging.getLogger('assembler')
    
    return logger