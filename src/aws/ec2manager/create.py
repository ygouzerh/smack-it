#! /usr/bin/env python3

"""
author : ygouzerh
date: 19/10/2018

API to create ec2 instances.
"""

from boto3 import resource
from fire import Fire
from configparser import ConfigParser
import os
from pathlib import Path
from ...utils.python.config_parser import Parser

class Creator():
    """
        Create ec2 instances
    """
    @staticmethod
    def execute(min_count=1, max_count=1):
        """
            WRAPPER
            Create an ec2 instance with an ami file,
            a minimal number of instances and a maximal number of
            instances
        """
        # Retrieve the if of the ami that we want to launch. => OS
        config = Parser.parse('instances.ini')
        ami_image_id = config['INSTANCES']['ami_id']
        instance_type = config['INSTANCES']['instance_type']
        # Create the ec2. WARNING : Stop this after
        print(ami_image_id)
        try:
            instances = resource('ec2').create_instances(ImageId=ami_image_id, InstanceType=instance_type, MinCount=min_count, MaxCount=max_count)
            # Debug message
            print("EC2 are fully created: ")
            for instance in instances:
                print("\t{}".format(instance.id))
        except Exception as exception:
            print(exception)
            print("Error during the instance creation")
            # TODO : Revert the possible instance
