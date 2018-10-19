#!/usr/bin/env python3

"""
author : ygouzerh
date : 19/10/2018

Terminate action.
"""

# Relative import
from .action import ActionOnInstance
from boto3 import client
from fire import Fire

class Terminate(ActionOnInstance):
    """
        Could be used to terminate instance
    """
    @classmethod
    def _concrete_action(cls, instances_ids, dry_run):
        """
            Inner action to terminate instances
        """
        client('ec2').terminate_instances(InstanceIds=instances_ids, DryRun=dry_run)