#! /usr/bin/env python3

"""
author : ygouzerh
date: 19/10/2018

Deploy the configuration on the instances
"""

from boto3 import resource
import sh
from .read import ReaderRunning
from ...utils.python.config_parser import Parser
from .ssh import Ssh

class Deployer:
    """
        Deploy the configuration on each ec2
    """
    @staticmethod
    def deploy():
        """
            Deploy the configuration
        """
        instances = ReaderRunning.instances()
        for instance in instances:
            Ssh.go(instance.id)
            print("Is go")
            _ = input()
