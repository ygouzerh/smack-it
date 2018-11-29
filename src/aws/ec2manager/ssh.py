#! /usr/bin/env python3

"""
author : ygouzerh
date: 19/10/2018

Manage ssh
"""

from boto3 import resource
import sh
from .read import ReaderRunning
from ...utils.python.config_parser import Parser
from .security import Security

class Ssh:
    """
        Manage ssh
    """
    @staticmethod
    def go(ec2_id):
        """
            Go on an ec2
        """
        ip = resource('ec2').Instance(ec2_id).public_ip_address
        config = Parser.parse('instances.ini')
        key_path = Security.get_default_key_path()
        sh.ssh("-i", key_path, config["INSTANCES"]["ami_user"]+"@"+ip)
