#! /usr/bin/env python3

"""
author : ygouzerh
date: 19/10/2018

Manage the vpc
"""

from boto3 import client, resource
from .tagger import Tagger

class Vpc:
    """
        Manage the vpc
    """
    @staticmethod
    def get_vpcs():
        """
            Get the id of the vpc
        """
        response = client('ec2').describe_vpcs(Filters=[Tagger.get_project_filter()])
        return response['Vpcs']

    @staticmethod
    def get_our_vpc():
        """
            Return the vpc id or False if not
        """
        vpcs = Vpc.get_vpcs()
        if not vpcs:
            return None
        else:
            return resource('ec2').Vpc(vpcs[0]["VpcId"])
