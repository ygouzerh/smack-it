#! /usr/bin/env python3

"""
author : ygouzerh
date: 19/10/2018

Manage our subnet
"""

from boto3 import client, resource
from .tagger import Tagger
from .vpc import Vpc

class Subnet:
    """
        Manage our subnet
    """

    @staticmethod
    def get_our_subnet():
        """
            Return the vpc id or False if not
        """
        vpc = Vpc.get_our_vpc()
        if vpc is not None:
            subnets = list(vpc.subnets.all())
            if subnets:
                return subnets[0]
        return None
