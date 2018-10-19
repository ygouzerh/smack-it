#! /usr/bin/env python3

"""
author : ygouzerh
date: 19/10/2018

Parse ini files for configuration.
Need to pass in parameters
the relativ path to the /config folder
of a .ini file
"""

from configparser import ConfigParser
import os
from pathlib import Path

class Parser():
    @staticmethod
    def parse(config_relativ_path):
        """
            Parse a config files,
            and return a config object.
        """
        # Get the absolute path of this file
        absolute_path = Path(os.path.dirname(os.path.abspath(__file__)))
        # Get the absolute path of the /config folder
        config_path = absolute_path.parent.parent.parent / "config" / config_relativ_path
        # Create the parser
        config = ConfigParser()
        # Parse the file
        config.read(config_path.absolute())
        # Return the file parsed
        return config
        