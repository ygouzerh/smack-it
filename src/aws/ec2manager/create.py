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
import time
from pathlib import Path
from ...utils.python.config_parser import Parser

class Creator:
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
        subnet_id = config['INSTANCES']['subnet_id']
        key_name = config['INSTANCES']['key_name']
        security_group_id = config['INSTANCES']['security_group_id']
        # Create the ec2. WARNING : Stop this after
        try:
            instances = resource('ec2').create_instances(ImageId=ami_image_id, InstanceType=instance_type, MinCount=min_count,\
                                                        MaxCount=max_count, SubnetId=subnet_id, KeyName=key_name, SecurityGroupIds=[security_group_id])
            # Wait until each instances are running
            Creator._wait_until_created(instances)
            # Debug message
            print("EC2 are fully created: ")
            for instance in instances:
                print("\t{}".format(instance.id))
        except Exception as exception:
            print(exception)
            print("Error during the instance creation")
            # TODO : Revert the possible instance

    @staticmethod
    def _wait_until_created(instances):
        """
            Wait until all instances are
            fullty created
        """
        all_runned = False
        while(Creator._check_all_runned(instances) != True):
            print("Still in creation.")
            time.sleep(5)

    @staticmethod
    def _check_all_runned(instances):
        """
            Check if all instances are runned
        """
        # Update the instances to get the last status
        instances = resource('ec2').instances.filter(InstanceIds=[instance.id for instance in instances])
        for instance in instances:
            if(instance.state["Name"] != 'running'):
                return False
        return True
