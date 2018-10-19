#! /usr/bin/env python3

"""
author: ygouzerh
date: 19/10/2018

Create a CLI using the Fire package to
easily maintain our ec2 instances.
"""

from fire import Fire
from src.aws.ec2manager.start import Start
from src.aws.ec2manager.read import ReaderCli
from src.aws.ec2manager.stop import Stop
from src.aws.ec2manager.terminate import Terminate
from src.aws.ec2manager.create import Creator

class Manage:
    """
        Perform management actions
        on ec2 instances.
    """
    @staticmethod
    def start():
        """
            Start ec2 instances
        """
        return Start

    @staticmethod
    def read():
        """
            Get informations about
            ec2 instances
        """
        return ReaderCli
    
    @staticmethod
    def stop():
        """
            Stop ec2 instances
        """
        return Stop

    @staticmethod
    def terminate():
        """
            Get informations about
            ec2 instances
        """
        return Terminate

    @staticmethod
    def create():
        return Creator    

if __name__ == '__main__':
    Fire(Manage)


